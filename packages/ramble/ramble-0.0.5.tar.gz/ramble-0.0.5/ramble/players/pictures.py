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

from .chromium import Browser
from dynaconf import settings as config
from ramble.utils import is_multimedia_url
from ramble.utils import ramble_offline_profile_path
from ramble.lib.ramble_screen import parse_screenres
import pyglet
import asyncio
import json
import time
import logging
import webbrowser
from pyglet.window import mouse
import tempfile

pyglet_loop_active = True


async def pyglet_event_loop():
    while pyglet_loop_active:
        try:
            pyglet.clock.tick()
            for window in pyglet.app.windows:
                window.switch_to()
                window.dispatch_events()
                window.dispatch_event('on_draw')
                window.flip()

            await asyncio.sleep(0.02)
        except:
            logging.exception("Error in loop")


class PicturePlayer:
    def __init__(self, ncontents=2, maxduration=8):
        self.tempdir = tempfile.TemporaryDirectory()
        self.directory = self.tempdir.name
        self.curcontentidx = 0
        self.maxduration = maxduration
        self.ncontents = ncontents
        self.browser = Browser(headless=True, nimages=3, screenshot_dir=f"{self.directory}/{self.curcontentidx}")
        self.browser_entered = False
        w, h = parse_screenres(config.get("screen_resolution"))
        if w != 1980 or h != 1080:
            self.window = pyglet.window.Window(width=w, height=h)
        else:
            self.window = pyglet.window.Window(fullscreen=True)
        self.image = None
        self.displayed_entry = {}
        for curcontentidx in range(ncontents):
            if not os.path.isdir(f"{self.directory}/{curcontentidx}"):
                os.makedirs(f"{self.directory}/{curcontentidx}")
            entry = {"duration": 0}
            open(f"{self.directory}/{curcontentidx}/entry.json", "w").write(json.dumps(entry))

        self.timeout = time.time()

        @self.window.event
        def on_draw():
            self.window.clear()
            if self.image:
                self.image.blit(0, 0)

        @self.window.event
        def on_mouse_press(x, y, button, modifiers):
            if button == mouse.LEFT:
                webbrowser.open(self.displayed_entry["url"])

        self.pyglet_task = asyncio.create_task(pyglet_event_loop())

    async def __aenter__(self):
        from dynaconf import settings as config
        self.directory = self.directory or ramble_offline_profile_path(config["profile"])
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        if not self.browser_entered:
            await self.browser.__aenter__()

        return self

    async def __aexit__(self, *args):
        global pyglet_loop_active
        pyglet_loop_active = False
        if self.browser_entered:
            await self.browser1.__aexit__(*args)
        return False

    def display(self, curcontentidx):
        try:
            entry = json.loads(open(f"{self.directory}/{self.curcontentidx}/entry.json", "r").read())
            self.timeout = time.time() + min(self.maxduration, entry["duration"])
            self.image = pyglet.image.load(f"{self.directory}/{curcontentidx}/img0.png")
            self.displayed_entry = entry
        except:
            logging.exception("Issue during  display")

    async def navigate(self, entry):
        self.display((self.curcontentidx + (self.ncontents - 1)) % self.ncontents)

        url = entry["url"]
        timelimit = entry.get("duration")
        if not os.path.isdir(f"{self.directory}/{self.curcontentidx}"):
            os.mkdir(f"{self.directory}/{self.curcontentidx}")

        open(f"{self.directory}/{self.curcontentidx}/entry.json", "w").write(json.dumps(entry))
        self.browser.screenshot_dir = f"{self.directory}/{self.curcontentidx}"
        await self.browser.navigate(entry)

        self.curcontentidx += 1
        self.curcontentidx %= self.ncontents
        return True

    async def playing(self, entry):
        try:
            await self.browser.playing(entry)
        except:
            logging.exception("error while monitoring headless browser")
        return time.time() < self.timeout


Player = PicturePlayer
