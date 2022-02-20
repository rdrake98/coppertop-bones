# **********************************************************************************************************************
#
#                             Copyright (c) 2021 David Briant. All rights reserved.
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
sys._TRACE_IMPORTS = True
if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)

from coppertop.pipe import *
from coppertop.core import assertRaises, PP
from coppertop.std import check, equal, different
from bones.core.types import pystr, pyint

from coppertop.tests.adders import addOne, eachAddOne, eachAddTwo


@coppertop
def addOneAgain(x: pystr) -> pystr:
    return x + 'One'

@coppertop
def addOneAgain(x):
    return x + 1

@coppertop
def addOneAgain(x):
    return x + 2



def test_redefine():
    1 >> addOneAgain >> check >> 3



def main():
    test_redefine()


if __name__ == '__main__':
    main()
    print('pass')

