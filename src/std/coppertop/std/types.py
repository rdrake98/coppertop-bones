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

from coppertop.std.structs import tvstruct as _tvstruct
from bones.core.metatypes import BTAtom
from bones.core.types import num, N, tv


adhoc = BTAtom.define('adhoc').setConstructor(_tvstruct)
agg = BTAtom.define('agg').setConstructor(_tvstruct)

ellipsis = type(...)



TBT = BTAtom.define('TBT')      # temporary type to allow  'fred' >> box | pystr - aka to be types
void = BTAtom.ensure('void')    # nothing returned on the stack from this function (should not be assignable)

# NB a 1x1 matrix is assumed to be a scalar, e.g. https://en.wikipedia.org/wiki/Dot_product#Algebraic_definition

vec = (N**num)          # N**num is common so don't name it
matrix = (N**N**num).nameAs('matrix').setNonExclusive
colvec = matrix['colvec'].setNonExclusive
rowvec = matrix['rowvec'].setNonExclusive

I = BTAtom.define('I')
square = BTAtom.define('square')
right = BTAtom.define('right')
left = BTAtom.define('left')
upper = BTAtom.define('upper')
lower = BTAtom.define('lower')
orth = BTAtom.define('orth')
diag = BTAtom.define('diag')
tri = BTAtom.define('tri')
cov = BTAtom.define('cov')

ccy = BTAtom.define('ccy').setExplicit
fx = BTAtom.define('fx').setExplicit

matrix[tv].setConstructor(tv).setExclusive    # tv provides a coercion method so matrix[tv] doesn't need to
