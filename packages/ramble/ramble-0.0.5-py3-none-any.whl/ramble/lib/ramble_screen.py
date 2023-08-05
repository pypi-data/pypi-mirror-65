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

import os
import subprocess
import asyncio
from dynaconf import settings as config

## ---------------------------------------------------------------------------------------------------
##
## This manage the state of the screen
## For instance, we may want to render offscreen with audio for cast via chromecost or other fancy stuffs.
## Alternatively we may want to ensure that current screen is on and usable (dpms, etc...)
## or we may want to ensure that a specific window is displayed in a specific way on the screen
## and this may require setup/
##
## ---------------------------------------------------------------------------------------------------


class NestedRendering:
    """
    Provides offscreen rendering via nested X
    """

    def __init__(self, command="", display=":7", audiochannel=None, mode="xephyr", chromecast_stream=None):
        self.command = command
        self.p = []
        self.cp = None
        self.mode = mode

        self.display = display
        self.cc1 = audiochannel
        self.env = {k: v for k, v in os.environ.items()}
        self.env.update(
            {
                "DISPLAY": self.display,
            }
        )
        if self.cc1:
            self.env["PULSE_SYNC"] = self.cc1
        self.cast = None
        self.chromecast_stream = chromecast_stream

    async def __aenter__(self):
        #        self.p.append( subprocess.Popen("Xnest "+self.display, shell=True))
        if self.mode == "xephyr":
            sr = parse_screenres(config.get("screen_resolution"))
            self.p.append(
                subprocess.Popen("Xephyr -resizeable -title ramble -screen %sx%s %s" % (sr[0], sr[1], self.display),
                                 shell=True))
            config["fullscreen_resolution"] = config.get("screen_resolution")
        else:
            raise NotImplementedError

        self.saved_display = os.environ["DISPLAY"]
        os.environ["DISPLAY"] = self.display

        if self.cc1:
            self.cp = subprocess.Popen(
                "pactl load-module module-null-sink sink_name=%s sink_properties=device.description=\"%s\"" % (self.cc1,
                                                                                                               self.cc1),
                shell=True
            )

        self.p.append(subprocess.Popen(
            "[ -f ~/.config/i3/config] || i3-config-wizard ; i3",
            shell=True,
            env=self.env
        ))

        if self.command:
            self.p.append(subprocess.Popen(
                self.command,
                shell=True,
                env=self.env
            )
            )

        self._auto_tick_active = True

        if self.chromecast_stream:
            from ramble.players.chromecast import Chromecast
            self.ccast = Chromecast()
            await self.ccast.__aenter__()
            #                         extra_opts=f"--input-slave pulse://{cc1}.monitor",
            self.ccast.play_via_vlc({"url": "screen://"},

                                    env=env)

        # loop = asyncio.get_event_loop()
        # async def tf():
        #     await self._auto_tick()
        # self._auto_task = loop.create_task(tf)

        # self.p4 = subprocess.Popen(
        #     entry.get("command", "konsole"),
        #     shell=True,
        #     env=env
        # )

    async def _auto_tick(self):
        while self._auto_tick_active:
            self.tick()
            yield asyncio.sleep(0.1)

    def tick(self):
        for i, p in list(enumerate(self.p))[::-1]:
            if p.returncode is None:
                p.poll()
            if p.returncode is not None:
                p.wait()
                del self.p[i]
        self.p = []

    async def __aexit__(self):
        self._auto_tick_active = False

        self.tick()
        for i, p in list(enumerate(self.p)):
            os.kill(self.p[i], 9)
        self.tick()

        self._autotask.cancel()
        if self.cc1:
            os.system(
                "for m in $(pactl list modules | grep '" + cc1 + "' -B 3 | grep Module | cut -d '#' -f 2 | tr '\n' ' '); do pactl unload-module $m; done"
            )

        os.environ["DISPLAY"] = self.saved_display

        # await self.play_via_vlc({"url": "screen://"},
        #                         extra_opts=f"--input-slave pulse://{cc1}.monitor",
        #                         env=env
        # -sout="#chromecast{ip=ip_address}"
        #                         )
        #


class ActivescreenRendering:
    def __init__(self):
        pass

    async def __aenter__(self):
        os.system("xset s noblank")
        os.system("xset s off")
        os.system("xset dpms force on")
        os.system("xset -dpms")

    async def __aexit__(self, *args):
        os.system("xset +dpms")
        os.system("xset s on")

        # org.kde.kscreen.osdService
        # showOsd


def parse_screenres(screenres):
    if isinstance(screenres, str):
        return tuple(map(int, screenres.split("x")))
    else:
        return screenres
