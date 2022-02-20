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

import os
from coppertop.std import assertEquals
from coppertop.range.examples.count_lines_jsp import countLinesJsp, countLinesTrad, countLinesRanges1, countLinesRanges2, countLinesRanges3


home = os.path.dirname(os.path.abspath(__file__))
filename = "/linesForCounting.txt"
expected = [
    ('aaa\n', 2),
    ('bb\n', 1),
    ('aaa\n', 1),
    ('bb\n', 3),
    ('aaa\n', 1)
]

def main():
    with open(home + filename) as f:
        actual = countLinesJsp(f)
    actual >> assertEquals >> expected

    with open(home + filename) as f:
        actual = countLinesTrad(f)
    actual >> assertEquals >> expected

    with open(home + filename) as f:
        actual = countLinesRanges1(f)
    actual >> assertEquals >> expected

    with open(home + filename) as f:
        actual = countLinesRanges2(f)
    actual >> assertEquals >> expected

    with open(home + filename) as f:
        actual = countLinesRanges3(f)
    actual >> assertEquals >> expected


if __name__ == '__main__':
    main()
    print('pass')

