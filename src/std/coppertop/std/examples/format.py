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

from coppertop.pipe import _
from coppertop.std import stdout, format



stdout \
    << (2 >> format(_, '{a:.{0}%}', a=2)) << '\n' \
    << ((10, 2, 123.456) >> format(_, '{2:{0}.{1}f} - {a:.1%}', a=2)) << '\n' \
    << (dict(a=2) >> format(_, '{a:.1%}')) << '\n'

