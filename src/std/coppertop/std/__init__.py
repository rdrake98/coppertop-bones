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

version = '2022.01.05'       # coppertop.std.version


import sys

if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)

import inspect
from coppertop.pipe import _DispatcherBase, _MultiDispatcher, MultiFn, _, sig
from coppertop.std.structs import tvarray, tvstruct

_mfByName = {}



def _collectDispatchers(mfByName, module):
    members = inspect.getmembers(module)
    members = [(name, o) for (name, o) in members if (name[0:1] != '_')]         # remove private
    members = [(name, mf) for (name, mf) in members if isinstance(mf, MultiFn)]
    for name, mf in members:
        mfByName.setdefault(name, []).append(mf)



# aggregation protocols
from coppertop.std import accessing as _mod; _collectDispatchers(_mfByName, _mod)
from coppertop.std import combining as _mod; _collectDispatchers(_mfByName, _mod)
from coppertop.std import complex as _mod; _collectDispatchers(_mfByName, _mod)
from coppertop.std import converting as _mod; _collectDispatchers(_mfByName, _mod)
from coppertop.std import dividing as _mod; _collectDispatchers(_mfByName, _mod)
from coppertop.std import generating as _mod; _collectDispatchers(_mfByName, _mod)
from coppertop.std import reordering as _mod; _collectDispatchers(_mfByName, _mod)
from coppertop.std import searching as _mod; _collectDispatchers(_mfByName, _mod)
from coppertop.std import transforming as _mod; _collectDispatchers(_mfByName, _mod)

# other protocols
from coppertop.std import files as _mod; _collectDispatchers(_mfByName, _mod)
from coppertop.std import linalg as _mod; _collectDispatchers(_mfByName, _mod)
from coppertop.std import maths as _mod; _collectDispatchers(_mfByName, _mod)
from coppertop.std import misc as _mod; _collectDispatchers(_mfByName, _mod)
from coppertop.std import stdio as _mod; _collectDispatchers(_mfByName, _mod)
from coppertop.std import testing as _mod; _collectDispatchers(_mfByName, _mod)
from coppertop.std import text as _mod; _collectDispatchers(_mfByName, _mod)
from coppertop.std import types as _mod; _collectDispatchers(_mfByName, _mod)

# aggregation protocols
from coppertop.std.accessing import *
from coppertop.std.combining import *
from coppertop.std.complex import *
from coppertop.std.converting import *
from coppertop.std.dividing import *
from coppertop.std.generating import *
from coppertop.std.reordering import *
from coppertop.std.searching import *
from coppertop.std.transforming import *

# other protocols
from coppertop.std.files import *
from coppertop.std.linalg import *
from coppertop.std.maths import *
from coppertop.std.misc import *
from coppertop.std.stdio import *
from coppertop.std.testing import *
from coppertop.std.text import *
from coppertop.std.types import *

from coppertop.std.misc import _t, _v   # needs doing separately as _ generally indicates it is pvt



__all__ = list(_mfByName.keys()) + ['_', 'tvarray', 'agg', '_t', '_v', 'typeOf', 'sig']


if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__ + ' - done')

