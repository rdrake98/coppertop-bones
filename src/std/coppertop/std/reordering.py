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
from coppertop.core import NotYetImplemented
from coppertop.std.structs import tvstruct
from bones.core.types import pydict, pylist, pyfunc
from coppertop.std.types import adhoc




# **********************************************************************************************************************
# sort
# **********************************************************************************************************************

@coppertop(style=unary1)
def sort(x:pydict) -> pydict:
    return dict(sorted(x.items(), key=None, reverse=False))

@coppertop(style=unary1)
def sort(x:tvstruct) -> tvstruct:
    return tvstruct(sorted(x._nvs(), key=None, reverse=False))

@coppertop(style=unary1)
def sort(x:adhoc) -> adhoc:
    return adhoc(sorted(x._nvs(), key=None, reverse=False))

@coppertop(style=unary1)
def sort(x:pylist) -> pylist:
    return sorted(x, key=None, reverse=False)


# **********************************************************************************************************************
# sortBy
# **********************************************************************************************************************

@coppertop
def sortBy(agg, names):
    raise NotYetImplemented()

@coppertop
def sortBy(agg, names, directions):
    raise NotYetImplemented()


# **********************************************************************************************************************
# sortRev
# **********************************************************************************************************************

@coppertop(style=unary1)
def sortRev(x:pylist) -> pylist:
    return sorted(x, key=None, reverse=True)

@coppertop(style=unary1)
def sortRev(x:pydict) -> pydict:
    return dict(sorted(x.items(), key=None, reverse=True))


# **********************************************************************************************************************
# sortRevUsing
# **********************************************************************************************************************

@coppertop(style=binary2)
def sortRevUsing(x:pylist, key:pyfunc) -> pylist:
    return sorted(x, key=key, reverse=True)

@coppertop(style=binary2)
def sortRevUsing(x:pydict, key:pyfunc) -> pydict:
    return dict(sorted(x.items(), key=key, reverse=True))


# **********************************************************************************************************************
# sortUsing
# **********************************************************************************************************************

@coppertop(style=binary2)
def sortUsing(x:pylist, key:pyfunc) -> pylist:
    return sorted(x, key=key, reverse=False)

@coppertop(style=binary2)
def sortUsing(x:pydict, key:pyfunc) -> pydict:
    return dict(sorted(x.items(), key=key, reverse=False))

@coppertop(style=binary)
def sortUsing(soa, f):
    raise NotYetImplemented()

