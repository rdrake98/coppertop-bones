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

import sys
if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)


from coppertop.core import Missing
from coppertop.pipe import *
from bones.core.types import pylist, pytuple, pydict, pystr, pyint


@coppertop
def strip(s, chars=Missing):
    if chars is Missing:
        return s.strip()
    else:
        return s.strip(chars)

@coppertop(style=binary)
def split(s1, s2, maxsplit=Missing):
    if maxsplit is Missing:
        return s1.split(s2)
    else:
        return s1.split(s2, maxsplit)

# @coppertop
# def ljust(s:pystr, n:pyint, pad:pystr=' ') -> pystr:
#     return s.ljust(n, pad)
#
# @coppertop
# def rjust(s:pystr, n:pyint, pad:pystr=' ') -> pystr:
#     return s.rjust(n, pad)
#
# @coppertop
# def cjust(s:pystr, n:pyint, pad:pystr=' ') -> pystr:
#     return s.center(n, pad)

@coppertop
def pad(s: pystr, left:pyint=Missing , right:pyint=Missing, center:pyint=Missing, pad:pystr=' '):
    if right is not Missing:
        return s.rjust(right, pad)
    if center is not Missing:
        return s.center(center, pad)
    return s.ljust(left, pad)

# see https://realpython.com/python-formatted-output/ and https://www.python.org/dev/peps/pep-3101/
@coppertop
def format(arg, f:pystr, **kwargs) -> pystr:
    return f.format(arg, **kwargs)
@coppertop
def format(args:pylist, f:pystr, **kwargs) -> pystr:
    return f.format(*args, **kwargs)
@coppertop
def format(args:pytuple, f:pystr, **kwargs) -> pystr:
    return f.format(*args, **kwargs)
@coppertop
def format(kwargs:pydict, f:pystr) -> pystr:
    return f.format(**kwargs)

@coppertop
def replace(haystack:pystr, needle:pystr, alt:pystr) -> pystr:
    return haystack.replace(needle, alt)