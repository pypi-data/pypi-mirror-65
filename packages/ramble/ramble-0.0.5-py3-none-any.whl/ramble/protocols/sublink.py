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
import bs4
import random
import aiohttp
import re
import urllib
import urllib.parse


def lstrip(url):
    while len(url) and url[0] == "/":
        url = url[1:]
    return url


def rstrip(url):
    while len(url) and url[-1] == "/":
        url = url[:-1]
    return url


class SUBLINK:
    PATTERN = "sublink://"

    @classmethod
    async def update(cls, entry, match):
        match = entry["url"][len(cls.PATTERN):]

        def make_lambda(turl):
            async def res():
                url = turl
                async with aiohttp.client.ClientSession() as c:
                    content = await (await c.get(url)).read()

                links = bs4.BeautifulSoup(content, features='lxml').find_all('a')
                # filter according to link pattern
                links = [x["href"] for x in links if "href" in x.attrs and x["href"]]
                url = rstrip(url)
                pu = urllib.parse.urlparse(url)
                links = [
                    (x if "://" in x else ((pu.scheme + "://" + pu.netloc + "/" + lstrip(x))) if x[0] == "/" else url+"/"+x)
                    for x in links
                ]
                links = [x for x in links if re.match("^" + entry["sublink_pattern"], x)]
                return random.choice(links)

            return res

        entry["url"] = make_lambda(match)
        return entry


PROTOCOL = SUBLINK
