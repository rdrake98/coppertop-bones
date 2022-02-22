# **********************************************************************************************************************
#
#                             Copyright (c) 2021-2022 David Briant. All rights reserved.
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


# bones tests
from bones.tests import test_all as bones_test_all

# core tests
from coppertop.tests import test_styles
from coppertop.tests import test_ns
from coppertop.tests import test_anon_and_partial
from coppertop.tests import test_pipeable
from coppertop.tests import test_testing
from coppertop.tests import test_scope
from coppertop.tests import test_fx

# std tests
from coppertop.std.tests import test_agg_us_yields
from coppertop.std.tests import test_std
from coppertop.std._linalg.tests import test_linealg_core

# range tests
from coppertop.std.tests import test_range
from coppertop.std.examples.tests import test_count_lines_jsp
from coppertop.std.examples.tests import test_format_calendar
from coppertop.std.examples.tests import test_lazy_vs_eager
from coppertop.std.examples.tests import test_misc as examples_test_misc

# dm tests
from dm.tests import test_all as dm_test_all



def main():
    # bones
    bones_test_all.main()

    # coppertop
    test_styles.main()
    test_ns.main()
    test_anon_and_partial.main()
    test_pipeable.main()
    test_testing.main()
    test_scope.main()
    test_fx.main()

    # std
    # test_agg.main()
    test_agg_us_yields.main()
    test_std.main()
    test_linealg_core.main()

    # range
    test_range.main()
    test_count_lines_jsp.main()
    test_format_calendar.main()
    test_lazy_vs_eager.main()
    examples_test_misc.main()

    # dm
    dm_test_all.main()



if __name__ == '__main__':
    main()
    print('pass')
    from bones.core.metatypes import BType
    from coppertop.std import count
    from coppertop.core import Missing
    print([t for t in BType._BTypeById if t is not Missing] >> count)

