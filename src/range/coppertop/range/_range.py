# **********************************************************************************************************************
#
#                             Copyright (c) 2019-2020 David Briant. All rights reserved.
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

from __future__ import annotations

import sys, types

if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)

from typing import Any, Union
from coppertop.pipe import *
from coppertop.core import Null

if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__ + ' - imports done')


if not hasattr(sys, '_EMPTY'):
    class _EMPTY(object):
        def __bool__(self):
            return False
        def __repr__(self):
            # for pretty display in pycharm debugger
            return 'EMPTY'
    sys._EMPTY = _EMPTY()
EMPTY = sys._EMPTY


# d style ranges
# http://www.informit.com/articles/printerfriendly/1407357 - Andrei Alexandrescu
# https://www.drdobbs.com/architecture-and-design/component-programming-in-d/240008321 - Walter Bright

# empty - checks for end-of-input and fills a one-element buffer held inside the range object
# front - returns the buffer
# popFront() - sets an internal flag that tells empty to read the next element when called
# moveFront() - moves to the start


class IInputRange(object):
    @property
    def empty(self) -> bool:
        raise NotImplementedError()
    @property
    def front(self) -> Any:
        raise NotImplementedError()
    def popFront(self) -> None:
        raise NotImplementedError()
    def moveFront(self) -> Any:
        raise NotImplementedError()

    # assignable
    @front.setter
    def front(self, value: Any) -> None:
        raise NotImplementedError()

    # python iterator interface - so we can use ranges in list comprehensions and for loops!!! ugh
    # this is convenient but possibly too convenient and it may muddy things hence the ugly name
    @property
    def _getIRIter(self):
        return IInputRange._Iter(self)

    class _Iter(object):
        def __init__(self, r):
            self.r = r
        def __iter__(self) -> IInputRange:
            return self
        def __next__(self) -> Any:
            if self.r.empty: raise StopIteration
            answer = self.r.front
            self.r.popFront()
            return answer

@coppertop
def getIRIter(r):
    # the name is deliberately semi-ugly to discourage but not prevent usage - see comment above
    return r._getIRIter


class IForwardRange(IInputRange):
    def save(self) -> IForwardRange:
        raise NotImplementedError()


class IBidirectionalRange(IForwardRange):
    @property
    def back(self) -> Any:
        raise NotImplementedError()
    def moveBack(self) -> Any:
        raise NotImplementedError()
    def popBack(self) -> None:
        raise NotImplementedError()

    # assignable
    @back.setter
    def back(self, value: Any) -> None:
        raise NotImplementedError()


class IRandomAccessFinite(IBidirectionalRange):
    def moveAt(self, i: int) -> Any:
        raise NotImplementedError()
    def __getitem__(self, i: Union[int, slice]) -> Union[Any, IRandomAccessFinite]:
        raise NotImplementedError()
    @property
    def length(self) -> pyint:
        raise NotImplementedError()

    # assignable
    def __setitem__(self, i: int, value: Any) -> None:
        raise NotImplementedError()


class IRandomAccessInfinite(IForwardRange):
    def moveAt(self, i: int) -> Any:
        raise NotImplementedError()

    def __getitem__(self, i: int) -> Any:
        """Answers an element"""
        raise NotImplementedError()


class IOutputRange(object):
    def put(self, value: Any):
        """Answers void"""
        raise NotImplementedError()


@coppertop
def toIRangeIfNot(x):
    if isinstance(x, IInputRange):
        return x
    else:
        return IndexableFR(x)


class FnAdapterFR(IForwardRange):
    # adapts a unary function (that takes a position index) into a forward range
    def __init__(self, f):
        self.f = f
        self.i = 0
        self.current = self.f(self.i)
    @property
    def empty(self):
        return self.current == EMPTY
    @property
    def front(self):
        return self.current
    def popFront(self):
        self.i += 1
        if not self.empty:
            self.current = self.f(self.i)
    def save(self):
        new = FnAdapterFR(self.f)
        new.i = self.i
        new.current = new.f(new.i)
        return  new
    def repr(self):
        return 'FnAdapterFR(%s)[%s]' % (self.f, self.i)

def FnAdapterEager(f):
    answer = []
    i = 0
    while (x := f(i)) != EMPTY:
        answer.append(x)
        i += 1
    return answer


class ChunkFROnChangeOf(IForwardRange):
    def __init__(self, r, f):
        assert isinstance(r, IForwardRange)
        self.r = r
        self.f = f
        self.lastF = None if self.r.empty else self.f(self.r.front)
    @property
    def empty(self):
        return self.r.empty
    @property
    def front(self):
        assert not self.r.empty
        return _ChunkFR(self.r, self.f, self.lastF)
    def popFront(self):
        assert not self.r.empty
        while not self.r.empty and self.f(self.r.front) == self.lastF:
            self.r.popFront()
        if not self.r.empty:
            self.lastF = self.f(self.r.front)
    def save(self):
        return ChunkFROnChangeOf(self.r.save(), self.f)
    def __repr__(self):
        return 'ChunkFROnChangeOf(%s,%s)' % (self.r, self.curF)

