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
import sys
import select
import termios
import tty

class StdinControl:
    """ Very simple PoC control to control ramble via the terminal"""

    def __init__(self):
        # we need to set tty+stdin in non buffered mode
        self.fd = sys.stdin.fileno()
        self.old_settings = termios.tcgetattr(self.fd)
        #tty.setraw(self.fd)

    def __del__(self):
        termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)

    async def tick(self):
        rs = select.select([0], [], [], 0)
        if len(rs[0]):
            l = sys.stdin.read(1)
            if l.isalpha():
                if hasattr(self, "keypress_" + l):
                    return getattr(self, "keypress_" + l)()

    def keypress_s(self):
        return {"action": "next"}

    def keypress_q(self):
        return {"action":"exit"}

    def keypress_p(self):
        return {"action":"pause"}

    def keypress_t(self):
        return {"action":"browser"}

    def keypress_y(self):
        return {"action":"bookmark"}

    def keypress_m(self):
        return {"action":"more"}

    def keypress_n(self):
        return {"action":"less"}

    def keypress_b(self):
        return {"action":"blacklist"} # via taboo list
