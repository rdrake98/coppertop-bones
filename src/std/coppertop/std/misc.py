# **********************************************************************************************************************
#
#                             Copyright (c) 2017-2020 David Briant. All rights reserved.
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
from coppertop.pipe import typeOf
from bones.core.types import tv, T
from bones.core.metatypes import cacheAndUpdate, fitsWithin as _fitsWithin
from coppertop.std.transforming import inject
from coppertop.std.types import TBT


dict_keys = type({}.keys())
dict_values = type({}.values())



@coppertop
def box(v) -> TBT:
    return tv(TBT, v)

@coppertop
def box(v, t:T) -> T:
    return tv(t, v)

@coppertop
def getAttr(x, name):
    return getattr(x, name)

@coppertop
def compose(x, fs):
    return fs >> inject(_, x, _) >> (lambda x, f: f(x))

def not_(b):
    return False if b else True
Not = coppertop(style=unary1, newName='Not')(not_)
not_ = coppertop(style=unary1, newName='not_')(not_)

repr = coppertop(style=unary1, newName='repr')(builtins.repr)

@coppertop(style=unary1)
def _t(x):
    return x._t

@coppertop(style=unary1)
def _v(x):
    return x._v

@coppertop(style=binary2, supressDispatcherQuery=True)
def fitsWithin(a, b):
    doesFit, tByT, distances = cacheAndUpdate(_fitsWithin(a, b), {})
    return doesFit

@coppertop(style=binary2, supressDispatcherQuery=True)
def doesNotFitWithin(a, b):
    return a >> fitsWithin >> b >> not_


