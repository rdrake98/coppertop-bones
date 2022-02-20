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

from coppertop.pipe import *
from coppertop.core import NotYetImplemented



# see https://code.kx.com/q/basics/funsql/

@coppertop(style=unary)
def fromselect(listr, defs, byNames, wherePreds):
    raise NotYetImplemented()


@coppertop(style=unary)
def fromreject(listr, wherePreds):
    raise NotYetImplemented()


@coppertop(style=unary)
def fromupdate(defs, byNames, agg, wherePreds):
    raise NotYetImplemented()



def sequenceBreaks(soa, names):
    '''answers a new list with each difference item e.g. hello -> h, e, l, o'''
    raise NotYetImplemented()


def isequenceBreaks(soa, names):
    '''as above but also includes the index of the break'''
    raise NotYetImplemented()


