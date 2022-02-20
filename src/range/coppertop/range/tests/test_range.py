# **********************************************************************************************************************
#
#                             Copyright (c) 2019-2020 David Briant
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

from coppertop.std import check, equal
from coppertop.range.std import rEach, rChain
from coppertop.range import IndexableFR, ListOR, getIRIter, materialise


def test_listRanges():
    r = IndexableFR([1,2,3])
    o = ListOR([])
    while not r.empty:
        o.put(r.front)
        r.popFront()
    r.indexable >> check >> equal >> o.list

def test_rangeOrRanges():
    rOfR = [] >> rChain
    [e for e in rOfR >> getIRIter] >> check >> equal >> []
    rOfR = (IndexableFR([]), IndexableFR([])) >> rChain
    [e for e in rOfR >> getIRIter] >> check >> equal >> []
    rOfR = (IndexableFR([1]), IndexableFR([2])) >> rChain
    [e for e in rOfR >> getIRIter] >> check >> equal >> [1,2]

def test_other():
    [1, 2, 3] >> rEach >> (lambda x: x) >> materialise >> check >> equal >> [1, 2, 3]

def test_take():
    r1 = IndexableFR([1,2,3])
    r2 = r1 >> take >> 3
    r1.popFront >> check >> equal >> 1
    r3 = r1 >> take >> 4
    r2 >> materialise >> check >> equal >> [1,2,3]
    r3 >> materialise >> check >> equal >> [2,3]


def main():
    test_listRanges()
    test_rangeOrRanges()
    test_other()
    # test_take()


if __name__ == '__main__':
    main()
    print('pass')


