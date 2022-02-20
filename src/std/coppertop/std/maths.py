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


_EPS = 7.105427357601E-15      # i.e. double precision


import builtins, numpy, math

from coppertop.core import NotYetImplemented
from coppertop.pipe import *
from bones.core.types import T1, T2, pylist, N, pyfloat
from coppertop.std.transforming import array

import itertools, scipy



# **********************************************************************************************************************
# permutations (arrangements) and combinations
# perms and combs are such useful variable names so use fuller name in fn
# **********************************************************************************************************************

@coppertop(style=binary)
def permutations(xs, k):
    return itertools.permutations(xs, k) >> array

@coppertop(style=binary)
def nPermutations(n, k):
    return math.perm(n, k)

@coppertop(style=binary)
def permutationsR(xs, k):
    return itertools.product(*([xs]*k)) >> array

@coppertop(style=binary)
def nPermutationsR(n, k):
    return n ** k

@coppertop(style=binary)
def combinations(xs, k):
    return itertools.combinations(xs, k) >> array

@coppertop(style=binary)
def nCombinations(n, k):
    return math.comb(n, k)

@coppertop(style=binary)
def combinationsR(xs, k):
    return itertools.combinations_with_replacement(xs, k) >> array

@coppertop(style=binary)
def nCombinationsR(n, k):
    return scipy.special.comb(n, k, exact=True)


# **********************************************************************************************************************
# both
# **********************************************************************************************************************

@coppertop(style=binary)
def closeTo(a, b, tolerance=_EPS):
    if abs(a) < tolerance:
        return abs(b) < tolerance
    else:
        return abs(a - b) / abs(a) < tolerance

@coppertop
def within(x, a, b):
    # answers true if x is in the closed interval [a, b]
    return (a <= x) and (x <= b)


# **********************************************************************************************************************
# functions
# **********************************************************************************************************************

@coppertop
def sqrt(x):
    return numpy.sqrt(x)   # answers a nan rather than throwing


# **********************************************************************************************************************
# stats
# **********************************************************************************************************************

@coppertop(style=unary1)
def min(x):
    return builtins.min(x)

@coppertop(style=unary1)
def max(x):
    return builtins.max(x)

@coppertop(style=unary1)
def sum(x):
    return builtins.sum(x)

@coppertop(style=unary1)
def sum(x:(N**T1)[pylist][T2]) -> pyfloat:
    return builtins.sum(x._v)

@coppertop(style=unary1)
def sum(x:(N**T1)[pylist]) -> pyfloat:
    return builtins.sum(x._v)


# **********************************************************************************************************************
# rounding
# **********************************************************************************************************************

@coppertop(style=unary1)
def roundDown(x):
    # i.e. [roundDown(-2.9), roundDown(2.9,0)] == [-3, 2]
    return math.floor(x)

@coppertop(style=unary1)
def roundUp(x):
    # i.e. [roundUp(-2.9), roundUp(2.9,0)] == [-2, 3]
    return math.ceil(x)

@coppertop(style=unary1)
def roundHalfToZero(x):
    # i.e. [round(-2.5,0), round(2.5,0)] == [-2.0, 2.0]
    return round(x)

@coppertop(style=unary1)
def roundHalfFromZero(x):
    raise NotYetImplemented()

@coppertop(style=unary1)
def roundHalfToNeg(x):
    raise NotYetImplemented()

@coppertop(style=unary1)
def roundHalfToPos(x):
    raise NotYetImplemented()


