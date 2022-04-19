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
# You should have received a copy of the GNU Affero General Public License along with coppertop-bones. If not, see
# <https://www.gnu.org/licenses/>.
#
# **********************************************************************************************************************

import sys
sys._TRACE_IMPORTS = True
if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)

import coppertop.pipe

import cProfile, pstats
cProfile.run('''

import coppertop.tests.test_all

''', 'testAndProfileAll.profile')

from pstats import SortKey
p = pstats.Stats('test_and_profile_all.profile')
p.strip_dirs().sort_stats(SortKey.CUMULATIVE).print_stats(30)



def main():
    coppertop.tests.testAll.main()


if __name__ == '__main__':
    main()
    print('pass')