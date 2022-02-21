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

from datetime import date

from coppertop.core import Null, PP
from coppertop.pipe import *
from coppertop.std import check, equal, strip, take, not_, _, count, wrapInList, each
from coppertop.std.datetime import addDays, parseDate, toCTimeFormat, day
from bones.core.types import pydate

from coppertop.std.range import EMPTY, getIRIter, ListOR, toIndexableFR, RaggedZipIR, FnAdapterFR, \
    ChunkUsingSubRangeGeneratorFR, pushAllTo
from coppertop.std.range import front, rEach, materialise, rChain

from coppertop.std.examples.format_calendar import datesInYear, monthChunks, weekChunks, weekStrings, monthTitle, \
    monthLines, monthStringsToCalendarRow
from coppertop.std.examples.format_calendar import _untilWeekdayName



YYYY_MM_DD = 'YYYY.MM.DD' >> toCTimeFormat

# see notes in format_calendar.py


@coppertop
def _ithDateBetween(start, end, i):
    ithDate = start >> addDays(_, i)
    return EMPTY if ithDate > end else ithDate

@coppertop(style=binary2)
def datesBetween(start:pydate, end:pydate):
     return FnAdapterFR(_ithDateBetween(start, end, _))



def test_allDaysInYear():
    actual = []
    o = 2020 >> datesInYear >> pushAllTo >> ListOR(actual)
    actual[0] >> check >> equal >> date(2020, 1, 1)
    actual[-1] >> check >> equal >> date(2020, 12, 31)
    [e for e in 2020 >> datesInYear >> getIRIter] >> count >> check >> equal >> 366


def test_datesBetween():
    ('2020.01.16' >> parseDate(_, YYYY_MM_DD)) >> datesBetween >> ('2020.01.29' >> parseDate(_, YYYY_MM_DD)) \
    >> rEach >> day \
    >> materialise >> check >> equal >> [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]


def test_chunkingIntoMonths():
    2020 >> datesInYear \
        >> monthChunks \
        >> materialise \
        >> count \
        >> check >> equal >> 12


def test_checkNumberOfDaysInEachMonth():
    2020 >> datesInYear \
        >> monthChunks \
        >> materialise \
        >> each >> count \
        >> check >> equal >> [31,29,31,30,31,30,31,31,30,31,30,31]


def test__untilWeekdayName():
    r = 2020 >> datesInYear
    dates = [d for d in r >> _untilWeekdayName(_, 'Sun') >> getIRIter]
    dates[-1] >> check >> equal >> date(2020, 1, 5)   # the sunday
    r >> front >> check >> equal >> date(2020, 1, 6) # the monday


def test_WeekChunks():
    datesR = '2020.01.16' >> parseDate(_, YYYY_MM_DD) >> datesBetween >> ('2020.01.29' >> parseDate(_, YYYY_MM_DD))
    weeksR = ChunkUsingSubRangeGeneratorFR(datesR, _untilWeekdayName(_, 'Sun'))
    actual = []
    while not weeksR.empty:
        weekR = weeksR >> front
        actual.append([d >> day for d in weekR >> getIRIter])
        weeksR.popFront()
    actual >> check >> equal >> [[16, 17, 18, 19], [20, 21, 22, 23, 24, 25, 26], [27, 28, 29]]


def test_WeekStrings():
    expectedJan2020 = [
        '        1  2  3  4  5',
        '  6  7  8  9 10 11 12',
        ' 13 14 15 16 17 18 19',
        ' 20 21 22 23 24 25 26',
        ' 27 28 29 30 31      ',
    ]
    weekStringsR = (
        2020 >> datesInYear
        >> monthChunks
        >> front
        >> weekChunks
        >> weekStrings
    )
    weekStringsR2 = weekStringsR.save()
    [ws for ws in weekStringsR >> getIRIter] >> check >> equal >> expectedJan2020

    actual = [ws for ws in weekStringsR2 >> getIRIter]
    if actual >> equal >> expectedJan2020 >> not_:
        "fix WeekStringsRange.save()" >> PP


def test_MonthTitle():
    1 >> monthTitle(_, 21) >> wrapInList >> toIndexableFR \
        >> rEach >> strip >> materialise \
        >> check >> equal >> ['January']


def test_oneMonthsOutput():
    [
        1 >> monthTitle(_, 21) >> wrapInList >> toIndexableFR,
        2020 >> datesInYear
            >> monthChunks
            >> front
            >> weekChunks
            >> weekStrings
    ] >> rChain \
        >> materialise >> check >> equal >> Jan2020TitleAndDateLines

    # equivalently
    check(
        materialise(monthLines(front(monthChunks(datesInYear(2020))))),
        equal,
        Jan2020TitleAndDateLines
    )


def test_firstQuarter():
    2020 >> datesInYear \
        >> monthChunks \
        >> take >> 3 \
        >> RaggedZipIR >> rEach >> monthStringsToCalendarRow(Null, " "*21, " ")



Jan2020DateLines = [
    '        1  2  3  4  5',
    '  6  7  8  9 10 11 12',
    ' 13 14 15 16 17 18 19',
    ' 20 21 22 23 24 25 26',
    ' 27 28 29 30 31      ',
]

Jan2020TitleAndDateLines = ['       January       '] + Jan2020DateLines

Q1_2013TitleAndDateLines = [
    "       January              February                March        ",
    "        1  2  3  4  5                  1  2                  1  2",
    "  6  7  8  9 10 11 12   3  4  5  6  7  8  9   3  4  5  6  7  8  9",
    " 13 14 15 16 17 18 19  10 11 12 13 14 15 16  10 11 12 13 14 15 16",
    " 20 21 22 23 24 25 26  17 18 19 20 21 22 23  17 18 19 20 21 22 23",
    " 27 28 29 30 31        24 25 26 27 28        24 25 26 27 28 29 30",
    "                                             31                  "
]



def main():
    test_allDaysInYear()
    test_datesBetween()
    test_chunkingIntoMonths()
    test_checkNumberOfDaysInEachMonth()
    test__untilWeekdayName()
    test_WeekChunks()
    test_WeekStrings()
    test_MonthTitle()
    test_oneMonthsOutput()
    # test_firstQuarter()


if __name__ == '__main__':
    main()
    print('pass')
