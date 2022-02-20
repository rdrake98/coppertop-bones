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

import scipy.linalg, numpy
from coppertop.pipe import *
from coppertop._structs._tvarray import tvarray
from bones.core.types import N, num, offset, pytuple, pylist
from coppertop.std.converting import to         # extended below
from coppertop.std.types import matrix, colvec, rowvec, vec


_matrix = matrix[tvarray]
_colvec = colvec[tvarray]
_rowvec = rowvec[tvarray]

_vec = vec[tvarray].setConstructor(tvarray)

def _to_matrix(t, x) -> _matrix:
    answer = tvarray(t, x)
    ndims = len(answer.shape)
    if ndims == 0:
        if t in (_rowvec, _colvec, _matrix):
            answer.shape = (1, 1)
        else:
            raise TypeError('Huh')
    elif ndims == 1:
        if t in (_colvec, _matrix):
            answer.shape = (answer.shape[0], 1)
            answer = answer._asT(_colvec)
        elif t is _rowvec:
            answer.shape = (1, answer.shape[0])
        else:
            raise TypeError('Huh')
    elif ndims == 2:
        if t is _rowvec and answer.shape[0] != 1:
            raise TypeError('x is not a row vec')
        if t is _colvec and answer.shape[1] != 1:
            raise TypeError('x is not a col vec')
    elif ndims > 2:
        raise TypeError('x has more than 2 dimensions')
    return answer
matrix[tvarray].setConstructor(_to_matrix)
colvec[tvarray].setConstructor(_to_matrix)
rowvec[tvarray].setConstructor(_to_matrix)



@coppertop
def at(xs:_matrix, o:offset):
    return xs[o]

@coppertop
def at(xs:_matrix, os:pylist):
    return xs[os]

@coppertop(style=unary1)
def min(x:_matrix):
    return numpy.min(x)

@coppertop(style=unary1)
def max(x:_matrix):
    return numpy.max(x)

@coppertop(style=ternary)
def both(a: _matrix, f, b:_matrix) -> _matrix:
    with numpy.nditer([a, b, None]) as it:
        for x, y, z in it:
            z[...] = f(x,y)
        return it.operands[2].view(tvarray) | _matrix

@coppertop
# def to(x:pylist, t:matrix[tvarray]) -> matrix[tvarray]:
def to(x:pylist, t:_matrix) -> _matrix:
    return _to_matrix(t, x)

@coppertop
def inv(A:_matrix) -> _matrix:
    return numpy.linalg.inv(A)

@coppertop(style=binary2)
def dot(A:colvec[tvarray], B:colvec[tvarray]) -> num:
    return float(numpy.dot(A, B))

@coppertop(style=binary2)
def solveTriangular(R:_matrix, b:_matrix) -> _matrix:
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.solve_triangular.html
    return scipy.linalg.solve_triangular(R, b).view(tvarray) | _matrix

@coppertop(style=unary1)
def shape(x:_matrix) -> pytuple:
    return x.shape

@coppertop(style=unary1)
def T(A:_matrix) -> _matrix:
    return A.T

__all__ = ['at', 'min', 'max', 'both', 'to', 'inv', 'dot', 'solveTriangular', 'shape', 'T']
