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
import yaml
import functools
import motor
import motor.motor_asyncio
import aiohttp
from dynaconf import settings as config


@functools.lru_cache(1)
def get_db():
    client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')
    # db = await client.get_database(config.get("mongo-ramble-database"))
    db = client.get_database('ramble-test')
    return db


@functools.lru_cache(3)
def get_collection(c):
    return get_db()[c]


async def load_playlist(profile, playlist):
    document = {'title': playlist, 'unix_owner': os.environ["USER"]}
    result = await get_collection("playlists").find(document)
    return await get_collection("entries").find(playlist=result["id"])


async def create_playlist(profile, name, content):
    document = {'title': name, 'unix_owner': os.environ["USER"]}
    playlist = get_collection("playlists")
    await playlist.create_index([("title", 1),
                                 ("unix_owner", 1),
                                 ("owner", 1)], **{"name": "playlists_index", "unique": True})
    result = await playlist.find_one(document)
    if result:
        result_id = result["_id"]
    else:
        result = await playlist.insert_one(document)
        result_id = result.inserted_id
    uc = [{**c, 'playlist': result_id, profile: profile} for c in content]
    entries = await get_collection("entries").insert_many(uc)
