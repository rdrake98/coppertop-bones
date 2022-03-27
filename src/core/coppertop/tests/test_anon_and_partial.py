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
sys._TRACE_IMPORTS = True
if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)

from coppertop.pipe import *
from coppertop.pipe import NO_TYPE
from coppertop.testing import assertRaises
from dm.std import check, each, tvseq
from bones.core.types import pystr, pyint, N
from bones.core.metatypes import BTTuple



def test_anon():
    f = anon(pyint^pyint, lambda x: x + 1)
    fxs = tvseq((N ** pyint)[tvseq], [1, 2, 3]) >> each >> f
    fxs >> check >> typeOf >> (N ** pyint)[tvseq]
    with assertRaises(TypeError):
        fxs = tvseq((N ** pyint)[tvseq], [1, 2, 3]) >> each >> anon(pystr ^ pystr, lambda x: x + 1)

def test_partial():
    @coppertop
    def myunary_(a, b, c):
        return a + b + c
    t = myunary_ >> typeOf
    assert t == (BTTuple(NO_TYPE, NO_TYPE, NO_TYPE)^NO_TYPE)

    @coppertop
    def myunary(a:pyint, b:pyint, c:pyint) -> pyint:
        return a + b + c

    myunary >> check >> typeOf >> ((pyint*pyint*pyint)^pyint)
    myunary(1,_,3) >> check >> typeOf >> (pyint^pyint)

    fxs = tvseq((N ** pyint)[tvseq], [1, 2, 3]) >> each >> myunary(1,_,3)
    fxs >> check >> typeOf >> (N ** pyint)[tvseq]


def main():
    test_anon()
    test_partial()



if __name__ == '__main__':
    main()
    print('pass')

