# **********************************************************************************************************************
#
#                             Copyright (c) 2021 David Briant. All rights reserved.
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

from coppertop.pipe import *
from bones.core.types import pylist, pytuple, pyint

ellipsis = type(...)


sys._BREAK = True  # hasattr(sys, '_BREAK') and sys._BREAK


@coppertop(style=binary2)
def _take(xs:pylist, n:pyint) -> pylist:
    '''hello'''
    if n >= 0:
        return xs[:n]
    else:
        return xs[len(xs) + n:]

@coppertop(style=binary2)
def _take(xs: pylist, os: pylist) -> pylist:
    '''there'''
    return [xs[o] for o in os]

@coppertop(style=binary2)
def _take(xs:pylist, ss:pytuple) -> pylist:
    s1, s2 = ss
    if s1 is Ellipsis:
        if s2 is Ellipsis:
            return xs
        else:
            return xs[:s2]
    else:
        if s2 is Ellipsis:
            return xs[s1:]
        else:
            return xs[s1:s2]
