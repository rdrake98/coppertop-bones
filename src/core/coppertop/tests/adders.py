# **********************************************************************************************************************
#
#                             Copyright (c) 2021 David Briant. All rights reserved.
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



from coppertop.pipe import *
from bones.core.types import pyint, pylist

@coppertop
def addOne(x:pyint) -> pyint:
    return x + 1

@coppertop
def eachAddOne(xs:pylist) -> pylist:
    answer = []
    for x in xs:
        answer.append(x >> addOne)
    return answer

@coppertop
def addTwo(x:pyint) -> pyint:
    return x + 2

@coppertop
def eachAddTwo(xs:pylist) -> pylist:
    answer = []
    for x in xs:
        answer.append(x >> addTwo)
    return answer
