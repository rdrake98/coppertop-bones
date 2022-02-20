# **********************************************************************************************************************
#
#                             Copyright (c) 2021-2022 David Briant. All rights reserved.
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

from coppertop.core import PP as _PP, Void as _Void
from coppertop.pipe import *
from coppertop.pipe import NO_TYPE
from bones.core.metatypes import BTAtom
from bones.core.types import pystr, N, pyint, pylist, pyset, pydict_keys, pydict_values, T1, T2, pytuple, tv
from coppertop.std import count, equal, tvseq, each, max, pad
from dm.utils import formatStruct
from dm.pmf import PMF, L

from coppertop.std.types import void


display_table = (N**pystr)[tvseq][BTAtom.ensure('table')].setCoercer(tvseq)

Void = tv(void, _Void)  # move to std and the singleton should have type void

@coppertop
def PP(t:display_table) -> display_table:
    for string in t:
        string >> PP
    return t

@coppertop(style=binary)
def hjoin(a:display_table, b:display_table, options={}) -> display_table:
    assert (a >> count) == (b >> count)
    answer = tvseq(display_table, [])
    for i in range(len(a)):
        answer.append(a[i] + options.get('sep', '') + b[i])
    return answer

@coppertop(style=binary)
def join(a:display_table, b:display_table, options={}) -> display_table:
    return tvseq(display_table, a.data + b.data) >> ljust

@coppertop
def ljust(rows:display_table, width:pyint=0, fillchar:pystr=' ') -> display_table:
    maxLength = rows >> each >> count >> max
    return rows >> each >> pad(_, left=max((maxLength, width)), pad=fillchar) | display_table

@coppertop(style=binary2)
def aside(x:T1, fn:T1^T2) -> T1:
    fn(x)
    return x

@coppertop(style=binary2)
def aside(x:pylist, fn) -> pylist:
    fn(x)
    return x

@coppertop(style=binary2)
def countIf(xs, fn):
    c = 0
    for x in xs:
        c += fn(x)
    return c

@coppertop(style=binary2)
def minus(a:pyset, b:pyset+pylist+pydict_keys+pydict_values) -> pyset:
    return a.difference(b)

@coppertop(style=binary2)
def minus(a:pylist+pytuple, b:pyset+pylist+pydict_keys+pydict_values) -> pyset:
    return set(a).difference(b)

@coppertop
def only(a:pyset):
    return list(a)[0]

@coppertop(style=binary2)
def append(rows:display_table, row:pystr) -> display_table:
    rows.append(row)
    return rows >> ljust

formatPmf = formatStruct(_, 'PMF', '.3f', '.3f', ', ')
formatL = formatStruct(_, 'L', '.3f', '.3f', ', ')

@coppertop
def PP(x):
    return x >> _PP

@coppertop
def PP(x, f):
    f(x) >> _PP
    return x

@coppertop
def PP(x:L):
    x >> formatL >> _PP
    return x

@coppertop
def PP(x:PMF):
    x >> formatPmf >> _PP
    return x

