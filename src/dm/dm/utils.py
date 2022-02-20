# **********************************************************************************************************************
#
#                             Copyright (c) 2017-2021 David Briant. All rights reserved.
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
from coppertop.std import each, joinAll


# print(items >> sig)

@coppertop
def formatStruct(s, name, keysFormat, valuesFormat, sep):
    def formatKv(kv):
        k,v = kv
        k = k if isinstance(k, str) else format(k, keysFormat)
        v = v if isinstance(v, str) else format(v, valuesFormat)
        return f'{k}={v}'
    return f'{name}({list(s._nvs()) >> each >> formatKv >> joinAll(_,sep)})'
    # return f'{name}({s >> nvs >> each >> formatKv >> join >> sep})'

