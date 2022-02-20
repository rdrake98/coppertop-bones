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

import math, numpy
from coppertop.pipe import *
from coppertop.std.linalg import tvarray


@coppertop
def cov(A:tvarray) -> tvarray:
    return numpy.cov(A).view(tvarray)

@coppertop
def mean(ndOrPy):
    # should do full numpy?
    return numpy.mean(ndOrPy)

@coppertop
def std(ndOrPy, dof=0):
    # should do full numpy? std(a, axis=None, dtype=None, out=None, ddof=0, keepdims=<no value>)
    return numpy.std(ndOrPy, dof)

@coppertop
def logisticCDF(x, mu, s):
    return 1 / (1 + math.exp(-1 * (x - mu) / s))

@coppertop
def logisticCDFInv(p, mu, s):
    return mu + -s * math.log(1 / p - 1)
