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

# leave here as needs to be importable without dragging in the whole of coppertop.std

import numpy
from coppertop.core import Missing
from bones.core.metatypes import BType


# see https://en.wikipedia.org/wiki/Tensor
# https://medium.com/@quantumsteinke/whats-the-difference-between-a-matrix-and-a-tensor-4505fbdc576c

# tvarray is not a tensor - see Dan Fleisch - https://www.youtube.com/watch?v=f5liqUk0ZTw&t=447s
# I understand a tensor to be a n dimensional matrix of coefficients with each coefficient corresponding to m vectors in and

# tensors are combination of components and basis vectors

# a scalar is a tensor of rank 0 - size is 1 x 1 x 1 etc

# a vector is a tensor of rank 1 - size is rank x dimensions,
# e.g for 3 dimensions
# [Ax,           (0,0,1)
#  Ab,           (0,1,0)
#  Ac]           (1,0,0)

# a matrix is a tensor of rank 2 - size is n x n for n dimensions
# e.g. for for 2 dimensions
# [Axx, Axy;           (0,1)&(0,1), (0,1)&(1,0)
#  Ayx, Ayy]           (1,0)&(0,1), (1,0)&(1,0)

# a tensor is therefore not a data structure by a data structure with a context



class tvarray(numpy.ndarray):

    def __new__(cls, *args, **kwargs):
        if isinstance(args[0], BType):
            t = args[0]
            args = args[1:]
        else:
            t = Missing
        obj = numpy.asarray(*args, **kwargs).view(cls)
        obj._t_ = t if t else tvarray
        return obj

    def __array_finalize__(self, obj):
        # see - https://numpy.org/doc/stable/user/basics.subclassing.html
        if obj is None: return
        self._t_ = getattr(obj, '_t_', tvarray)

    @property
    def _v(self):
        return self

    @property
    def _t(self):
        return self._t_

    def _asT(self, t):
        self._t_ = t
        return self

    def __rrshift__(self, arg):  # so doesn't get in the way of arg >> func
        return NotImplemented

    def __rshift__(self, arg):  # so doesn't get in the way of func >> arg
        return NotImplemented


    def __or__(self, arg):  # so doesn't get in the way of arg | type
        return NotImplemented

    def __ror__(self, arg):  # disabled so don't get confusing error messages for type | arg (we want a doesNotUnderstand)
        return NotImplemented

    def __repr__(self):
        if type(self._t) is type:
            typename = self._t.__name__
        else:
            typename = str(self._t)
        return f'{typename}({numpy.array2string(self)})'


