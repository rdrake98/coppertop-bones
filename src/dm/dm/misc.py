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

from coppertop.core import Missing

import numpy


def sequence(p1, p2, n=Missing, step=Missing, sigmas=Missing):
    if step is not Missing and n is not Missing:
        raise TypeError('Must only specify either n or step')
    if step is Missing and n is Missing:
        first , last = p1, p2
        return list(range(first, last+1, 1))
    elif n is not Missing and sigmas is not Missing:
        mu, sigma = p1, p2
        low = mu - sigmas * sigma
        high = mu + sigmas * sigma
        return sequence(low, high, n=n)
    elif n is not Missing and sigmas is Missing:
        first , last = p1, p2
        return list(numpy.linspace(first, last, n))
    elif n is Missing and step is not Missing:
        first , last = p1, p2
        return list(numpy.arange(first, last + step, step))
    else:
        raise NotImplementedError('Unhandled case')