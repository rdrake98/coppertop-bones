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

# A python implementation of  https://wiki.dlang.org/Component_programming_with_ranges

from datetime import date
from coppertop.core import Null
from coppertop.pipe import *
from coppertop.std import count, _, pad, join, wrapInList, to, joinAll
from coppertop.std.datetime import day, weekday, weekdayName, monthLongName, addDays
from coppertop.range import ChunkUsingSubRangeGeneratorFR, FnAdapterFR, ChunkFROnChangeOf, IForwardRange, \
    EMPTY, toIndexableFR, rEach, rUntil, rChain, replaceWith, RaggedZipIR, materialise
from bones.core.types import pystr

@coppertop
def datesInYear(year):
     return FnAdapterFR(_ithDateInYear(year, _))
@coppertop
def _ithDateInYear(year, i):
    ithDate = date(year, 1, 1) >> addDays(_, i)
    return EMPTY if ithDate.year != year else ithDate


@coppertop
def monthChunks(datesR):
    return ChunkFROnChangeOf(datesR, lambda x: x.month)


@coppertop
def _untilWeekdayName(datesR, wdayName):
    return datesR >> rUntil >> (lambda d: d >> weekday >> weekdayName == wdayName)
@coppertop
def weekChunks(r):
    return ChunkUsingSubRangeGeneratorFR(r, _untilWeekdayName(_, 'Sun'))


@coppertop
def dateAsDayString(d):
    return d >> day >> to(_,pystr) >> pad(_, right=3)


class WeekStringsRange(IForwardRange):
    def __init__(self, rOfWeeks):
        self.rOfWeeks = rOfWeeks

    @property
    def empty(self):
        return self.rOfWeeks.empty

    @property
    def front(self):
        # this exhausts the front week range
        week = self.rOfWeeks.front
        startDay = week.front >> weekday
        preBlanks = ['   '] * startDay
        dayStrings = week >> rEach >> dateAsDayString >> materialise
        postBlanks = ['   '] * (7 - ((dayStrings >> count) + startDay))
        return (preBlanks + dayStrings + postBlanks) >> joinAll

    def popFront(self):
        self.rOfWeeks.popFront()

    def save(self):
        # TODO delete once we've debugged the underlying save issue
        return WeekStringsRange(self.rOfWeeks.save())
weekStrings = coppertop(style=unary1, newName='weekStrings')(WeekStringsRange)

@coppertop
def monthTitle(month, width):
    return month >> monthLongName >> pad(_, center=width)


@coppertop
def monthLines(monthDays):
    return [
        monthDays.front.month >> monthTitle(_, 21) >> wrapInList >> toIndexableFR,
        monthDays >> weekChunks >> weekStrings
    ] >> rChain


@coppertop
def monthStringsToCalendarRow(strings, blank, sep):
    return strings >> materialise >> replaceWith(Null, blank) >> join(_, sep)


def pasteBlocks(rOfMonthChunk):
    return rOfMonthChunk >> RaggedZipIR >> rEach >> monthStringsToCalendarRow(" "*21, " ")

