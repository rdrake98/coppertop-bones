# **********************************************************************************************************************
#
#                             Copyright (c) 2019-2021 David Briant. All rights reserved.
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


from coppertop.pipe import *
from bones.core.types import pybool, pyint

class IInputRange(object):
    @property
    def empty(self) -> pybool:
        raise NotImplementedError()
    @property
    def front(self):
        raise NotImplementedError()
    def popFront(self):
        raise NotImplementedError()
    def moveFront(self):
        raise NotImplementedError()

    # assignable
    @front.setter
    def front(self, value):
        raise NotImplementedError()

    # python iterator interface - so we can use ranges in list comprehensions and for loops!!! ugh
    # this is convenient but possibly too convenient and it may muddy things hence the ugly name
    @property
    def _getIRIter(self):
        return IInputRange._Iter(self)

    class _Iter(object):
        def __init__(self, r):
            self.r = r
        def __iter__(self):
            return self
        def __next__(self):
            if self.r.empty: raise StopIteration
            answer = self.r.front
            self.r.popFront()
            return answer

@coppertop
def getIRIter(r):
    # the name is deliberately semi-ugly to discourage but not prevent usage - see comment above
    return r._getIRIter


class IForwardRange(IInputRange):
    def save(self):
        raise NotImplementedError()


class IBidirectionalRange(IForwardRange):
    @property
    def back(self):
        raise NotImplementedError()
    def moveBack(self):
        raise NotImplementedError()
    def popBack(self):
        raise NotImplementedError()

    # assignable
    @back.setter
    def back(self, value):
        raise NotImplementedError()


class IRandomAccessFinite(IBidirectionalRange):
    def moveAt(self, i: int):
        raise NotImplementedError()
    def __getitem__(self, i: pyint+slice):
        raise NotImplementedError()
    @property
    def length(self) -> pyint:
        raise NotImplementedError()

    # assignable
    def __setitem__(self, i: int, value):
        raise NotImplementedError()


class IRandomAccessInfinite(IForwardRange):
    def moveAt(self, i: int):
        raise NotImplementedError()

    def __getitem__(self, i: int):
        """Answers an element"""
        raise NotImplementedError()


class IOutputRange(object):
    def put(self, value):
        """Answers void"""
        raise NotImplementedError()




