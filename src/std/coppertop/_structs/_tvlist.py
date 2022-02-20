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

import sys

if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)

from collections import UserList
import abc
from bones.core.metatypes import BType


class tvseq(UserList):
    def __init__(self, *args):
        if len(args) == 1:
            arg = args[0]
            if isinstance(arg, tvseq):
                # tvseq(tvseq)
                super().__init__(arg._v)
                self._t = arg._t
            elif isinstance(arg, BType):
                # tvseq(<BType>)
                super().__init__()
                self._t = arg
            else:
                raise TypeError("Can't create tvseq without type information")
        elif len(args) == 2:
            # tvseq(t, iterable)
            arg1, arg2 = args
            super().__init__(arg2)
            self._t = arg1
        else:
            raise TypeError("Invalid arguments to tvseq constructor")

    @property
    def _v(self):
        return self.data

    def _asT(self, t):
        self._t = t
        return self

    def __repr__(self):
        itemStrings = (f"{str(e)}" for e in self.data)
        t = self._t
        if type(t) is abc.ABCMeta or t is tvseq:
            name = self._t.__name__
        else:
            name = str(self._t)
        rep = f'{name}({", ".join(itemStrings)})'
        return rep

    def __eq__(self, other):
        if isinstance(other, tvseq):
            return self._t == other._t and self.data == other.data
        else:
            return False

    def __getitem__(self, i):
        if isinstance(i, slice):
            return self.__class__(self._t, self.data[i])
        else:
            return self.data[i]



