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

from coppertop.std.structs import tvstruct
from bones.core.types import pystr, pyint


def test():
    fred = tvstruct(pystr**(pystr*pyint), [[1,2]])
    fred.a = 1
    fred.b = 2
    print(fred['a'])
    fred['a'] = 5
    fred._fred = 1
    fred = fred | pystr**(pystr*pyint)
    print(fred._fred)
    print(repr(fred))
    print(str(fred))
    for k, v in fred._nvs():
        print(k, v)



def main():
    test()


if __name__ == '__main__':
    main()
    print('pass')
