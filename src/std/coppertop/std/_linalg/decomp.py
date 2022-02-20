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

import numpy
from coppertop.pipe import *
from coppertop.std.types import adhoc, right, orth
from coppertop.std._linalg.core import matrix, tvarray

_matrix = matrix[tvarray]

@coppertop(style=unary1)
def QR(A:_matrix) -> adhoc:
    Q, R = numpy.linalg.qr(A)
    return adhoc(Q=_matrix(Q) | +orth, R=_matrix(R) | +right)

@coppertop(style=unary1)
def Cholesky(A:_matrix) -> _matrix&right:
    return _matrix(numpy.linalg.cholesky(A)) | +right
