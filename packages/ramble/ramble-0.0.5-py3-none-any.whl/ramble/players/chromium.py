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
import base64
import logging
import os
import subprocess
import time

import cproto

from dynaconf import settings as config
from ramble.lib.ramble_screen import parse_screenres

# Enable Page domain events
# cp.Page.enable()
# Adds Page callback that's fired after is loaded
# cp.Page.loadEventFired = on_load

class Browser:
    def __init__(self, headless=False, nimages=1, screenshot_dir=None, dt=1):
        self.cp = None
        self.headless = headless
        self.nimages = nimages
        self.screenshot_dir = screenshot_dir or f"~/.ramble/{config['profile']}"
        self.lt = None
        self.dt = dt
        self.i = 0

    async def __aenter__(self):
        screen_resolution = parse_screenres(config.get("screen_resolution"))
        if config["screen_captures"]:
            if not os.path.isdir(self.screenshot_dir):
                os.makedirs(self.screenshot_dir)

        chromium_path = os.environ.get("RAMBLE_CHROMIUM_PATH", "/usr/bin/" + config["browser"])

        screen_resolution = parse_screenres(config.get("screen_resolution"))
        if config["browser"] in ["chromium", "chromium-browser", "chrome", "chrome-browser", "google-chrome"]:
            outlog = open("/tmp/cb.log", "w")
            options = [
                chromium_path
            ]

            options.append("--use-mobile-user-agent")

            if self.headless:
                options.append("--headless")
            else:
                options.append("--class=ramble")
                options.append("--ramble")

            if config.get("screen_resolution")==config.get("fullscreen_resolution"):
                options.append("--start-fullscreen")
            else:
                "--window-size=%d,%d" % (screen_resolution[0], screen_resolution[1]),

            # we will need a play via xephyr mode
            options += [
                "--disable-gpu",
                "--window-position=0,0",
                # "--app=blank:",
                # "--content-shell-hide-toolbar",
                # "--force-app-mode",
                # "--hide-icons",
                "blank:",
                "--remote-debugging-port=9222",
            ]
            if config["ignore_certificate_errors"]:
                options.append("-test-type")
                options.append("--ignore-certificate-errors")
            if config["mute_audio"]:
                options.append("--mute-audio")

            # incognito or not ?
            # no browser or browser enabled ?

            print(options)
            self.sp = subprocess.Popen(
                options, env={**os.environ, **{"HOME": os.path.expanduser("~/.ramble/browser/"), "OS_POSIX": "1"}},
            )
        else:
            raise NotImplementedError

        connected = False
        logging.info("connecting to browser")
        delay = 0.3
        while not connected:
            try:
                await asyncio.sleep(delay)
                self.cp = cproto.CProto(host="127.0.0.1", port=9222)
                connected = True
            except:
                logging.info("failed to connect to browser - trying again")
                delay += 0.1
        self.lt = time.time()
        logging.info("connected to browser")
        if self.headless:
            # print(self.cp.Browser.getWindowBounds(windowId=1))
            self.cp.Browser.setWindowBounds(windowId=1, bounds=dict(left=0, top=0,
                                                                    width=screen_resolution[0],
                                                                    height=screen_resolution[1],
                                                                    windowState='normal'
                                                                    )
                                            )
        return self

    async def __aexit__(self, *args):
        try:
            self.cp.close()
        except:
            pass
        os.kill(self.sp.pid, 15)
        await asyncio.sleep(0.1)
        os.kill(self.sp.pid, 9)
        return False

    async def navigate(self, entry):
        url = entry["url"]
        timelimit = entry.get("duration")

        logging.debug("Asking browser to open %s ", url)
        done = False
        retries = 4
        while not done:
            try:
                rets = self.cp.Page.navigate(url=url)
                # print("---------------")
                # #'Accessibility', 'Animation', 'ApplicationCache', 'Audits', 'BackgroundService', 'Browser', 'CSS', 'CacheStorage', 'Cast', 'Console', 'DOM', 'DOMDebugger', 'DOMSnapshot', 'DOMStorage', 'Database', 'Debugger', 'DeviceOrientation', 'Emulation', 'Fetch', 'HeadlessExperimental', 'HeapProfiler', 'IO', 'IndexedDB', 'Input', 'Inspector', 'LayerTree', 'Log', 'Media', 'Memory', 'Network', 'Overlay', 'Page', 'Performance', 'Profiler', 'Runtime', 'Schema', 'Security', 'ServiceWorker', 'Storage', 'SystemInfo', 'Target', 'Tethering', 'Tracing', 'WebAudio', 'WebAuthn',
                # print(dir(self.cp))
                # print(dir(self.cp.Browser))
                # print(dir(self.cp.Page))
                # print(dir(self.cp.Target))
                # print(dir(rets))
                # print("---------------")
                done = True
            except:
                logging.debug("retrying...")
                await asyncio.sleep(0.5)
                retries -= 1
                if retries <= 0:
                    logging.exception("Error while trying to open url %r", url)
                    raise
        logging.info("Opened %s ", url)

    async def playing(self, entry):
        if time.time() - self.lt > self.dt:
            try:
                res = self.cp.Page.captureScreenshot()
                if config["screen_captures"]:
                    with open(os.path.expanduser(f"{self.screenshot_dir}/img{self.i % self.nimages}.png"), "wb") as f:
                        pdd = base64.b64decode(res["result"]["data"])
                        f.write(pdd)
                        f.close()
                        self.i += 1
            except:
                logging.exception("Exception while taking screenshot of page")
            self.lt = time.time()
        return True


Player = Browser
