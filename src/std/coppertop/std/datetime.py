# **********************************************************************************************************************
#
#                             Copyright (c) 2017-2020 David Briant. All rights reserved.
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

# SHOULDDO handle locales


import sys
if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)


from _strptime import _strptime
import datetime
from coppertop.core import Missing
from coppertop.pipe import *
from bones.core.types import pystr, pyint, pydate


@coppertop
def year(x):
    return x.year

@coppertop
def month(x):
    return x.month

@coppertop
def day(x):
    return x.day

@coppertop
def hour(x):
    return x.hour

@coppertop
def minute(x):
    return x.minute

@coppertop
def second(x):
    return x.second

@coppertop
def weekday(x):
    return x.weekday()

@coppertop
def weekdayName(x, locale=Missing):
    return ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][x]

@coppertop
def weekdayLongName(x, locale=Missing):
    return ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][x]

@coppertop
def monthName(month, locale=Missing):
    return ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][month - 1]

@coppertop
def monthLongName(month, locale=Missing):
    return ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'][month - 1]

@coppertop
def parseDate(x:pystr, cFormat:pystr) -> pydate:
    # rework to be more efficient in bulk by parsing format separately from x or handle x as an array / range
    dt, micro, _ = _strptime(x, cFormat)
    return datetime.date(dt[0], dt[1], dt[2])

@coppertop
def toCTimeFormat(simpleFormat:pystr) -> pystr:

    # a little care is needed here to avoid clashes between formats
    answer = simpleFormat
    answer = answer.replace('DDDD', '%A')
    answer = answer.replace('DDD', '%a')
    answer = answer.replace('DD', '%d')
    answer = answer.replace('D', '%e')

    answer = answer.replace('YYYY', '%Y')
    answer = answer.replace('YY', '%y')

    answer = answer.replace('ms', '%f')                             # Microsecond as a decimal number, zero-padded to 6 digits
    answer = answer.replace('us', '%f')

    answer = answer.replace('mm', '%M')
    answer = answer.replace('m', '%-M')

    answer = answer.replace('ms', '%f')                             # Microsecond as a decimal number, zero-padded to 6 digits
    answer = answer.replace('us', '%f')

    answer = answer.replace('ss', '%S')
    answer = answer.replace('s', '%<single-digit-second>')

    answer = answer.replace('MMMM', '%B')                           # Month as locale’s full name
    answer = answer.replace('MMM', '%b')                            # Month as locale’s abbreviated name
    answer = answer.replace('MM', '%m')                             # Month as a zero-padded decimal number
    answer = answer.replace('M', '%<single-digit-month>')
    answer = answer.replace('%%<single-digit-month>', '%M')
    answer = answer.replace('%-%<single-digit-month>', '%-M')

    answer = answer.replace('hh', '%H')                             # 0 padded 12 hour
    answer = answer.replace('h', '%-H')
    answer = answer.replace('HH', '%I')                             # 0 padded 24 hour
    answer = answer.replace('H', '%-I')
    answer = answer.replace('%%-I', '%H')
    answer = answer.replace('%-%-I', '%-H')

    answer = answer.replace('TT', '%p')                             # Locale’s equivalent of either AM or PM

    answer = answer.replace('city', '%<city>')
    answer = answer.replace('z/z', '%<IANA>')
    answer = answer.replace('z', '%Z')                              # Time zone name (empty string if the object is naive)
    return answer

@coppertop
def addDays(d:pydate, n:pyint):
    return d + datetime.timedelta(n)
