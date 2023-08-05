#!/usr/bin/env python3
# ############################################################################
# |L|I|C|E|N|S|E|L|I|C|E|N|S|E|L|I|C|E|N|S|E|L|I|C|E|N|S|E|
# Copyright (c) Bertrand Nouvel.
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of the University nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
# |P|R|O|G|R|A|M|P|R|O|G|R|A|M|P|R|O|G|R|A|M|P|R|O|G|R|A|M|
# ############################################################################
"""
Copyright (c 2020) B.Nouvel and the ramble authors.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:
1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.
3. Neither the name of the University nor the names of its contributors
   may be used to endorse or promote products derived from this software
   without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
SUCH DAMAGE.
"""
import asyncio
import base64
import datetime
import functools
import logging
import math
import os
import random
import re
import shutil
import subprocess
import sys
import textwrap
import time
import urllib

import clize
import coloredlogs
import diskcache
import feedparser
import yaml

default_setting=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.yml')
print(default_setting)
from dynaconf import settings
settings.configure(settings_module=default_setting, ENVVAR_PREFIX_FOR_DYNACONF="RAMBLE")

from dynaconf import settings as config

print(dir(config))
print (config.to_dict())

from ramble.ramble_contents import tuple_entry_to_dict_entry
from ramble.ramble_engine import query_content
from ramble.players.chromecast import ChromecastPlayer
from ramble.players.chromium import Browser
from ramble.players.dummy import DummyPlayer
from ramble.players.pictures import PicturePlayer
from ramble.players.mpv import MPV
from ramble.players.offline import OfflinePlayer
from ramble.utils import ramble_path
from ramble.utils import ramble_profile_path
from ramble.utils import timestamp

logging.getLogger().setLevel(logging.DEBUG)


class SmartPlayer:
    # we should also allow rssfeeds
    PLAYERS = {"browser": Browser, "mpv": MPV}

    def __init__(self):
        self.current_player = None
        self.current_player_type = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        if self.current_player:
            await self.current_player.__aexit__(*args)
        return False

    def find_player_type(self, url):
        if "youtube" in url:
            return "mpv"
        return "browser"

    async def ensure_player(self, pt):
        if pt != self.current_player_type:
            if self.current_player:
                await self.current_player.__aexit__(None, None, None)
            self.current_player_type = pt
            self.current_player = self.PLAYERS[pt]()
            await self.current_player.__aenter__()

    async def navigate(self, entry):
        pt = self.find_player_type(entry["url"])
        await self.ensure_player(pt)
        res = await self.current_player.navigate(entry)
        return res

    async def playing(self, *args, **kwargs):
        return await self.current_player.playing(*args, **kwargs)


async def handle_action(action, player, entry, i, n):
    logging.info(action)
    dobreak = False
    if action == "next":
        dobreak = 1
    elif action == "exit":
        n = 1
        i = 1
        dobreak = 1
    elif action == "more":
        if "source" in entry:
            if hasattr(entry["source"], "more"):
                entry["source"].more(entry)
            else:
                logging.warning("source does not support more")
        else:
            logging.warning("source is not defined")
    elif action == "less":
        if "source" in entry:
            if hasattr(entry["source"], "less"):
                entry["source"].less(entry)
            else:
                logging.warning("source does not support less")
        else:
            logging.warning("source is not defined")
    elif action == "pause":
        res = await player.pause()
    elif action == "browser":
        import webbrowser
        webbrowser.open(entry["url"])
    return dobreak, entry, i, n


from .controls.stdin import StdinControl


