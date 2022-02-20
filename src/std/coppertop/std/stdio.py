# **********************************************************************************************************************
#
#                             Copyright (c) 2020 David Briant. All rights reserved.
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


class OStreamWrapper(object):
    def __init__(self, sGetter):
        self._sGetter = sGetter
    def __lshift__(self, other):
        # self << other
        self._sGetter().write(other)      # done as a function call so it plays nicely with HookStdOutErrToLines
        return self


stdout = OStreamWrapper(lambda : sys.stdout)
stderr = OStreamWrapper(lambda : sys.stderr)

