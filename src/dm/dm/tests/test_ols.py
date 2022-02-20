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

from coppertop.pipe import *
from coppertop.std import matrix
from coppertop.std import check, equal
from coppertop.std import tvarray
from bones.core.types import pybool



# utility fns
@coppertop
def to(v, t:matrix) -> matrix:
    return tvarray(t,v)

@coppertop(style=binary2)
def equal(a:matrix, b:matrix) -> pybool:
    return bool((a == b).all())


# domain functions
@coppertop(style=unary1)
def T(A:matrix) -> matrix:
    return A.T



def test1():
    A = ([[1, 2], [3, 4]] >> to(_,matrix))
    AT = A >> T
    B = ([[1,3], [2,4]] >> to(_,matrix))
    AT >> check >> equal >> B


def main():
    test1()


if __name__ == '__main__':
    main()
    print('pass')



