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

config = {
    "browser": os.environ.get("RAMBLE_BROWSER", "chromium-browser"),
    "playlist-location": "~/.ramble/{profile}/playlist.yaml",
    "profile": "default",
    "playlist": "default",
    "schedule-context-command": os.environ.get("RAMBLE_SCHEDULE_CONTEXT_COMMAND", ""),
    "default-static-duration": float(os.environ.get("RAMBLE_DEFAULT_STATIC_DURATION", "20")),
    "default-video-duration": float(os.environ.get("RAMBLE_DEFAULT_VIDEO_DURATION", "14400")),
    "screen_captures": os.environ.get("RAMBLE_SCREEN_CAPTURES", "True").upper() in ["T", "TRUE", "1", "Y", "YES"],
    "bookmark-file-path": "~/.config/google-chrome/Default/Bookmarks",
    "chromecast-device": os.environ.get("CHROMECAST_DEVICE", ""),
    "screen-resolution": [int(x) for x in os.environ.get("RAMBLE_SCREEN_RESOLUTION", "1980x1080").split("x")],
    "ignore-certificate-errors": True,
    "mute-audio": os.environ.get("RAMBLE_MUTE_AUDIO", "True").upper() in ["T", "TRUE", "1", "Y", "YES"],
    "chromecast-wake-on-lan": os.environ.get("RAMBLE_WAKE_ON_LAN", None),  # "70:54:b4:de:af:1a"
}
