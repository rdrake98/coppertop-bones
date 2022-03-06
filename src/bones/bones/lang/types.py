# **********************************************************************************************************************
#
#                             Copyright (c) 2011-2021 David Briant. All rights reserved.
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
# You should have received a copy of the GNU Affero General Public License along with Foobar. If not, see
# <https://www.gnu.org/licenses/>.
#
# **********************************************************************************************************************

import sys
if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)


from bones.core.metatypes import BTAtom as _BTAtom



# piping styles
noun = _BTAtom.ensure("noun")
nullary = _BTAtom.ensure("nullary")
unary = _BTAtom.ensure("unary")
binary = _BTAtom.ensure("binary")
ternary = _BTAtom.ensure("ternary")
rau = _BTAtom.ensure("rau")


# _BTAtom.define('imlist')        # immediate list, e.g. (1,2,3)
# _BTAtom.define('deflist')       # deferred list, e.g. [x: 1, x: 2, 3*3]
#
# _BTAtom.define('ast')
#
# _BTAtom.define('TFn')
# _BTAtom.define('FnByArgTypes')
# _BTAtom.define('PyFn')
#
# _BTAtom.define('null')
#
# _BTAtom('index')
# _BTAtom('offset')
# _BTAtom('num')
# _BTAtom('count')
#
# _BTAtom.define('vector')
# _BTAtom.define('matrix')
# _BTAtom.define('tensor')