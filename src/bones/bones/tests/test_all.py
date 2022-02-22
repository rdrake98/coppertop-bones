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


# metatype tests
from bones.core.tests import test_metatypes
from bones.core.tests import test_fits
from bones.core.tests import test_partition
from bones.core.tests import test_polymorphic

# lang tests
from bones.lang.tests import test_lex
from bones.lang.tests import test_group
from bones.lang.tests import test_group_visitors
from bones.lang.tests import test_sym



def main():
    # metatype tests
    test_fits.main()
    test_metatypes.main()
    test_partition.main()
    test_polymorphic.main()

    # lang tests
    test_sym.main()
    test_lex.main()
    test_group.main()
    # test_group_visitors.main()



if __name__ == '__main__':
    main()
    print('pass')
    from bones.core.metatypes import BType
    from coppertop.std import count
    from coppertop.core import Missing
    print([t for t in BType._BTypeById if t is not Missing] >> count)