async def run_play_list(player, max_rec=10, n=None, controls=None, **kwargs):
    logging.debug("Entering main loop")
    i = 0
    controls = controls or StdinControl()
    next_entry = current_entry = None
    while n is None or i < n:
        try:
            if next_entry == current_entry:
                next_entry = await query_content(max_rec=max_rec, **kwargs)  # FIXME (persistent changes?)
            current_entry = next_entry
            await player.navigate(current_entry)
            t0 = time.time()
            te = t0 + next_entry["duration"]

            # wait for event
            while time.time() < te:
                if controls is not None:
                    action = await controls.tick()
                    if action:
                        dobreak, next_entry, i, n = await handle_action(action, player, current_entry, i, n)
                        if dobreak:
                            break
                if not await player.playing(current_entry):
                    break
                await asyncio.sleep(0.1)
            i += 1
        except Exception as e:
            logging.exception("issue when loading next clip")
            await asyncio.sleep(1)
            # raise
    logging.debug("Leaving main loop")


PLAYERS = {
    "dummy": DummyPlayer,
    "smart": SmartPlayer,
    "browser": Browser,
    "chromecast": ChromecastPlayer,
    "video": MPV,
    "offline": OfflinePlayer,
    "picture": PicturePlayer,
    "pictures": PicturePlayer,
    "headless": lambda: Browser(headless=True, nimages=2),
    "screensaver_headless": lambda: Browser(headless=True, nimages=2,
                                            screenshot_dir=os.path.join(ramble_profile_path(config.get("profile")), "screensaver"))
}


def play_on_unlock(url=None, player_type="picture", n=5):
    import dbussy as dbus
    from dbussy import DBUS
    def message_filter(connection, message, data):
        if message.type == DBUS.MESSAGE_TYPE_SIGNAL:
            if message.interface == "org.freedesktop.ScreenSaver" and message.member == "ActiveChanged" and message.path == "/ScreenSaver" and \
                    (list(message.objects))[0] is False:
                burl = url or "default"
                if not burl.startswith("ramble://"):
                    burl = "ramble://" + burl
                loop = asyncio.get_event_loop()
                loop.create_task(_doplay(burl, player_type, n))
            sys.stdout.write \
                    (
                    "%s.%s[%s](%s)\n"
                    %
                    (
                        message.interface,
                        message.member,
                        repr(message.path),
                        ", ".join(repr(arg) for arg in message.objects)
                    )
                )
        # end if
        return DBUS.HANDLER_RESULT_HANDLED

    conn = dbus.Connection.bus_get(DBUS.BUS_SESSION, private=False)
    loop = asyncio.get_event_loop()
    conn.attach_asyncio(loop)
    conn.add_filter(message_filter, None)
    conn.bus_add_match("type=signal")
    loop.run_forever()


def play2(url=None, player_type="smart", n=-1):
    """
    Plays contents from various sources on a player

    :param profile: collection
    :param playlist: playlist to select inside of the profile
    :param player_type: player used to play
    """
    if n < 0:
        n = None
    url = url or "default"
    if not url.startswith("ramble://"):
        url = "ramble://" + url
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_doplay2(url, player_type, n))
    loop.close()

async def _doplay2(url=None, player_type="smart", n=-1):
    from ramble.lib.ramble_screen import ActivescreenRendering, NestedRendering
    async with ActivescreenRendering():
        async with NestedRendering() :
            await _doplay(url, player_type, n)

def play(url=None, player_type="smart", n=-1):
    """
    Plays contents from various sources on a player

    :param profile: collection
    :param playlist: playlist to select inside of the profile
    :param player_type: player used to play
    """
    if n < 0:
        n = None
    url = url or "default"
    if not url.startswith("ramble://"):
        url = "ramble://" + url
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_doplay(url, player_type, n))
    loop.close()


async def _doplay(url, player_type, n):
    async with PLAYERS[player_type]() as b:
        await run_play_list(b, url=url, n=n)
    return True


