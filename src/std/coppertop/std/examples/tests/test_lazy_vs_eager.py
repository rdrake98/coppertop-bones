# **********************************************************************************************************************
#
#                             Copyright (c) 2020-2021 David Briant. All rights reserved.
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
from coppertop.std import each, check, equal
from coppertop.std.range import FnAdapterFR, EMPTY, FnAdapterEager, rEach, materialise
from coppertop.std.datetime import addDays, parseDate, day, toCTimeFormat

YYYY_MM_DD = 'YYYY.MM.DD' >> toCTimeFormat

@coppertop
def _ithDateBetween2(start, end, i):
    ithDate = start >> addDays(_, i)
    return EMPTY if ithDate > end else ithDate

@coppertop(style=binary2)
def datesBetween2(start, end):
     return FnAdapterFR(_ithDateBetween2(start, end, _))

@coppertop(style=binary2)
def datesBetweenEager2(start, end):
     return FnAdapterEager(_ithDateBetween2(start, end, _))


def test_datesBetween_lazy():
    ('2020.01.16' >> parseDate(_, YYYY_MM_DD)) >> datesBetween2 >> ('2020.01.29' >> parseDate(_, YYYY_MM_DD)) \
    >> rEach >> day \
    >> materialise >> check >> equal >> [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]

def test_datesBetween_eager():
    ('2020.01.16' >> parseDate(_, YYYY_MM_DD)) >> datesBetweenEager2 >> ('2020.01.29' >> parseDate(_, YYYY_MM_DD)) \
    >> each >> day \
    >> check >> equal >> [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]

def main():
    test_datesBetween_lazy()
    test_datesBetween_eager()

if __name__ == '__main__':
    main()
    print('pass')

