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
from coppertop.testing import assertRaises
from coppertop.std.linalg import matrix, to, tvarray
from coppertop.std import check, shape, equal


def test():
    A = [[1, 2], [3, 5]] >> to(_, matrix[tvarray])
    b = [1, 2] >> to(_, matrix[tvarray])
    A @ b >> shape >> check >> equal >> (2,1)
    with assertRaises(Exception) as e:
        b @ A



def main():
    test()


if __name__ == '__main__':
    main()
    print('pass')




