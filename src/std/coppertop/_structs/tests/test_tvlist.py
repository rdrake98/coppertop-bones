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

from coppertop.pipe import typeOf
from coppertop.std.structs import tvseq
from coppertop.std import check, equal, append, join, _v
from bones.core.types import N, num


def test():
    fred = tvseq((N**num)[tvseq], [1, 2])
    fred >> _v >> check >> equal >> [1, 2]
    fred >> check >> typeOf >> (N**num)[tvseq]
    fred = fred >> append >> 3
    fred = fred >> join >> tvseq((N**num)[tvseq], [4, 5])
    fred >> _v >> check >> equal >> [1, 2, 3, 4, 5]
    print(repr(fred))
    print(str(fred))



def main():
    test()


if __name__ == '__main__':
    main()
    print('pass')
