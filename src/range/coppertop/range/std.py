# **********************************************************************************************************************
#
#                             Copyright (c) 2019-2020 David Briant. All rights reserved.
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

from coppertop.core import NotYetImplemented
from coppertop.pipe import *
from ._range import EachFR, ChainAsSingleFR, UntilFR, IInputRange, IRandomAccessInfinite
from bones.core.types import pylist


@coppertop
def rZip(r):
    raise NotYetImplemented()

@coppertop
def rInject(r, seed, f):
    raise NotYetImplemented()

@coppertop
def rFilter(r, f):
    raise NotYetImplemented()

@coppertop
def rTakeBack(r, n):
    raise NotYetImplemented()

@coppertop
def rDropBack(r, n):
    raise NotYetImplemented()

@coppertop
def rFind(r, value):
    while not r.empty:
        if r.front == value:
            break
        r.popFront()
    return r

@coppertop
def put(r, x):
    return r.put(x)

@coppertop(style=unary1)
def front(r):
    return r.front

@coppertop(style=unary1)
def back(r):
    return r.back

@coppertop(style=unary1)
def empty(r):
    return r.empty

@coppertop(style=unary1)
def popFront(r):
    r.popFront()
    return r

@coppertop(style=unary1)
def popBack(r):
    r.popBack()
    return r


rEach = coppertop(style=binary2, newName='rEach')(EachFR)
rChain = coppertop(style=unary1, newName='rChain')(ChainAsSingleFR)
rUntil = coppertop(style=binary2, newName='rUntil')(UntilFR)


@coppertop
def replaceWith(haystack, needle, replacement):
    return haystack >> rEach >> (lambda e: replacement if e == needle else e)

@coppertop(style=binary2)
def pushAllTo(inR, outR):
    while not inR.empty:
        outR.put(inR.front)
        inR.popFront()
    return outR

def _materialise(r) -> pylist:
    answer = list()
    while not r.empty:
        e = r.front
        if isinstance(e, IInputRange) and not isinstance(e, IRandomAccessInfinite):
            answer.append(_materialise(e))
            if not r.empty:  # the sub range may exhaust this range
                r.popFront()
        else:
            answer.append(e)
            r.popFront()
    return answer

materialise = coppertop(style=unary1, newName='materialise')(_materialise)