def server():
    """
    Runs a miniserver
    :return: 
    """
    import quart

    quart_app = quart.Quart("ramble")  # , static_folder=assets_folder, static_url_path=static_url,)

    @quart_app.route("/")
    async def get_content1():
        return quart.redirect((await query_content())["url"])

    @quart_app.route("/<playlist>")
    async def get_content2(playlist):
        return quart.redirect((await query_content(playlist=playlist))["url"])

    @quart_app.route("/<profile>/<playlist>")
    async def get_content3(profile, playlist):
        return quart.redirect((await query_content(profile=profile, playlist=playlist))["url"])

    quart_app.run()


def screensaver_install(screensaver_type="kscreenlocker", profile=None):
    """
    Configure a screensaver to show the images produced by ramble when online

    :param profile:
    :return:
    """
    if screensaver_type == "kscreenlocker":
        if not os.path.exists(os.path.expanduser("~/.config/kscreenlockerrc")):
            raise NotImplementedError(
                "Please install and configure kscreenlockerrc before we can install ramble-screensaver")
        if not os.path.exists(os.path.expanduser("~/.config/kscreenlockerrc.offline")):
            shutil.copy(os.path.expanduser("~/.config/kscreenlockerrc"),
                        os.path.expanduser("~/.config/kscreenlockerrc.offline"))
        connected = "default"
        if os.path.exists(os.path.join(ramble_path(), "get_connection_profile.sh")):
            subprocess.Popen()
            os.system(os.path.join(ramble_path(), "get_connection_profile.sh"))
        if connected:
            profile = connected
            kscreensaver = f"""
            [$Version]
            update_info=kscreenlocker.upd:0.1-autolock

            [Greeter]
            WallpaperPlugin=org.kde.slideshow

            [Greeter][Wallpaper][org.kde.slideshow][General]
            SlideInterval=10
            SlidePaths={os.path.join(ramble_profile_path(profile), "screensaver")}
            TransitionAnimationDuration=0.001
            """
            open(os.path.expanduser("~/.config/kscreenlockerrc"), "w").write(textwrap.dedent(kscreensaver))
        else:
            shutil.copy(os.path.expanduser("~/.config/kscreenlockerrc.offline"),
                        os.path.expanduser("~/.config/kscreenlockerrc"))
    else:
        raise NotImplementedError


def screensaver_daemon(url):
    config["screen_captures"] = True
    # subprocess.Popen(
    #     "exec Xvfb  -screen 0 %sx%sx24 %s " % (config["screen-resolution"][0], config["screen-resolution"][1], display),
    #     shell=True
    # )
    # # could configure to receive switch context from install
    # os.environ["DISPLAY"] = display
    play(url, player_type="screensaver_headless")


def show_help():
    print("ramble  a program to play contents from various sources on different media")
    print("ramble --help to know available command")
    print("ramble --play --help  to gep command specific help")


from .ramble_engine import get_playlist_parameters
from .ramble_engine import load_module


def transfer(source, destination):
    """Transfers a playlist from one storage to another"""

    async def _transfer():
        s = await get_playlist_parameters({"url": source})
        d = await get_playlist_parameters({"url": destination})
        pl = await (s[0].load_playlist(s[3], s[2]))
        await (d[0].create_playlist(s[3], s[2], pl))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(_transfer())
    loop.close()

    # file to db
    # ramble --transfer science science@mongo


def playlist(url):
    """Retrieves a playlist and displays it"""

    async def _playlist(url, indent=""):
        kwargs = {}
        kwargs["url"] = url
        from .ramble_engine import parse_ramble_url, load_module, load_urls
        current_module, current_module_name, current_playlist, current_profile = await get_playlist_parameters(kwargs)
        print(kwargs)
        contents, urls = await load_urls(current_playlist, current_profile, current_module)
        for u in urls:
            print(indent + str(u))
            if isinstance(u["url"], str) and u["url"].startswith("ramble://"):
                await(_playlist(u["url"], indent + "  "))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(_playlist(url))
    loop.close()


def main():
    clize.run(show_help,
              alt=[play, play2, playlist, play_on_unlock, screensaver_daemon, screensaver_install, server, transfer])


if __name__ == "__main__":
    main()
