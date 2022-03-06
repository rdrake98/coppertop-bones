# **********************************************************************************************************************
#
#                             Copyright (c) 2019-2021 David Briant. All rights reserved.
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
# You should have received a copy of the GNU Affero General Public License along with Foobar. If not, see
# <https://www.gnu.org/licenses/>.
#
# **********************************************************************************************************************

import random
from coppertop.pipe import *
from coppertop.core import PP
from coppertop.testing import assertRaises
from coppertop.std import check, equal, _v, to, drop, fitsWithin, doesNotFitWithin
from coppertop.std.structs import tvarray, tvseq

from bones.core.types import index, count, num, pystr, N, T, \
    T1, T2, T3, pyint, pyfloat, tv, anon, named, aliased, pylist
from bones.core.metatypes import BTAtom, S, _partition, BType,weaken
from coppertop.std.types import ccy, fx
from coppertop.std.linalg import square, right


tFred = BTAtom.ensure('fred')
tJoe = BTAtom.ensure('joe')
tSally = BTAtom.ensure('sally')
pystr2 = BTAtom.ensure('pystr2')
weaken(pystr, (pystr2,))


#
# we have these metatypes - atom, union, intersection, product (tuples and structs), exponential (arrays, maps
# and functions) & distinguished.
#
#
# when we do a A >> fitsWithin >> B we partition the two sets into three parts
#
# B intersect A' - stuff in B but not in A - anything here then it's not a fit
# B intersect A - common stuff, if we only have common stuff then it's an exact fit
# B' intersect A - stuff in A but not in B - we term this the residual
#
#
# when types are in the residual set we allow them to behave in exlusively one of the following ways:
#
# generic - the default of all types, e.g. matrix (i.e. N**N**num), matrix&left, right, upper, lower, orthogonal,
#     identity, diagonal, tridiagonal, banddiagonal, positivedefinite, positivesemidefinite etc
#     all matrix operations are available and some are optimisable. e.g. cov = AT @ A can return identity for the
#     orthogonal case
#     i.e. generics do not prevent matching, thus effectively are discarded from the matching decision
#
# implicit - e.g. anon, named, aliased with aliased as the implicit default, defaults do not prevent matching, and
#     non-defaults can be explicity weakened to the default to provide the right behaviour
#
# orthogonal - e.g. ISIN, CUSIP, inches, cm, all instances in the signature must have the same residual, i.e. like a T1,
#     thus add(num, num) called with (cm, inches) will not match as cm and inches are both orthogonal, and (cm, num) will
#     not match as cm is orthogonal to all other types
#
# explicit - e,g, ccy, fx, anything explicit in a residual results in no match
#
# exclusive - e.g. listOfLists, tvarray, ascii, utf8 (typically classes / structs / values / etc) only one exclusive type
#     may exist in the residual and common. Currently classes are the only exclusive type I can think of - maybe null set,
#     void, missing, are too. But what about void&num?


# generic / vanilla / tags / occasional / unremarkable / exceptional / partial / minor /


matrix = BType('matrix')
tdd = BTAtom.ensure('tdd')

# implicit / contextual
red = BTAtom.ensure('red')
yellow = BTAtom.ensure('yellow')
blue = BTAtom.ensure('blue')
# mouseButton = BTSet([red, yellow, blue], default=blue)


# orthogonal
ISIN = BTAtom.ensure('ISIN').setOrthogonal
CUSIP = BTAtom.ensure('CUSIP').setOrthogonal
inches = BTAtom.ensure('inches').setOrthogonal
cm = BTAtom.ensure('cm').setOrthogonal


# explicit
col = BTAtom.ensure('col').setExplicit
row = BTAtom.ensure('row').setExplicit

GBP = ccy['GBP2'].setCoercer(tv)
USD = ccy['USD2'].setCoercer(tv)


# exclusive
# anything including a python class, e.g. matrix[tvarray]
# pylist = BTAtom.ensure('pylist').setExclusive
lol = BTAtom.ensure('lol').setExclusive         # the type for a list of lists (regular?), e.g. matrix[lol]

(pystr).setConstructor(tv)
(ISIN & pystr).setConstructor(tv)
(CUSIP & pystr).setConstructor(tv)


join_psps = '_join(a:pystr, b:pystr)'
@coppertop(style=binary2)
def _join(a:pystr, b:pystr) -> pystr:
    return join_psps

