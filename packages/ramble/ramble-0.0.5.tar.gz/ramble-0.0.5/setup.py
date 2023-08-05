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
import json
import os
import subprocess
import sys

from setuptools import find_namespace_packages
from setuptools import setup

try:
    # pip < v10
    from pip.req import parse_requirements
except ImportError:
    # pip >= v10
    from pip._internal.req import parse_requirements

base_path = os.path.dirname(__file__)
o, e = subprocess.Popen(
    ["/bin/bash", "-c", "git describe --tags &> /dev/null  && ./semtag getlast || ./semtag getcurrent"],
    stdout=subprocess.PIPE
).communicate()
version = o.decode('ascii')[1:].strip("\n").replace("+","-")


def all_subpackages(*l):
    res = []
    for x in l:
        if os.path.exists(os.path.join(x.replace(".", "/"), "__init__.py")):
            res.append(x)
        res += list(find_namespace_packages(include=[x + ".*"]))
    return res


def get_requirements():
    req_path = os.path.join(base_path, "requirements.txt")
    if os.path.exists(req_path):
        reqs = parse_requirements(req_path, session=False)
        res = [str(ir.req) for ir in reqs]
    else:
        res = []
    return res


setup(
    name="ramble",
    version=version,
    packages=all_subpackages("ramble"),
    package_data={"ramble": ["settings.yml"],},
    zip_safe=False,
    install_requires=(get_requirements()),
    description="A program for playing  content automatically according to time, location and place",
    entry_points={"console_scripts": ["ramble = ramble.ramble:main"]},
    license="BSD",
    classifiers=[
        "Natural Language :: English",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
    ],
)
