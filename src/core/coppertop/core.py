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

version = '2022.01.05'       # coppertop.core.version


import sys
# sys._TRACE_IMPORTS = True
if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)


_all = set(['TBC', 'Missing', 'Null', 'Err', 'getMyPublicMembers', 'getPublicMembersOf'])

import inspect


def getMyPublicMembers(moduleName, globals, locals):
    pass

def getPublicMembersOf(module):
    pass

def _getPublicMembersOnly(module):
    def _isInOrIsChildOf(name, names):
        for parentName in names:
            if name[0:len(parentName)] == parentName:
                return True
        return False
    names = [module.__name__]
    members = [(name, o) for (name, o) in inspect.getmembers(module) if (name[0:1] != '_')]         # remove private
    members = [(name, o) for (name, o) in members if not (inspect.isbuiltin(o) or inspect.ismodule(o))]   # remove built-ins and modules

    # this form is easier to debug than
    members2 = []
    for name, o in members:
        if _isInOrIsChildOf(o.__module__, names):
            members2.append((name, o))
    # this form - but this problem is tooling rather than inherently list comprehensions
    members = [
        (name, o)
            for (name, o) in members
                if _isInOrIsChildOf(o.__module__, names)        # keep all @coppertops and children
    ]
    return [name for (name, o) in members]

# the following are wrapped in exception handlers to make test driven development and debugging of coppertop easier

try:
    from ._singletons import *
    from . import _singletons as _mod
    _all.update(_getPublicMembersOnly(_mod))
except Exception as ex:
    print(ex)
    pass

try:
    from ._module import *
    from . import _module as _mod
    _all.update(_getPublicMembersOnly(_mod))
except:
    pass

try:
    from ._repl import *
    from . import _repl as _mod
    _all.update(_getPublicMembersOnly(_mod))
except:
    pass


_all =list(_all)
_all.sort()
__all__ = _all


if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__ + ' - done')

