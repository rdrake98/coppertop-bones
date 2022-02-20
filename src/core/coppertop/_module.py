# **********************************************************************************************************************
#
#                             Copyright (c) 2011-2020 David Briant. All rights reserved.
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


__all__ = ['ensurePath', 'printModules', 'unload']
from coppertop.pipe import *


@coppertop
def ensurePath(path):
    import sys
    if path not in sys.path:
        sys.path.insert(0, path)


@coppertop
def printModules(root):
    noneNames = []
    moduleNames = []
    for k, v in sys.modules.items():
        if k.find(root) == 0:
            if v is None:
                noneNames.append(k)
            else:
                moduleNames.append(k)
    noneNames.sort()
    moduleNames.sort()
    print("****************** NONE ******************")
    for name in noneNames:
        print(name)
    print("****************** MODULES ******************")
    for name in moduleNames:
        print(name)


@coppertop
def unload(module_name, leave_relative_imports_optimisation=False):
    # for description of relative imports optimisation in earlier versions of python see:
    # http://www.python.org/dev/peps/pep-0328/#relative-imports-and-indirection-entries-in-sys-modules

    l = len(module_name)
    module_names = list(sys.modules.keys())
    for name in module_names:
        if name[:l] == module_name:
            if leave_relative_imports_optimisation:
                if sys.modules[name] is not None:
                    del sys.modules[name]
            else:
                del sys.modules[name]


if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__ + ' - done')
