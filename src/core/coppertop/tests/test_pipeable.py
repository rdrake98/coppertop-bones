# **********************************************************************************************************************
#
#                             Copyright (c) 2021 David Briant. All rights reserved.
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


from coppertop.pipe import *
from coppertop.core import *
from coppertop.testing import assertRaises
from bones.core.metatypes import BTAtom
from dm.std import check, equal, fitsWithin, each
from dm.std import tvarray
from coppertop.tests.take1 import _take
from coppertop.tests.take2 import _take
from bones.core.types import pyint, pylist

mat = BTAtom.ensure("mat2")
vec = BTAtom.ensure("vec2")


@coppertop(style=binary2)
def mmul(A:mat, B:vec) -> vec:
    answer = A @ B | vec
    return answer


def test_mmul():
    a = tvarray(mat, [[1, 2], [3, 4]])
    b = tvarray(vec, [1, 2])
    res = a >> mmul >> b
    res >> check >> typeOf >> vec


@coppertop(style=rau)
def unpack(f):
    return lambda xy: f(xy[0],xy[1])


def testTake():
    [1, 2, 3] >> _take >> 2 >> check >> equal >> [1, 2]
    [1, 2, 3] >> _take >> -2 >> check >> equal >> [2, 3]
    [1, 2, 3] >> _take >> (..., ...) >> check >> equal >> [1, 2, 3]
    [1, 2, 3] >> _take >> (1, ...) >> check >> equal >> [2, 3]
    [1, 2, 3] >> _take >> (..., 2) >> check >> equal >> [1, 2]
    [1, 2, 3] >> _take >> (0, 2) >> check >> equal >> [1, 2]

    {"a":1, "b":2, "c":3} >> _take >> "a" >> check >> equal >> {"a":1}
    {"a":1, "b":2, "c":3} >> _take >> ["a", "b"] >> check >> equal >> {"a":1, "b":2}


def testTypeOf():
    1 >> check >> typeOf >> pyint
    1 >> typeOf >> check >> fitsWithin >> pyint


def testDoc():
    _take(pylist, pyint).d.__doc__ >> check >> equal >> 'hello'
    _take(pylist, pylist).d.__doc__ >> check >> equal >> 'there'


def test_rau():
    p1 = ((1, 1), (2, 2), (3, 3)) >> each
    with assertRaises(NotYetImplemented):
        res = p1 >> unpack >> (lambda x, y: x + y)
        res >> check >> equal >> [2, 4, 6]


def main():
    testTake()
    testTypeOf()
    testDoc()
    test_mmul()
    test_rau()


if __name__ == '__main__':
    main()
    print('pass')

