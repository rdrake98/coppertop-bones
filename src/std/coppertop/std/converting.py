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


import numpy, datetime, csv

from coppertop.pipe import *
from coppertop.core import Missing
from bones.core.types import pystr, pylist, pydict, T1, N, pytuple, pydict_keys, pydict_values, pydate, pyint, pyfloat, \
    npfloat, pair as tPair
from coppertop.std.structs import tvarray, tvseq, tvstruct
from coppertop.std.accessing import values
from coppertop.std.datetime import toCTimeFormat, parseDate
from coppertop.std.transforming import each
from coppertop.std.types import agg, adhoc
from bones.core.metatypes import BType




@coppertop
def fromCsv(pfn:pystr, renames:pydict, conversions:pydict, cachePath=Missing) -> agg:
    with open(pfn, mode='r') as f:
        r = csv.DictReader(f)
        d = {}
        for name in r.fieldnames:
            d[name] = list()
        for cells in r:
            for k, v in cells.items():
                d[k].append(v)
        a = agg()
        for k in d.keys():
            newk = renames.get(k, k)
            fn = conversions.get(newk, lambda l: tvarray(l, Missing))     ## we could insist the conversions return tvarray s
            a[newk] = fn(d[k])
    return a


# **********************************************************************************************************************
# to
# **********************************************************************************************************************

@coppertop(style=binary2)
def pair(a, b):
    return tvstruct(tPair[tvstruct], a=a, b=b)


# **********************************************************************************************************************
# to
# **********************************************************************************************************************

@coppertop
def to(x:pydict+pylist, t:adhoc) -> adhoc:
    return t(x)

@coppertop
def to(x, t):
    if isinstance(t, BType):
        return t(x)
    try:
        return t(x)
    except:
        raise TypeError(f'Catch all can\'t convert to {repr(t)}')

@coppertop(style=unary1)
def to(x:pydict_keys+pydict_values, t:pylist) -> pylist:
    return list(x)

@coppertop(style=unary1)
def to(x, t:pylist) -> pylist:
    return list(x)

@coppertop(style=unary1)
def to(x:adhoc, t:pydict) -> pydict:
    return dict(x._nvs())

@coppertop(style=unary1)
def to(x, t:pydict) -> pydict:
    return dict(x)

@coppertop(style=unary1)
def to(p:tPair, t:pydict) -> pydict:
    return dict(zip(p.a, p.b))

@coppertop
def to(x:pystr, t:pydate, f:pystr) -> pydate:
    return parseDate(x, toCTimeFormat(f))

@coppertop(style=unary1)
def to(x, t:pystr) -> pystr:
    return str(x)

@coppertop(style=unary1)
def to(v:T1, t:T1) -> T1:
    return v

@coppertop
def to(x, t:pyint) -> pyint:
    return int(x)

@coppertop
def to(x, t:pyfloat) -> pyfloat:
    return float(x)

@coppertop
def to(a:agg, t:tvarray) -> tvarray:
    return numpy.vstack(a >> values >> each >> (lambda n: n)).T.view(tvarray)

@coppertop
def to(x:pylist+pytuple, t:(N**T1)[tvseq], tByT) -> (N**T1)[tvseq]:
    return tvseq((N**tByT[T1])[tvseq], x)
