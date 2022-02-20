# **********************************************************************************************************************
#
#                             Copyright (c) 2022 David Briant. All rights reserved.
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

from bones.core.metatypes import BTAtom, S
from coppertop.std import tvstruct
from coppertop.core import Missing
from bones.core.types import pydict, count, pystr


card = BTAtom.ensure('card')
handId = BTAtom.ensure('handId')
ndmap = BTAtom.ensure('ndmap')
pad_element = S(has=pystr, suggestions=count, like=count)
cluedo_pad = ((card*handId)**pad_element)[ndmap] & BTAtom.ensure('cluedo_pad')
cluedo_pad = pydict #& BTAtom.ensure('cluedo_pad') once we have tvmao we can do this
cluedo_bag = (tvstruct & BTAtom.ensure('_cluedo_bag')).nameAs('cluedo_bag')


YES = 'X'
NO = '-'
MAYBE = '?'
TBI = 'TBI'     # the hand with the people, weapon and room - To Be Inferred

class HasOne(object):
    def __init__(self, handId=Missing):
        self.handId = handId
    def __rsub__(self, handId):     # handId / has
        assert self.handId == Missing, 'Already noted a handId'
        return HasOne(handId)
one = HasOne()