# is it possible to handle this one automatically (by detecting the orthogonal type)?
# is it desirable from a clarity perspective?
join_pstpst = '_join(a:pystr & T1, b:pystr & T1)'
@coppertop(style=binary2)
def _join(a:pystr & T1, b:pystr & T1) -> pystr:
    return join_pstpst

join_ipsips = '_join(a:ISIN & pystr, b:ISIN & pystr)'
@coppertop(style=binary2)
def _join(a:ISIN & pystr, b:ISIN & pystr) -> pystr:
    return join_ipsips

add_mm = 'add(a:matrix, b:matrix)'
@coppertop(style=binary2)
def add(a:matrix, b:matrix) -> pystr:
    return add_mm

add_msms = 'add(a:matrix&square, b:matrix&square)'
@coppertop(style=binary2)
def add(a:matrix&square, b:matrix&square) -> pystr:
    return add_msms


@coppertop(style=binary2)
def mul(a:matrix & lol, b:matrix & lol) -> pystr:
    return 'a:matrix & lol, b:matrix & lol'


@coppertop(style=unary1)
def cov(a:matrix&tdd) -> pystr:
    # n rows of m variables
    # return a >> T >> mul >> a
    return 'a:matrix'


@coppertop(style=unary1)
def opA(A:matrix&aliased[T1], tByT) -> matrix&anon[T1]:
    return A | (matrix & anon & tByT[T1])

@coppertop(style=unary1)
def opB(A:matrix&aliased[T1], tByT) -> matrix&anon[T1]:
    return A | (matrix & anon & tByT[T1])

@coppertop(style=unary1)
def opB(A:matrix&anon) -> matrix&anon:
    return A



def testPartition():
    _partition((matrix & square).types, (matrix, )) >> check >> equal >> ((square,), (matrix,), (), {})
    _partition((matrix & square).types, (ISIN & CUSIP).types) >> check >> equal >> ((matrix, square,), (), (ISIN, CUSIP), {})
    _partition((pystr & square).types, (pystr2, )) >> check >> equal >> ((square,), (pystr,), (), {pystr:pystr2})
    _partition((pystr2 & square).types, (pystr, )) >> check >> equal >> ((square, pystr2), (), (pystr,), {})


def testExclusive():
    with assertRaises(TypeError) as ex:
        lol & pylist
    (pystr & square) >> check >> fitsWithin >> pystr
    tv(matrix & tdd, [[]]) >> cov >> check >> equal >> 'a:matrix'
    tv(matrix & lol & tdd, [[]]) >> cov >> check >> equal >> 'a:matrix'
    tv(matrix & tvarray & tdd, [[]]) >> cov >> check >> equal >> 'a:matrix'


def testGeneric():
    (matrix & square) >> check >> fitsWithin >> matrix
    matrix >> check >> doesNotFitWithin >> (matrix & square)
    tv(matrix, [[]] ) >> add >> tv(matrix, [[]] ) >> check >> equal >> add_mm
    tv(matrix & right, [[]] ) >> add >> tv(matrix & right, [[]] ) >> check >> equal >> add_mm
    tv(matrix & square, [[]] ) >> add >> tv(matrix & square, [[]] ) >> check >> equal >> add_msms


def testImplicit():
    matrix >> check >> fitsWithin >> (matrix & aliased)
    (matrix & aliased) >> check >> fitsWithin >> matrix
    (matrix & anon) >> check >> fitsWithin >> matrix      # although we might weaken anon to aliased
    (matrix & cm) >> check >> doesNotFitWithin >> matrix
    matrix >> check >> doesNotFitWithin >> (matrix & anon)

    (matrix & named) >> check >> fitsWithin >> matrix

    # show here that named, anon and aliased work as a set i.e.
    lmatrix = (matrix & pylist).setConstructor(tv)
    A = lmatrix([[1, 2], [3, 4]]) | +named
    A2 = A >> opA
    A3 = A2 >> opB      # dispatches to opB(A:matrix&aliased) but is subset of anon
    A4 = (A3 | -anon) >> opB
    A4 >> _v >> check >> equal >> A._v

    A = lmatrix([[1, 2], [3, 4]]) | +named
    A._t >> PP >> check >> fitsWithin >> (lmatrix[T1] >> PP) >> PP


