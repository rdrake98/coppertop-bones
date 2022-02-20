# **********************************************************************************************************************
#
#                             Copyright (c) 2020-2021 David Briant. All rights reserved.
#
# This file is part of bones.
#
# bones is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# bones is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License along with Foobar. If not, see
# <https://www.gnu.org/licenses/>.
#
# **********************************************************************************************************************

import sys
if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)


import os, os.path, json
from io import TextIOWrapper
from coppertop.pipe import *
from bones.core.types import pystr, pylist
from coppertop.std.text import strip
from coppertop.std.transforming import each

getCwd = coppertop(style=unary1, newName='getCwd')(os.getcwd)
isFile = coppertop(style=unary1, newName='isFile')(os.path.isfile)
isDir = coppertop(style=unary1, newName='isDir')(os.path.isdir)
dirEntries = coppertop(style=unary1, newName='dirEntries')(os.listdir)

@coppertop(style=binary2)
def joinPath(a, b):
    return os.path.join(a, *(b if isinstance(b, (list, tuple)) else [b]))

@coppertop
def readlines(f:TextIOWrapper) -> pylist:
    return f.readlines()

@coppertop
def linesOf(pfn:pystr):
    with open(pfn) as f:
        return f >> readlines >> each >> strip(_,'\\n')

@coppertop(style=binary)
def copyTo(src, dest):
    raise NotImplementedError()

@coppertop
def readJson(pfn:pystr):
    with open(pfn) as f:
        return json.load(f)

@coppertop
def readJson(f:TextIOWrapper):
    return json.load(f)

