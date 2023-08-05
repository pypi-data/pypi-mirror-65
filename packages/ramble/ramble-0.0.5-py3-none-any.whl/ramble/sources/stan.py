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

# class StanSubscription():
#     def __init__(self):
#
#     await def __aenter__(self):
#         sub = await sc.subscribe("hi", start_at='first', cb=cb)
#
#     await def __aexit__(self):
#         await self.sub.unsubscribe()

#
# def get_stan_connection():
#     self.nc = NATS()
#     await self.nc.connect(io_loop=loop)
#     self.sc = STAN()
#     await self.sc.connect("test-cluster", "client-123", nats=self.nc)

#
# async def navigate(url):
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
#             await asyncio.wait_for(future, 1, loop=loop)
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
