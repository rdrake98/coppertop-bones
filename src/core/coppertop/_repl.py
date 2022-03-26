# **********************************************************************************************************************
#
#                             Copyright (c) 2017-2020 David Briant. All rights reserved.
#
# This file is part of coppertop-bones.
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


from copy import copy as _copy


_list_iter_type = type(iter([]))
_numpy = None        # don't import numpy proactively


class _callFReturnX(object):
    def __init__(self, f2, pp):
        self.f2 = f2
        self.f1 = lambda x:x
        self.pp = pp
    def __rrshift__(self, lhs):   # lhs >> self
        "ENT"
        self.f2(self.f1(lhs))
        self.f1 = lambda x: x
        return lhs
    def __call__(self, f1):
        "ENT"
        self.f1 = f1
        return self
    def __lshift__(self, rhs):    # self << rhs
        "ENT"
        self.f2(self.f1(rhs))
        self.f1 = lambda x: x
        return self
    def __repr__(self):
        return self.pp


def _printRepr(x):
    print(repr(x))
RR = _callFReturnX(_printRepr, 'RR')

def _printDir(x):
    print(dir(x))
DD = _callFReturnX(_printDir, 'DD')

def _printHelp(x):
    if hasattr(x, '_doc'):
        print(x._doc)
    else:
        help(x)
HH = _callFReturnX(_printHelp, 'HH')

def _printType(x):
    print(type(x))
TT = _callFReturnX(_printType, 'TT')

def _isNdArray(x):
    global _numpy
    if type(x).__name__ != "ndarray":
        return False
    try:
        import numpy as _numpy
        return isinstance(x, _numpy.ndarray)
    except (ModuleNotFoundError, AttributeError):      # cf None.ndarray if numpy is not installed
        return False

def _printLen(x):
    if isinstance(x, _list_iter_type):
        x = list(_copy(x))
    if _isNdArray(x):
        print(x.shape)
    else:
        print(len(x))

LL = _callFReturnX(_printLen, 'LL')



if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__ + ' - done')
