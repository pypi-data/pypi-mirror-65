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
import copy
import logging
import os
import random
import re
import sys
import time
import importlib

from dynaconf import settings as config
from ramble.ramble_contents import load_enriched_profile
from ramble.utils import timestamp

"""
The goal of this file is to implement the logic for finding the next URL:
   1. in a local profile/playlist
   2. using a remote source (and eventually recursing as necessary) files -> api -> link_to_mail
"""


async def load_urls(current_playlist, profile, source_module):
    contents = await load_enriched_profile(profile, source_module)
    urls = contents["playlists"][current_playlist]
    return contents, urls


async def query_content(max_rec=None, retries=10, **kwargs):
    res = None
    delay = 0.1
    while not res:
        res = await _query_content(max_rec=max_rec, **kwargs)
        if not res:
            if retries > 0:
                await asyncio.sleep(delay)
                delay *= 1.5
            else:
                return None
            retries -= 1
    return res


def parse_ramble_url(url):
    res = re.match(
        "(ramble|kiosk)://((?P<profile>[A-Za-z0-9_-]+):)?([.]?(?P<playlist>[A-Za-z0-9_-]+))?(@(?P<source>[A-Za-z0-9_-]+))?(/(?P<args>.+))?",
        url,
    )
    if not res:
        return None
    return res.groupdict()


def dict_rec_update(d1, d2):
    res = {
        k: (v if k not in d2 else (
            dict_rec_update(v, d2[k]) if isinstance(v, dict) and isinstance(d2[k], dict) else d2[k])
            )
        for k, v in d1.items()
    }
    
    for k, v in d2.items():
        if k not in res:
            res[k] = v
    
    return res


async def _query_content(max_rec=None, current_context={}, **kwargs):
    """Find a content in a playlist

    Currently ramble URL are meant to be formated:
       ramble://[profile]:[playlist][@source]/[:arg]

    ramble://@bookmarks/
    ramble://default:videos@files/
    ramble://videos@files/
    ramble://@notifications/@xxxx;+@£lfldfdf
    ramble://@youtube/UVDFDKFDS?
    ramble://@mongo/
    ramble://@taboo/@youtube/?list=lflksdflsdf
    """
    max_rec = max_rec or 10

    current_module, current_module_name, current_playlist, current_profile = await get_playlist_parameters(kwargs)
    if hasattr(current_module, "query_content"):
        return await current_module.query_content(max_rec=max_rec - 1, **kwargs)

    contents, urls = await load_urls(current_playlist, current_profile, current_module)
    logging.debug("playlist %s, length = %d", current_playlist, len(urls))

    rec = 0
    path = ""
    current_context = current_context or {}
    while isinstance(urls, list):
        path += f"{current_playlist} "
        schedule_context = current_context.copy()
        schedule_context.update(get_context())
        possible_urls = list(
            filter(lambda u: (("schedule" not in u) or schedulable(u["schedule"], schedule_context)), urls))
        if not len(possible_urls):
            logging.debug("Nothing is schedulable in current playlist %s", current_playlist)
            return None
        # -------------------------------------------------------------------------------------------------
        entry = draw_from_playlist(current_playlist, possible_urls)
        urls = url = entry["url"]
        if entry.get("push_context"):
            current_context = dict_rec_update(current_context, entry["push_context"])

        # -------------------------------------------------------------------------------------------------
        # allow switch to another playlist
        if isinstance(url, str) and url.startswith("ramble://"):
            kwargs.update({k: v for k, v in parse_ramble_url(url).items() if v is not None})
            current_module_name = kwargs.get("source", current_module_name)
            current_profile = kwargs.get("profile", current_profile)
            current_playlist = kwargs.get("playlist", current_playlist)

            current_module = load_module(current_module_name)
            if hasattr(current_module, "query_content"):
                return current_module.query_content(max_rec=max_rec - 1, **kwargs)
            contents, urls =  await load_urls(current_playlist, current_profile, current_module)

        rec += 1
        if rec >= max_rec:
            raise Exception("Deep recursion")

    path += f": {current_playlist} "
    entry = copy.copy(entry)

    if callable(entry["url"]):
        entry["url"] = await entry["url"]()
    url = entry["url"]
    entry["duration"] = entry.get("duration", (
        config.get("default_static_duration") if not "youtube.com" in url else config.get("default_video_duration")))

    logging.debug(path + "-> %s  (%s)\n" % (entry["url"], entry["duration"]))
    logging.info("Navigating to " + entry["url"] + " for " + str(entry["duration"]) + "seconds")
    return entry


async def get_playlist_parameters(kwargs):
    if "url" in kwargs:
        kwargs.update({k: v for k, v in parse_ramble_url(kwargs.pop("url")).items() if v is not None})
    current_module_name = kwargs.get("source", config.get("source", "file"))
    current_profile = kwargs.get("profile", config["profile"])
    current_playlist = kwargs.get("playlist", config["playlist"])
    current_module = load_module(current_module_name)
    return current_module, current_module_name, current_playlist, current_profile


def load_module(current_module_name):
    assert current_module_name.isalnum() and current_module_name[0].isalpha()
    module = importlib.import_module("ramble.sources." + current_module_name)
    return module


def draw_from_playlist(current_playlist, possible_urls):
    total_weight = sum([int(u.get("weight", 1)) for u in possible_urls])
    x = random.randint(0, total_weight - 1)
    i = -1
    while x >= 0:
        i += 1
        x -= int(possible_urls[i].get("weight", 1))
    u = possible_urls[i]
    return u


def get_context():
    """Provide a context to determine if something is schedulable or not"""
    un = os.uname()
    extra_context = {}
    if config.get("schedule_context_command"):
        p = subprocess.Popen(ramble.get("schedule_context_command"), shell=True, stdout=subprocess.PIPE)
        o, e = p.communicate()
        extra_context = json.loads(o.read())

    return {
        "ts": ",".join(map(str, timestamp())),
        "sysname": un.sysname,
        "env": os.environ,
        "nodename": un.nodename,
        # "":
        # "physical_location":
        # "network_location"
        **extra_context
    }


def schedulable(schedule, context):
    """
    Check whether something is schedulable or not based on current context.
    Currently this only returns a boolean - a more sophisticated version could adjust weights.
    """
    if isinstance(schedule, dict):
        for k, v in schedule.items():
            if k in context:
                if k == "env":  # check environment variables
                    for ek, ev in k:
                        if ek not in context["env"] or context["env"][ek] != ev:
                            return False
                else:
                    if not re.match(v, str(context[k])):
                        return False
            return True
    else:
        ts = ",".join(map(str, timestamp()))
        return re.match(schedule, ts)
