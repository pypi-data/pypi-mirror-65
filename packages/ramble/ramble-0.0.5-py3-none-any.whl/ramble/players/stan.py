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
from nats.aio.client import Client as NATS
from stan.aio.client import Client as STAN


class StanConnection:
    def __init__(self, nats_connect_args={}):
        self.nats_connect_args = {}
        self.stan_connect_args = {}
        self.stan_client_name = "ramble"
        self.stan_cluster = "stan-cluster"

    async def __aenter__(self):
        self.nc = NATS()
        await self.nc.connect(**self.nats_connect_args)

        # Start session with NATS Streaming cluster.
        self.sc = STAN()
        await self.sc.connect(self.stan_cluster, self.stan_client, **self.stan_connect_args, nats=self.nc)

    async def __aexit__(self):
        await self.sc.close()
        await self.nc.close()


class StanPlayer(StanConnection):
    async def navigate(entry):
        await self.sc.publish(self.topic, json.encode(entry).encode('ascii'))
    #
    #     total_messages = 0
    #     future = asyncio.Future(loop=loop)
    #
    #     async def cb(msg):
    #         nonlocal future
    #         nonlocal total_messages
    #         print("Received a message (seq={}): {}".format(msg.seq, msg.data))
    #         total_messages += 1
    #         if total_messages >= 2:
    #             future.set_result(None)
    #
    #     # Subscribe to get all messages since beginning.
    #     sub = await sc.subscribe("hi", start_at='first', cb=cb)
    #     await asyncio.wait_for(future, 1, loop=loop)
    #
    #     # Stop receiving messages
    #     await sub.unsubscribe()
    #
    # if __name__ == '__main__':
    #     loop = asyncio.get_event_loop()
    #     loop.run_until_complete(run(loop))
    #     loop.close()

# class NatsPlayer:
#     def __init__(self):
#         import asyncio
#         from nats.aio.client import Client as NATS
#         from stan.aio.client import Client as STAN
#
#         async def run(loop):
#             # Use borrowed connection for NATS then mount NATS Streaming
#             # client on top.
#             self.nc = NATS()
#             await self.nc.connect(io_loop=loop)
#
#             # Start session with NATS Streaming cluster.
#             self.sc = STAN()
#             await self.sc.connect("test-cluster", "client-123", nats=self.nc)
#
#
#         async navigate(url):
#             # Synchronous Publisher, does not return until an ack
#             # has been received from NATS Streaming.
#             await sc.publish("hi", b'hello')
#
#             total_messages = 0
#             future = asyncio.Future(loop=loop)
#
#             async def cb(msg):
#                 nonlocal future
#                 nonlocal total_messages
#                 print("Received a message (seq={}): {}".format(msg.seq, msg.data))
#                 total_messages += 1
#                 if total_messages >= 2:
#                     future.set_result(None)
#
#             # Subscribe to get all messages since beginning.
#             sub = await sc.subscribe("hi", start_at='first', cb=cb)
#             await asyncio.wait_for(future, 1, loop=loop)
#
#             # Stop receiving messages
#             await sub.unsubscribe()
#
#             # Close NATS Streaming session
#             await sc.close()
#
#             # We are using a NATS borrowed connection so we need to close manually.
#             await nc.close()
#
#         if __name__ == '__main__':
#             loop = asyncio.get_event_loop()
#             loop.run_until_complete(run(loop))
#             loop.close()
