# **********************************************************************************************************************
#
#                             Copyright (c) 2017-2021 David Briant. All rights reserved.
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


import itertools, builtins

from coppertop.pipe import *
from coppertop.core import NotYetImplemented
from coppertop.std.structs import tvstruct
from bones.core.types import T1, T2, T3, pylist, pydict, pydict_values, pydict_keys, pytuple

from coppertop.std.types import adhoc, agg



# **********************************************************************************************************************
# chunkBy
# **********************************************************************************************************************

@coppertop
def chunkBy(a:agg, names):
    "answers a range of range of row"
    raise NotYetImplemented()


# **********************************************************************************************************************
# chunkUsing
# **********************************************************************************************************************

@coppertop(style=binary2)
def chunkUsing(iter, fn2):
    answer = []
    i0 = 0
    for i1, (a, b) in enumerate(_pairwise(iter)):
        if not fn2(a, b):
            answer += [iter[i0:i1+1]]
            i0 = i1 + 1
    answer += [iter[i0:]]
    return answer
def _pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return builtins.zip(a, b)


# **********************************************************************************************************************
# select and reject - https://en.wikipedia.org/wiki/Filter_(higher-order_function)
# **********************************************************************************************************************

@coppertop(style=binary2)
def select(d:pydict, f2) -> pydict:
    filteredKVs = []
    for k, v in d.items():
        if f2(k, v): filteredKVs.append((k,v))
    return dict(filteredKVs)

@coppertop(style=binary2)
def select(d:adhoc, f2) -> adhoc:
    filteredKVs = []
    for k, v in d._nvs():
        if f2(k, v): filteredKVs.append((k,v))
    return adhoc(filteredKVs)

@coppertop(style=binary2)
def select(pm:tvstruct, f2) -> tvstruct:
    filteredKVs = []
    for k, v in pm._nvs():
        if f2(k, v): filteredKVs.append((k,v))
    return tvstruct(pm._t, filteredKVs)

@coppertop(style=binary2)
def select(pm:(T1**T2)[tvstruct], f2) -> (T1**T2)[tvstruct]:
    filteredKVs = []
    for k, v in pm._nvs():
        if f2(k, v): filteredKVs.append((k,v))
    return tvstruct(pm._t, filteredKVs)

@coppertop(style=binary2)
def select(pm:(T1**T2)[tvstruct][T3], f2) -> (T1**T2)[tvstruct][T3]:
    filteredKVs = []
    for k, v in pm._v._nvs():
        if f2(k, v): filteredKVs.append((k,v))
    return tvstruct(pm._t, filteredKVs)

@coppertop(style=binary2)
def select(xs:pylist+pydict_keys+pydict_values, f) -> pylist:
    return [x for x in xs if f(x)]

@coppertop(style=binary2)
def select(xs:pytuple, f) -> pytuple:
    return tuple(x for x in xs if f(x))

@coppertop(style=binary2)
def select(a:agg, fn1) -> agg:
    fs = a._names()
    cols = [c for c in a._values()] #a >> values >> std.each >> anon(lambda c: c)
    # collate the offsets that fn1 answers true
    os = []
    for o in range(cols[0].shape[0]):
        r = tvstruct(zip(fs, [c[o] for c in cols]))
        if fn1(r): os.append(o)
    # create new cols from the old cols and the offsets
    newCols = [c[os] for c in cols]
    return agg(zip(fs, newCols))

@coppertop(style=binary2)
def divide(xs:pytuple, f1):        # could be called filter but that would probably confuse
    selected = []
    rejected = []
    for x in xs:
        if f1(x):
            selected.append(x)
        else:
            rejected.append(x)
    return tuple(selected), tuple(rejected)



# **********************************************************************************************************************
# groupBy
# **********************************************************************************************************************

@coppertop
def groupBy(a:agg, keys):
    "answers a collection of groups"
    raise NotYetImplemented()

@coppertop
def groupBy(a:agg, keys, directions):
    "answers a collection of groups"
    raise NotYetImplemented()


