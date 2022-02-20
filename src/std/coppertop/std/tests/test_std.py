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



import operator
from coppertop.pipe import *
from coppertop.std import inject, each, eachAsArgs, check, equal, to, shape, adhoc, drop, at, keys, sort, tvseq, \
    typeOf
from coppertop.std.linalg import matrix, tvarray
from bones.core.types import offset, index, N, count, pystr, pydict, pylist


def test_inject():
    [1,2,3] >> inject(_,0,_) >> (lambda a,b: a + b) >> check >> equal >> 6


def test_stuff():

    @coppertop
    def squareIt(x):
        return x * x

    @coppertop(style=binary2)
    def add(x, y):
        return x + y

    [1,2,3] >> each >> squareIt >> inject(_, 0, _) >> add >> check >> equal >> 14

    [[1,2], [2,3], [3,4]] >> eachAsArgs >> add >> check >> equal >> [3, 5, 7]
    [[1, 2], [2, 3], [3, 4]] >> eachAsArgs >> operator.add >> check >> equal >> [3, 5, 7]


def test_misc():
    [[1, 2], [3, 5]] >> to(_,matrix[tvarray]) >> shape >> check >> equal >> (2,2)
    adhoc(a=1,b=2,c=3) >> drop >> ['a', 'b'] >> to(_,pydict) >> check >> equal >> dict(c=3)
    [dict(a=1)] >> at(_, 0) >> at(_, "a") >> check >> equal >> 1
    dict(b=1, a=2) >> keys >> to(_, pylist) >> sort

def test_at():
    [1,2,3] >> at(_, 0) >> check >> equal >> 1
    [1,2,3] >> at(_, 0 | offset) >> check >> equal >> 1
    [1,2,3] >> at(_, 1 | index) >> check >> equal >> 1
    tvseq((N**index)[tvseq], [1 | index, 2 | index, 3 | index]) >> at(_, 1 | index) >> check >> typeOf >> index

def test_drop():
    tvseq((N**pystr)[tvseq], ['a','b','c']) >> drop >> (2 | count) >> check >> typeOf >> (N**pystr)[tvseq]

def main():
    test_at()
    test_inject()
    test_stuff()
    test_misc()
    test_drop()


if __name__ == '__main__':
    main()
    print('pass')

