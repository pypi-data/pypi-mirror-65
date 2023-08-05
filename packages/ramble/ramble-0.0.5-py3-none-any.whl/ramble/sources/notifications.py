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
# simply waterfall between different sources hence giving prioritiy to one source of another
# if the source is empty go to the next

def _pl_to_entry(pl):
    res = pl.split("/")
    if len(res) != 2:
        return None
    return res


async def query_content(max_rec=10, profile, playlist, **kwargs):
    """
    Notifications will try different query on different sources.
    It works like this :

    profile: list of sources separated by:
    file#file
    api#api#file


    playlist: base64 json list of dict with parameters for the sources or a srting beginning with #
    containinh a list of profile:playlist seprated by #
    """
    if playlist.startswith("#"):
        playlists = [x for x in [_pl_to_entry(pl) for pl in playlist[1:].split("#")] if x is not None]
    else:
        playlists = json.loads(base64.b64decode(playlist))

    for source, playlist in zip(profile.split("#"), playlists):
        current_module = load_module(current_module_name)
        if hasattr(current_module, "query_content"):
            res = await current_module.query_content(max_rec=max_rec - 1, **kwargs)
            return res

    return None
