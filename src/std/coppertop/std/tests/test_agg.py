# **********************************************************************************************************************
#
#                             Copyright (c) 2017-2020 David Briant. All rights reserved.
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




from coppertop.std import select, update, delete, sortBy, agg


def test():
    agg = []
    agg2 = select(["a", ], [], agg, [])
    agg3 = update([["a", lambda x: x]], [], agg2, [])
    agg3 = delete(agg3, [])

def test2():
    a = agg(a=[1,2,1,2,1,2],b=[2,2,2,1,1,1],c=['a','b','c','d','e','f'])
    r = a >> sortBy >> ['b', 'a']

def test_groupBy():
    a = freds \
        >> chunkBy('a') \
        >> map >> (lambda g: tvstruct(
            b=g >> first >> at(_, 'b'),
            a=g >> first >> at(_, 'a'),
            N=g >> count,
        ))

    b = freds \
        >> chunkBy('b') \
        >> inject(_, Null, _) >> (lambda p, g: p >> join >> (g >> byA >> join >> Null))


def main():
    test()


if __name__ == '__main__':
    main()
    print('pass')




