# **********************************************************************************************************************
#
#                             Copyright (c) 2019-2022 David Briant. All rights reserved.
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
# You should have received a copy of the GNU Affero General Public License along with coppertop-bones. If not, see
# <https://www.gnu.org/licenses/>.
#
# **********************************************************************************************************************

from coppertop.core import Missing

class Sym(object):
    __slots__ = ['_id', '_st']
    def __init__(self, id, st):
        self._id = id
        self._st = st
    def __repr__(self):
        return '`%s'%(self._st._strings[self._id])
    def __str__(self):
        return self._st._strings[self._id]
    def __eq__(self, other):
        return self is other
    def __ne__(self, other):
        return self is not other
    def __lt__(self, other):
        return self._st._lt(self, other)
    def __gt__(self, other):
        return self._st._gt(self, other)
    def __le__(self, other):
        return self._st._le(self, other)
    def __ge__(self, other):
        return self._st._ge(self, other)
    def __cmp__(self, other):
        return self._st._cmp(self, other)


class SymTable(object):

    def __init__(self):
        self._symByString = {}
        self._syms = []
        self._strings = []
        self._isSorted = False
        self._sortOrder = []
        self._toBeSorted = []

    def Sym(self, string):
        # if it exists return it
        sym = self._symByString.get(string, Missing)
        if sym is not Missing: return sym

        # if it doesn't exist create it, add to the toBeSortedCollection and return it
        sym = Sym(len(self._strings), self)
        self._symByString[string] = sym
        self._strings.append(string)
        self._toBeSorted.append(sym)
        self._isSorted = False
        return sym

    def _sort(self):
        # I can come up with faster ways of doing this for my needs at the moment we'll just do it the easy way
        # e.g. sort the _toBeSorted then merge the two lists, could investigate how to sort large sets of strings
        # e.g. timsort, radix sort, etc
        strings = self._strings
        sortedSyms = sorted(self._syms + self._toBeSorted, key=lambda x:strings[x._id])      # syms is in order of id, i.e. adding order
        num = len(sortedSyms)
        self._sortOrder = [None] * num
        for position, sym in enumerate(sortedSyms):
            self._sortOrder[sym._id] = position
        self._syms.extend(self._toBeSorted)
        self._toBeSorted = []
        self._isSorted = True

    def _lt(self, a, b):
        if not self._isSorted: self._sort()
        return self._sortOrder[a._id] < self._sortOrder[b._id]
    def _gt(self, a, b):
        if not self._isSorted: self._sort()
        return self._sortOrder[a._id] > self._sortOrder[b._id]
    def _le(self, a, b):
        if not self._isSorted: self._sort()
        return self._sortOrder[a._id] <= self._sortOrder[b._id]
    def _ge(self, a, b):
        if not self._isSorted: self._sort()
        return self._sortOrder[a._id] >= self._sortOrder[b._id]
    def _cmp(self, a, b):
        if a is b:
            return 0
        if self._sortOrder[a._id] < self._sortOrder[b._id]:
            return -1
        return 1
