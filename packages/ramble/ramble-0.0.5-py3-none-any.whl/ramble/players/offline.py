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
from ramble.utils import is_multimedia_url
from ramble.utils import ramble_offline_profile_path


class OfflinePlayer:
    def __init__(self, directory=None):
        self.directory = directory
        self.curcontentidx = 0
        self.browser = Browser(headless=True, nimages=True, screenshot_dir=f"{self.directory}/{self.curcontentidx}")
        self.browser_entered = False

    async def __aenter__(self):
        from dynaconf import settings as config

        self.directory = self.directory or ramble_offline_profile_path(config["profile"])
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        return self

    async def __aexit__(self, *args):
        if self.browser_entered:
            await self.browser.__aexit__(*args)
        return False

    async def navigate(self, entry):
        url = entry["url"]
        timelimit = entry.get("duration")
        if not os.path.isdir(f"{self.directory}/{self.curcontentidx}"):
            os.mkdir(f"{self.directory}/{self.curcontentidx}")
            pass
        if is_multimedia_url(url):
            p = subprocess.Popen(
                "youtube-dl %s" % (url,),
                shell=True,
                cwd=f"{self.directory}/{self.curcontentidx}",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            o, e = p.communicate()
            print(o)
        else:
            if not self.browser_entered:
                await self.browser.__aenter__()

            self.browser.screenshot_dir = f"{self.directory}/{self.curcontentidx}"
            await self.browser.navigate(entry)

        self.curcontentidx += 1
        return True

    async def playing(self, entry):
        return False

Player = OfflinePlayer
