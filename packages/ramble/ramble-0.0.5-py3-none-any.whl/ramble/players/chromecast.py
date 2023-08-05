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
import asyncio
import os

import catt.cli
import pychromecast
from catt.controllers import get_chromecast
from catt.controllers import get_chromecasts
from catt.controllers import setup_cast

from dynaconf import settings as config
import re
import subprocess

def shell_safe(url):
    if not re.match("[A-Za-z0-9:/_-&#,.]+", url):
        raise ValueError(url)
    return url


class ChromecastPlayer:
    async def __aenter__(self):
        if config.get("chromecast_wake_on_lan"):
            os.system("wakeonlan " + config.get("chromecast_wake_on_lan"))

        if not config["chromecast_device"]:
            config["chromecast_device"] = pychromecast.discover_chromecasts()[0][0]
        self.device = config["chromecast_device"]
        self.mode = "unset"
        self._cst = None
        return self

    @property
    def cst(self):
        if self._cst is None:
            self._cst = setup_cast(self.device)
        return self._cst

    async def __aexit__(self, *args):
        catt.cli.stop.callback.__wrapped__({"device": self.device})
        return False

    async def navigate(self, entry):
        print(entry)
        if entry.get("chromecast-via-xnest"):
            await self.play_via_xnest(entry)
        elif entry.get("chromecast-via-vlc"):
            await self.play_via_vlc(entry)
        else:
            await self.play_via_catt(entry)

        return True

    async def play_via_catt(self, entry):
        url = entry["url"]
        if "youtube" in url:
            # catt.cli.cast({"device": self.device, 'url': url})
            os.system("catt -d '%s' cast '%s'" % (self.device, url))
            stopped = False
            await asyncio.sleep(3)
            self.mode = "video"
        else:
            catt.cli.cast_site.callback.__wrapped__({"device": self.device}, url)
            self.mode = "url"

    async def play_via_vlc(self, entry, extra_opts="", env=None):
        url = entry["url"]
        env = env or os.environ
        timelimit = None
        # udo N
        if "timelimit" in entry:
            timelimit = int(entry["timelimit"])
        url = shell_safe(url)
        if timelimit is not None and timelimit >= 1:
            self.p = subprocess.Popen(
                "exec timelimit -T %s -t %s cvlc --play-and-exit  --sout chromecast --sout-chromecast-ip %s "
                "--sout-chromecast-video %s '%s'" % (timelimit, timelimit - 1, extra_opts, url), shell=True, env=env)
        else:
            self.p = subprocess.Popen("exec cvlc --play-and-exit  --sout-chromecast-ip %s"
                                      "--sout chromecast --sout-chromecast-video %s '%s'" % (self.device, extra_opts,
                                                                                             url,), shell=True, env=env)

    async def play_via_xnest(self, entry):
        # this records the desktop of x windows and cast its
        # https://wiki.archlinux.org/index.php/PulseAudio/Examples
        # ### Create Remap sink
        # load-module module-remap-sink sink_name=Remap_sink master=SINK_NAME channels=2 remix=no
        # set-default-sink Remap_sink
        #  pactl load-module module-null-sink sink_name=fcdv1op \ sink_properties=device.description="fcdv1op"
        # pactl load-module module-loopback latency_msec=1
        # export DISPLAY=xxxx
        # export PULSE_SYNC=xxxx
        # `pacmd list-sinks | grep -e 'name:' -e 'index:'"
        #                                       "| grep -A 1 '[*]' | grep name | cut -d : -f 2 | tr -d '<> '`
        orend = OffscreenRendering()
        await self.play_via_vlc({"url": "screen://"},
                           extra_opts=f"--input-slave pulse://{orend.cc1}.monitor",
                           env=orend.env
                           )

        self.mode = "xnest"

    async def playing(self, entry):
        if self.mode == "video":
            self.cst.prep_info()
            info = self.cst.info
            stopped = (info["player_state"] not in ["BUFFERING", "PLAYING", "PAUSED"]) or (
                (info["current_time"] is not None)
                and (info["duration"] is not None)
                and (info["current_time"] + 1 > info["duration"])
            )
            await asyncio.sleep(0.1)
            return not stopped
        elif self.mode == "vlc":
            if self.p.returncode is None:
                self.p.poll()
            if self.p.returncode is not None:
                self.p.wait()
            return self.p.returncode is None
        elif self.mode == "xnest":
            for p in [self.p, self.p1, self.p2, self.p3]:
                if p:
                    if p.returncode is None:
                        p.poll()
                    if p.returncode is not None:
                        p.wait()
                    if p.returncode:
                        # kill other
                        import time
                        time.sleep(10)
                        return False
            return True
        else:
            return True


Player = ChromecastPlayer
