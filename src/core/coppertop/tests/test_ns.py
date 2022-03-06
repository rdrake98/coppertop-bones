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
from coppertop.testing import assertRaises
from coppertop.std import check, equal
from bones.core.types import pystr, pyfloat

from coppertop.tests.adders import addOne, eachAddOne, eachAddTwo


@coppertop
def addTwo(x: pystr) -> pystr:
    return x + 'Two'


def test_addOneEtc():
    1 >> addOne >> check >> equal >> 2
    [1, 2] >> eachAddOne >> check >> equal >> [2, 3]


def test_updatingAddOne():

    # now we want to use it with strings
    @coppertop
    def addOne(x:pystr) -> pystr:
        return x + 'One'

    # and floats
    @coppertop
    def addOne(x:pyfloat) -> pyfloat:
        return x + 1.0

    # check our new implementation
    1 >> addOne >> check >> equal >> 2
    'Two' >> addOne >> check >> equal >> 'TwoOne'
    1.0 >> addOne >> check >> equal >> 2.0

    # but
    with assertRaises(Exception) as ex:
        a = ['Two'] >> eachAddOne >> check >> equal >> ['TwoOne']
    # which is to be expected since the above are local (defined in a function)

    b = ['One'] >> eachAddTwo >> check >> equal >> ['OneTwo']



def main():
    test_addOneEtc()
    test_updatingAddOne()


if __name__ == '__main__':
    main()
    print('pass')

