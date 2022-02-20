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

from coppertop.core import PP, Missing
from coppertop.pipe import *
from bones.core.types import N, num, aliased, anon, pytuple, pylist, tv, named
from bones.core.metatypes import BTAtom, cacheAndUpdate, fitsWithin as _fitsWithin
from coppertop.std import tvarray, check, equal



matrix = N**N**num

colvec = matrix['colvec']
rowvec = matrix['rowvec']

square = BTAtom.ensure('square')

colmaj = BTAtom.ensure('colmaj').setImplicit
rowmaj = BTAtom.ensure('rowmaj').setOrthogonal



lol = BTAtom.ensure('lol').setConstructor(tv)

_matrix = matrix & tvarray
_colvec = _matrix & colvec
_rowvec = _matrix & rowvec

_llmatrix = (matrix & lol).setConstructor(tv)        # lol is a tvseq of tvseq, i.e. ragged array that we are making regular
_llcolvec = _llmatrix & colvec
_llrowvec = _llmatrix & rowvec

_lmatrix = matrix & pylist  # store the matrix in a linear fashion starting with n, m (colmaj and possibly transposed are in type)
_lcolvec = matrix & pylist
_lrowvec = matrix & pylist

# square and transposed is more of a dynamic / contingent type than a static type on the value but is static in
# terms of function sig and binding and sometimes static in terms of dispatch


@coppertop(style=unary1)
def T(A: _matrix) -> _matrix:
    return A.T


@coppertop(style=unary1)
def T(A: _llmatrix & aliased & colmaj) -> _llmatrix & anon & colmaj:
    answer = lol(A >> shape, colmaj)
    for i, col in enumerate(A):
        answer
    return answer


@coppertop(style=unary1)
def T(A: _llmatrix & anon & colmaj) -> _llmatrix & anon & colmaj:
    sh = A >> shape
    if sh[0] == sh[1]:
        A | +square >> T  # dispatch to T(A:_lmatrix & anon & colmaj & square)
    else:
        A | -anon >> T  # dispatch to T(A:_lmatrix & aliased & colmaj)


@coppertop(style=unary1)
def T(A: _llmatrix & anon & colmaj & square) -> _llmatrix & anon & colmaj & square:
    answer = lol(A >> shape, colmaj)
    for i, col in enumerate(A):
        answer
    return answer


@coppertop(style=unary1)
def T(A: _llmatrix & aliased & rowmaj) -> _llmatrix & anon & rowmaj:
    answer = [[]]
    for i in x:
        answer
    return answer


@coppertop(style=unary1)
def T(A: _llmatrix & anon & rowmaj) -> _llmatrix & anon & rowmaj:
    for i in x:
        A
    return A


@coppertop(style=unary1)
def T(A: _llmatrix & named & colmaj) -> _llmatrix & anon & colmaj:
    old = A._v
    new = [[] for r in old[0]]
    for i, col in enumerate(old):
        for j, e in enumerate(col):
            new[j].append(e)
    return tv(_llmatrix & anon, new)


@coppertop(style=unary1)
def shape(A: _lmatrix) -> pytuple:
    return tuple(A[0:2])

@coppertop(style=unary1)
def shape(A: _llmatrix) -> pytuple:
    lol = A._v
    return (len(lol[0]) if len(lol) > 0 else 0, len(lol))


def main():
    A = _llmatrix([[1, 2, 3], [3, 4, 5]]) | +named
    A >> shape >> PP
    A >> T >> PP >> shape >> check >> equal >> (2, 3)

# facts
# B: A causes both A and B to change type to aliased
# A's type is now aliased+named+anon as before it was named or anon
# AST Node results can be anon but A (upon assignment can only be named)
# any value addressable in a container is "named", e.g. A: (1,2,3)  - each element is "named"

# can tranpose as a type be static? no - consider rand(1,6) timesRepeat: [A: A T]?



if __name__ == '__main__':
    main()
    print('pass')
