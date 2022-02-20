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

from coppertop.std import closeTo, check, equal
from dm.misc import sequence
from dm.pmf import uniform, rvAdd, mix, toXsPs, PMF



def test_pmf():
    d4 = uniform(sequence(1, 4))
    d6 = uniform(sequence(1, 6))
    rv = d4 >> rvAdd >> d4
    rv[2] >> check >> equal >> 1/16

    d4d6 = [d4, d6] >> mix
    result = d4d6[1]
    expected = (1/4 + 1/6) / (4 * (1/4 + 1/6) + 2 * 1/6)
    assert closeTo(result, expected, 0.00001), '%s != %s' % (result, expected)

    (d4 >> toXsPs)[0] >> check >> equal >> (1.0, 2.0, 3.0, 4.0)


def test_MMs():
    bag1994 = PMF(Brown=30, Yellow=20, Red=20, Green=10, Orange=10, Tan=10)
    bag1994.Brown >> check >> closeTo >> 0.3
    bag1996 = PMF(Brown=13, Yellow=14, Red=13, Green=20, Orange=16, Blue=24)

def main():
    test_pmf()
    test_MMs()


if __name__ == '__main__':
    main()
    print('pass')