class _ChunkFR(IForwardRange):
    def __init__(self, r, f, curF):
        self.r = r
        self.f = f
        self.curF = curF
    @property
    def empty(self):
        return self.r.empty or self.curF != self.f(self.r.front)
    @property
    def front(self):
        return self.r.front
    def popFront(self):
        assert not self.r.empty
        self.r.popFront()
    def save(self):
        return _ChunkFR(self.r.save(), self.f, self.curF)
    def __repr__(self):
        return '_ChunkFR(%s)' % self.curF


class UntilFR(IForwardRange):
    def __init__(self, r, f):
        if not isinstance(r, IForwardRange):
            raise TypeError(str(r))
        self.r = r
        self.f = f
        self.hasFound = False
    @property
    def empty(self):
        return self.r.empty or self.hasFound
    @property
    def front(self):
        assert not self.r.empty
        return self.r.front
    def popFront(self):
        assert not self.empty
        self.hasFound = self.f(self.r.front)
        self.r.popFront()

    def save(self):
        return UntilFR(self.r.save(), self.f)
    def __repr__(self):
        return 'UntilFR(%s,%s)' % (self.r, self.f)


class ChunkUsingSubRangeGeneratorFR(IForwardRange):
    def __init__(self, r, f):
        self.r = r
        self.f = f
        self.curSR = None if self.r.empty else self.f(self.r)
    @property
    def empty(self):
        return self.r.empty
    @property
    def front(self):
        assert not self.r.empty
        return self.curSR
    def popFront(self):
        self.curSR = None if self.r.empty else self.f(self.r)

    def save(self) -> IForwardRange:
        new = ChunkUsingSubRangeGeneratorFR(self.r.save(), self.f)
        new.curSR = None if self.curSR is None else self.curSR.save()
        return new


class IndexableFR(IForwardRange):
    def __init__(self, indexable):
        self.indexable = indexable
        self.i= 0
    @property
    def empty(self):
        return self.i >= len(self.indexable)
    @property
    def front(self):
        return self.indexable[self.i]
    def popFront(self):
        self.i += 1
    def save(self):
        new = IndexableFR(self.indexable.__class__(self.indexable))
        new.i = self.i
        return new
toIndexableFR = coppertop(style=unary1, newName='toIndexableFR')(IndexableFR)

class ListOR(IOutputRange):
    def __init__(self, list):
        self.list = list
    def put(self, value):
        self.list.append(value)


class ChainAsSingleFR(IForwardRange):
    def __init__(self, listOfRanges):
        self.rOfR = listOfRanges >> toIndexableFR
        if self.rOfR.empty:
            self.curR = None
        else:
            self.curR = self.rOfR.front
            self.rOfR.popFront()
    @property
    def empty(self):
        if self.curR is None: return True
        while self.curR.empty and not self.rOfR.empty:
            self.curR = self.rOfR.front
            self.rOfR.popFront()
        return self.curR.empty
    @property
    def front(self):
        assert not self.curR.empty
        return self.curR.front
    def popFront(self):
        if not self.curR.empty:
            self.curR.popFront()


class EachFR(IForwardRange):
    def __init__(self, r, fn):
        self.r = r >> toIRangeIfNot
        if not callable(fn):
            raise TypeError("RMAP.__init__ fn should be a function but got a %s" % type(fn))
        self.f = fn
    @property
    def empty(self):
        return self.r.empty
    @property
    def front(self):
        return self.f(self.r.front)
    def popFront(self):
        self.r.popFront()
    def save(self):
        return EachFR(self.r.save(), self.f)


class FileLineIR(IInputRange):
    def __init__(self, f, stripNL=False):
        self.f = f
        self.line = self.f.readline()
    @property
    def empty(self):
        return self.line == ''
    @property
    def front(self):
        return self.line
    def popFront(self):
        self.line = self.f.readline()


class RaggedZipIR(IInputRange):
    """As RZip but input ranges do not need to be of same length, shorter ranges are post padded with Null"""
    def __init__(self, ror):
        self.ror = ror
        self.allEmpty = ror >> allSubRangesExhausted
    @property
    def empty(self):
        return self.allEmpty
    @property
    def front(self) -> pylist:
        parts = []
        ror = self.ror.save()
        while not ror.empty:
            subrange = ror.front
            if subrange.empty:
                parts.append(Null)
            else:
                parts.append(subrange.front)
            if not subrange.empty:
                subrange.popFront()
        return parts
    def popFront(self):
        ror = self.ror.save()
        self.allEmpty = True
        while not ror.empty:
            subrange = ror.front
            if not subrange.empty:
                subrange.popFront()
                if not subrange.empty:
                    self.allEmpty = False
            ror.popFront()


@coppertop
def allSubRangesExhausted(ror):
    ror = ror.save()
    answer = True
    while not ror.empty:
        if not ror.front.empty:
            answer = False
            break
    return answer


if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__ + ' - done')
