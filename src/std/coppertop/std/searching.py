# **********************************************************************************************************************
#
#                             Copyright (c) 2017-2021 David Briant. All rights reserved.
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
if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)

from coppertop.pipe import *
from bones.core.types import pystr, pybool

dict_keys = type({}.keys())
dict_values = type({}.values())
ellipsis = type(...)
function = type(lambda x:x)



# **********************************************************************************************************************
# endsWith
# **********************************************************************************************************************

@coppertop(style=binary2)
def endsWith(s1:pystr, s2:pystr) -> pybool:
    return s1.endswith(s2)


# **********************************************************************************************************************
# startsWith
# **********************************************************************************************************************

@coppertop(style=binary2)
def startsWith(s1:pystr, s2:pystr) -> pybool:
    return s1.startswith(s2)

