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


import builtins
from coppertop.pipe import *
from coppertop.pipe import MultiFn
from bones.core.types import T1, T2, T3, T4, T5, T6, pybool, pydict
from coppertop.std.maths import closeTo
from coppertop.std.structs import tvarray, tvstruct
from coppertop.std.types import adhoc

_EPS = 7.105427357601E-15      # i.e. double precision



@coppertop(style=binary)
def assertEquals(actual, expected, suppressMsg=False, keepWS=False, returnResult=False, tolerance=_EPS):
    if keepWS:
        act = actual
        exp = expected
    else:
        act = actual.replace(" ", "").replace("\n", "") if isinstance(actual, (str,)) else actual
        exp = expected.replace(" ", "").replace("\n", "") if isinstance(expected, (str,)) else expected
    if isinstance(act, (int, float)) and isinstance(exp, (int, float)):
        equal = act >> closeTo(_, _, tolerance=tolerance) >> exp
    else:
        equal = act == exp
    if returnResult:
        return equal
    else:
        if not equal:
            if suppressMsg:
                raise AssertionError()
            else:
                if isinstance(actual, (str,)):
                    actual = '"' + actual + '"'
                if isinstance(expected, (str,)):
                    expected = '"' + expected + '"'
                raise AssertionError(f'Expected {expected} but got {actual}')
        else:
            return None

@coppertop(style=ternary)
def check(actual, fn, expected):
    fnName = fn.name if hasattr(fn, 'name') else (fn.dispatcher.name if isinstance(fn, MultiFn) else '')
    with context(showFullType=True):
        if fn is builtins.type or fnName == 'typeOf':
            res = fn(actual)
            assert res == expected, f'Expected type <{expected}> but got type <{fn(actual)}>'
        else:
            res = fn(actual, expected)
            assert res == True, f'\nChecking fn \'{fn}\' failed the following:\nactual:   {actual}\nexpected: {expected}'
    return actual

@coppertop(style=binary2, supressDispatcherQuery=True)
def equal(a, b) -> pybool:
    return a == b

@coppertop(style=binary2, supressDispatcherQuery=True)
def equal(a:tvarray, b:tvarray) -> pybool:
    return bool((a == b).all())

@coppertop(style=binary2)
def different(a, b) -> pybool:
    return a != b

@coppertop(style=binary2)
def different(a:tvarray, b:tvarray) -> pybool:
    return bool((a != b).any())

@coppertop(style=binary2)
def sameLen(a, b):
    return len(a) == len(b)

@coppertop(style=binary2)
def sameShape(a, b):
    return a.shape == b.shape


# **********************************************************************************************************************
# sameNames
# **********************************************************************************************************************

@coppertop(style=binary2)
def sameKeys(a:pydict, b:pydict) -> pybool:
    return a.keys() == b.keys()

@coppertop(style=binary2)
def sameNames(a:adhoc, b:adhoc) -> pybool:
    return a._names() == b._names()

# some adhoc are defined like this (num ** account)[tvstruct]["positions"]
@coppertop(style=binary2)
def sameNames(a:(T1 ** T2)[tvstruct][T3], b:(T4 ** T2)[tvstruct][T5]) -> pybool:
    return a._names() == b._names()


@coppertop(style=binary2)
def sameNames(a:(T1 ** T2)[tvstruct][T3], b:(T5 ** T4)[tvstruct][T6]) -> pybool:
    assert a._names() != b._names()
    return False

# many structs should be typed (BTStruct)[tvstruct] and possibly (BTStruct)[tvstruct][T]   e.g. xy in pixels and xy in data

# if we can figure how to divide up the dispatch space (or even indicate it) this would be cool
# the total space below is T1[BTStruct][tvstruct] * T2[BTStruct][tvstruct] with
# T1[BTStruct][tvstruct] * T1[BTStruct][tvstruct] as a subspace / set
# can dispatch to the total space and then to the specific subset - with one as default
# @coppertop(style=binary2)
# def sameNames(a:T1[BTStruct][tvstruct], b:T2[BTStruct][tvstruct]) -> bool:
#     assert a._names() != b._names()
#     return False
#
# #@coppertop(style=binary2, memberOf=(T1[BTStruct][tvstruct]) * (T2[BTStruct][tvstruct])))
# @coppertop(style=binary2)
# def sameNames(a:T1[BTStruct][tvstruct], b:T1[BTStruct][tvstruct]) -> bool:
#     assert a._names() == b._names()
#     return True

# any should really be unhandles or alt or others or not default


