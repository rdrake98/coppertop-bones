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

# vector operations

import numpy
import datetime

from coppertop.pipe import *
from coppertop.std.linalg import tvarray
from coppertop.std.datetime import parseDate, toCTimeFormat
from bones.core.types import pystr, pyfloat, pydate, pylist


@coppertop
def diff(v:tvarray) -> tvarray:
    return numpy.diff(v)

@coppertop
def log(v:tvarray) -> tvarray:
    return numpy.log(v)

def parseNum(x:pystr) -> pyfloat:
    try:
        return float(x)
    except:
        return numpy.nan

@coppertop
def to(xs:pylist, t:pyfloat) -> tvarray:
    return tvarray([parseNum(x) for x in xs])

@coppertop
def to(xs:pylist, t:pydate, f:pystr) -> tvarray:
    cFormat = toCTimeFormat(f)
    return tvarray([parseDate(x, cFormat) for x in xs])
