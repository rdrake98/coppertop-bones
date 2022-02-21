# **********************************************************************************************************************
#
#                             Copyright (c) 2020-2021 David Briant. All rights reserved.
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

# see - https://en.wikipedia.org/wiki/Jackson_structured_programming
# this file show four ways to implement the problem of counting repeated lines in a file - two are translations from
# the wikipedia article and the remaining two take the "traditional" program and transform it into range style code


from coppertop.pipe import *
from coppertop.std import getAttr, _
from coppertop.std.range import FileLineIR, ListOR, IInputRange, put, pushAllTo


def countLinesTrad(f):
    answer = []

    count = 0
    firstLineOfGroup = ''
    line = f.readline()
    while line != '':
        if firstLineOfGroup == '' or line != firstLineOfGroup:
            if firstLineOfGroup != '':
                answer.append((firstLineOfGroup, count))
            count = 0
            firstLineOfGroup = line
        count += 1
        line = f.readline()

    if (firstLineOfGroup != ''):
        answer.append((firstLineOfGroup, count))

    return answer



def countLinesRanges1(f):
    r = FileLineIR(f)
    out = ListOR([])

    count = 0
    firstLineOfGroup = ''
    while not r.empty:
        if firstLineOfGroup == '' or r.front != firstLineOfGroup:
            if firstLineOfGroup != '':
                out >> put(_, (firstLineOfGroup, count))
            count = 0
            firstLineOfGroup = r.front
        count += 1
        r.popFront()

    if firstLineOfGroup != '':
        out >> put(_, (firstLineOfGroup, count))

    return out.list



def countLinesRanges2(f):
    out = ListOR([])
    r = FileLineIR(f)
    while not r.empty:
        count = r >> countEquals(_, firstLineOfGroup := r.front)
        out >> put(_, (firstLineOfGroup, count))
    return out.list


@coppertop
def countEquals(r, value):
    count = 0
    while not r.empty and r.front == value:
        count += 1
        r.popFront()
    return count



def countLinesRanges3(f):
    return FileLineIR(f) >> rRepititionCounts >> pushAllTo >> ListOR([]) >> getAttr(_, 'list')


@coppertop
def rRepititionCounts(r):
    return RepititionCountIR(r)

class RepititionCountIR(IInputRange):
    def __init__(self, r):
        self.r = r
    @property
    def empty(self):
        return self.r.empty
    @property
    def front(self):
        firstInGroup = self.r.front
        count = 0
        while not self.r.empty and self.r.front ==firstInGroup:
            count += 1
            self.r.popFront()
        return firstInGroup, count
    def popFront(self):
        pass



# "Jackson criticises the traditional version, claiming that it hides the relationships which exist between the
# input lines, compromising the program's understandability and maintainability by, for example, forcing the use
# of a special case for the first line and forcing another special case for a final output operation."

def countLinesJsp(f):
    answer = []

    line = f.readline()
    while line != '':
        count = 0
        firstLineOfGroup = line

        while line != '' and line == firstLineOfGroup:
            count += 1
            line = f.readline()
        answer.append((firstLineOfGroup, count))

    return answer
