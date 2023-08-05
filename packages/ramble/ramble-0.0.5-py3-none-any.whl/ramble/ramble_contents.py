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
import random
import re
import urllib
import logging

import functools
import feedparser
import aiohttp


async def load_enriched_profile(profile, source_module):
    return await enrich_profile(await source_module.load_profile(profile))


async def enrich_profile(profile_content):
    for pl, plc in profile_content["playlists"].items():
        all_urls = await enrich_playlist(plc)
        profile_content["playlists"][pl] = all_urls
    return profile_content


async def enrich_playlist(plc):
    all_urls = [(await enrich_entry(e)) for e in plc]
    return all_urls


@functools.lru_cache(1)
def get_protocols():
    res = {}

    import ramble.protocols.youtube as yt
    res[yt.PROTOCOL.PATTERN] = yt.PROTOCOL.update

    import ramble.protocols.rss as rss
    res[rss.PROTOCOL.PATTERN] = rss.PROTOCOL.update

    import ramble.protocols.sublink as sl
    res[sl.PROTOCOL.PATTERN] = sl.PROTOCOL.update

    return res


async def enrich_entry(x):
    assert isinstance(x, dict)
    protocols = get_protocols()
    if isinstance(x["url"], str):
        for p in protocols.items():
            r = re.match("^" + p[0], x["url"])
            if r:
                return await p[1](x, r)
    return x


# async def enrich_entry_leg(x):
#     assert isinstance(x, dict)
#     if isinstance(x["url"], str) and x["url"].startswith("youtube://"):
#         r = re.match("youtube://(?P<feed>[^?/]+)[/]?([?](?P<args>.*))?", x["url"])
#         if r:
#             r = r.groupdict()
#
#             def make_lambda(r):
#                 async def res():
#                     return await random_from_youtube_feed(
#                         r["feed"], **({k: v[0] for k, v in urllib.parse.parse_qs(r["args"] or "").items()})
#                     )
#
#                 return res
#
#             x["url"] = make_lambda(r)
#     elif isinstance(x["url"], str) and x["url"].startswith("rss://"):
#         def make_lambda(xu):
#             async def res():
#                 return await random_from_rss(xu)
#
#             return res
#
#         x["url"] = make_lambda(x["url"][6:])
#     return x


def tuple_entry_to_dict_entry(e):
    assert isinstance(e, (tuple, list))
    return {
        "weight": int(e[0]),
        "schedule": e[1],
        "duration": int(e[2]),
        "url": e[3],
    }


def youtube_feed(cid, **kwargs):
    feed = "http://www.youtube.com/feeds/videos.xml?channel_id=" + cid
    if "list" in kwargs:
        # feed = feed + "&list=" + kwargs["list"]
        feed = "http://www.youtube.com/feeds/videos.xml?playlist_id=" + kwargs["list"]
    return feed


async def load_rss(feed):
    async with aiohttp.client.ClientSession() as c:
        feed_content = await (await c.get(feed)).read()

    res = feedparser.parse(feed_content)
    return res


async def random_from_youtube_feed(cid, **kwargs):
    f = await load_rss(youtube_feed(cid, **kwargs))
    logging.info("yt %r len %d", cid, len(f.entries))
    if not len(f.entries):
        raise Exception(str("youtube feed empty - yt:") + cid)
    return "https://www.youtube.com/embed/" + random.choice(f.entries)["yt_videoid"] + "?autoplay=1"


async def random_from_rss(feed_url):
    f = await load_rss(feed_url)
    logging.info("fu %r len %d", feed_url, len(f.entries))
    if not len(f.entries):
        raise Exception(str("empty rss:") + feed_url)
    return random.choice(f.entries)["link"]
