# **********************************************************************************************************************
#
#                             Copyright (c) 2019-2022 David Briant. All rights reserved.
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


from bones.lang.explaining import descriptionByLocationId

class BonesError(Exception):
    def __init__(self, msg, locationId):
        super().__init__(msg)
        self._locationId = locationId
        assert locationId in descriptionByLocationId

class GroupingError(BonesError): pass

class ParsingError(BonesError): pass


# our exception handling should allow locations to be accumulated on unwind so a library programmer can describe
# more precisely the cause and possible solutions to an error

class SrcPtr(object):
    # should be compact?
    def __init__(self, srcId, c1, c2):
        self.srcId = srcId      # u16 64k sources?
        self.c1 = c1            # u24 250MB?
        self.c2 = c2            # u24 250MB?


# coppertop piping etc should use this framework too - hence it lives in core not lang