def testOrthogonal():
    (pystr & ISIN) >> check >> doesNotFitWithin >> pystr  # because ISIN is left in the residual
    (pystr & ISIN) >> check >> doesNotFitWithin >> (pystr & CUSIP)  # conflict between ISIN and CUSIP
    (pystr & ISIN) >> check >> fitsWithin >> (pystr & ISIN)
    (pystr & ISIN & square) >> check >> fitsWithin >> (pystr & ISIN)
    (pystr & ISIN) >> check >> fitsWithin >> (pystr & T1)
    (pystr & ISIN) >> check >> doesNotFitWithin >> (pystr & ISIN & T)

    (pystr)('DE') >> _join >> (pystr)('0008402215') >> check >> equal >> join_psps
    (CUSIP & pystr)('DE') >> _join >> (CUSIP & pystr)('0008402215') >> check >> equal >> join_pstpst
    (ISIN & pystr)('DE') >> _join >> (ISIN & pystr)('0008402215') >> check >> equal >> join_ipsips
    with assertRaises(TypeError) as ex:
        (ISIN & pystr)('DE') >> _join >> ('0008402215')


def testExplicit():
    GBP >> check >> fitsWithin >> GBP
    GBP >> check >> fitsWithin >> ccy
    ccy >> check >> fitsWithin >> ccy
    ccy >> check >> doesNotFitWithin >> T                           # ccy is explicit
    ccy >> check >> doesNotFitWithin >> ccy[T]                      # T has nothing
    GBP >> check >> fitsWithin >> ccy[T]                            # T will equal the _GBP part
    (GBP & square) >> check >> fitsWithin >> GBP                    # square is in residual
    (GBP & square) >> check >> fitsWithin >> ccy[T]                 # square is in residual
    (N ** ccy) >> check >> doesNotFitWithin >> (N ** T)
    (N ** GBP) >> check >> fitsWithin >> (N ** ccy[T])


@coppertop(style=binary2)
def mul(c:ccy[T1], f:fx[S(d=ccy[T1], f=ccy[T2])], tByT) -> ccy[T2]:
    return tv(ccy[tByT[T2]], c._v * f._v)

@coppertop(style=binary2)
def mul(c:ccy[T1], f:fx[S(d=ccy[T2], f=ccy[T1])], tByT) -> ccy[T2]:
    return tv(ccy[tByT[T2]], c._v / f._v)

GBPUSD = fx[S(d=GBP, f=USD).setExplicit].setCoercer(tv)

def testExplicitStructs():
    GBPUSD >> check >> doesNotFitWithin >> fx
    GBPUSD >> check >> doesNotFitWithin >> fx[S(d=T1, f=T2)]        # ccy is not explicit in the rhs
    GBPUSD >> check >> fitsWithin >> fx[S(d=ccy[T1], f=ccy[T2])]
    (100 | GBP) >> mul >> (1.30 | GBPUSD) >> check >> equal >> (130 | USD)
    (130 | USD) >> mul >> (1.30 | GBPUSD) >> check >> equal >> (100 | GBP)


def testMisc():
    (pystr & square) >> check >> fitsWithin >> pystr2
    (pystr2 & square) >> check >> doesNotFitWithin >> pystr
    matrix[square,right] >> check >> fitsWithin >> (matrix & right & square)


def testAddAndSubtract():
    A = matrix[tv]([[1,2],[3,4]])
    (A | +square) >> check >> typeOf >> (matrix[tv] & square)
    (A | +square | -matrix[tv]) >> check >> typeOf >> square


def testDrop():
    card = pystr['card']
    cards = (N ** card)[tvseq].setPP('deck').setConstructor(tvseq)
    Gr = 'Green'
    Mu = 'Mustard'
    Or = 'Orchid'
    Pe = 'Peacock'
    Pl = 'Plum'
    Sc = 'Scarlet'
    people = [Gr, Mu, Or, Pe, Pl, Sc] >> to(_, cards)
    people >> drop >> [0, 5] >> _v >> check >> equal >> [Mu, Or, Pe, Pl]


def testTypes():
    (num & anon & col & num) >> check >> fitsWithin >> (col & anon & num)


def testFitsWithin():
    (num & col & anon) >> check >> fitsWithin >> num
    (num & col & anon) >> check >> fitsWithin >> (col & anon)

    num >> check >> doesNotFitWithin >> (num & col & anon)
    (num & col & anon) >> check >> doesNotFitWithin >> (num & col & tdd)
    (num & col & anon) >> check >> doesNotFitWithin >> (num & col & anon & tdd)



def main():
    # testTypes()
    # testFitsWithin()
    testPartition()
    testExclusive()
    testGeneric()
    testOrthogonal()
    testImplicit()
    testMisc()
    testAddAndSubtract()
    testDrop()
    testExplicit()
    testExplicitStructs()

if __name__ == '__main__':
    main()
    print('pass')

