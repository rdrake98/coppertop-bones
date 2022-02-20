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


from coppertop.pipe import *
from coppertop.core import NotYetImplemented
from coppertop.std.structs import tvstruct, tvseq

from coppertop.std.types import adhoc, agg
from bones.core.types import pystr, N, pylist, T1, pytuple, pydict
from coppertop.std.misc import fitsWithin



# **********************************************************************************************************************
# interleave
# **********************************************************************************************************************

@coppertop(style=binary2)
def interleave(xs:pylist+pytuple, b) -> pylist:
    answer = xs[0]
    for x in xs[1:]:
        answer = answer >> join >> b >> join >> x
    return answer

@coppertop(style=binary2)
def interleave(a:(N**T1)[tvseq], b: T1) -> (N**T1)[tvseq]:
    raise NotYetImplemented()

@coppertop(style=binary2)
def interleave(a:(N**T1)[tvseq], b: (N**T1)[tvseq]) -> (N**T1)[tvseq]:
    raise NotYetImplemented()

@coppertop(style=binary2)
def interleave(xs:N**pystr, sep:pystr) -> pystr:
    # ['hello', 'world'] >> joinAll(_,' ')
    return sep.join(xs)

@coppertop(style=binary2)
def interleave(xs:pylist+pytuple, sep:pystr) -> pystr:
    return sep.join(xs)


# **********************************************************************************************************************
# join
# **********************************************************************************************************************

@coppertop(style=binary2)
def join(xs:pylist, ys:pylist) -> pylist:
    return xs + ys

@coppertop(style=binary2)
def join(xs:(N**T1)[tvseq], ys:(N**T1)[tvseq], tByT) -> (N**T1)[tvseq]:
    return tvseq((N**(tByT[T1]))[tvseq], xs.data + ys.data)

@coppertop(style=binary2)
def join(s1:pystr, s2:pystr) -> pystr:
    return s1 + s2

@coppertop(style=binary2)
def join(d1:pydict, d2:pydict) -> pydict:
    answer = dict(d1)
    for k, v in d2.items():
        if k in answer:
            raise KeyError(f'{k} already exists in d1 - use underride or override to merge (rather than join) two pydicts')
        answer[k] = v
    return answer


# **********************************************************************************************************************
# joinAll
# **********************************************************************************************************************

@coppertop
def joinAll(xs:N**pystr) -> pystr:
    return ''.join(xs)

@coppertop
def joinAll(xs:pylist+pytuple) -> pystr + ((N**T1)[tvseq]) + pylist + pytuple:
    # could be a list of strings or a list of (N**T1) & tvseq
    # answer a string if no elements
    if not xs:
        return ''
    typeOfFirst = typeOf(xs[0])
    if typeOfFirst >> fitsWithin >> pystr:
        return ''.join(xs)
    elif typeOfFirst >> fitsWithin >> (N**T1)[tvseq]:
        elements = []
        for x in xs:
            # could check the type of each list using metatypes.fitsWithin
            elements.extend(x.data)
        return tvseq(xs[0]._t, elements)
    elif typeOfFirst >> fitsWithin >> pylist:
        answer = []
        for e in xs:
            answer += e
        return answer
    elif typeOfFirst >> fitsWithin >> pytuple:
        answer = ()
        for e in xs:
            answer += e
        return answer


# **********************************************************************************************************************
# merge
# **********************************************************************************************************************


# **********************************************************************************************************************
# override
# **********************************************************************************************************************

@coppertop(style=binary2)
def override(a:pydict, b:pydict) -> pydict:
    answer = dict(a)
    answer.update(b)
    return answer

@coppertop(style=binary2)
def override(a:pydict, b:tvstruct) -> pydict:
    answer = dict(a)
    answer.update(b._nvs())
    return answer

@coppertop(style=binary2)
def override(a:adhoc, b:adhoc) -> adhoc:
    answer = adhoc(a)
    answer._update(b._nvs())
    return answer

@coppertop(style=binary2)
def override(a:tvstruct, b:tvstruct) -> tvstruct:
    answer = tvstruct(a)
    answer._update(b._nvs())
    return answer

@coppertop(style=binary2)
def override(a:tvstruct, b:pydict) -> tvstruct:
    answer = tvstruct(a)
    answer._update(b)
    return answer


# **********************************************************************************************************************
# underride
# **********************************************************************************************************************

@coppertop(style=binary2)
def underride(a:tvstruct, b:tvstruct) -> tvstruct:
    answer = tvstruct(a)
    for k, v in b._nvs():
        if k not in answer:
            answer[k] = v
        # answer._setdefault(k, v)      # this doesn't respect insertion order!!
    return answer

@coppertop(style=binary2)
def underride(a:tvstruct, b:pydict) -> tvstruct:
    answer = tvstruct(a)
    for k, v in b.items():
        if k not in answer:
            answer[k] = v
        # answer._setdefault(k, v)      # this doesn't respect insertion order!!
    return answer


# **********************************************************************************************************************
# agg joins
# **********************************************************************************************************************

@coppertop(style=binary2)
def lj(agg1:agg, agg2:agg):
    raise NotYetImplemented()


@coppertop(style=binary2)
def rj(agg1:agg, agg2:agg):
    raise NotYetImplemented()


@coppertop(style=binary2)
def ij(agg1:agg, agg2:agg):
    raise NotYetImplemented()


@coppertop(style=binary2)
def oj(agg1:agg, agg2:agg):
    raise NotYetImplemented()


@coppertop(style=binary2)
def uj(agg1:agg, agg2:agg):
    raise NotYetImplemented()


@coppertop(style=binary2)
def aj(agg1:agg, agg2:agg):
    raise NotYetImplemented()


