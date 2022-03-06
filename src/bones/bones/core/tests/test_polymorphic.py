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

from coppertop.core import NotYetImplemented
from coppertop.pipe import *
from coppertop.pipe import selectDispatcher
from coppertop.std.structs import tvseq
from coppertop.std import check, equal, fitsWithin, doesNotFitWithin

from bones.core.types import num, pystr, N, T1, T2, T3, T4, pyint, ascii
from bones.core.metatypes import BTAtom, hasT, determineRetType

tFred = BTAtom.ensure('fred')
tJoe = BTAtom.ensure('joe')
tSally = BTAtom.ensure('sally')


# we need macro expansion in order to dispatch on the return value of `each`, e.g. see testExample()

def _eachHelper(xs:(N**T1)[tvseq], f:T1^T2, tByT) -> dict:
    t1 = tByT[T1]
    d, tByT_f = selectDispatcher(f, (t1,))
    t2 = d.retType
    if hasT(t2):
        raise NotYetImplemented()
    answer = dict(tByT)
    answer[T2] = t2
    return answer

@coppertop(style=binary2, typeHelper=_eachHelper)
def each_(xs:(N**T1)[tvseq], f:T1^T2, tByT) -> (N**T2)[tvseq]:
    fxs = [f(x) for x in xs]
    return tvseq((N**tByT[T2])[tvseq], fxs)


def _polyAddOneHelper(x:T1):
    sigCaller = (typeOf(x), )
    d_addOne2, tByT = selectDispatcher(addOne2, sigCaller)   # T could be T1, T2 etc as is defined by each addOne2 impl
    retT = determineRetType(d_addOne2, tByT, sigCaller)
    return retT

@coppertop(typeHelper=_polyAddOneHelper)
def polyAddOne(x:T1) -> T2:
    return x >> addOne2

@coppertop
def addOne2(x:pyint) -> pyint:
    '''addOne2(pyint) -> pyint'''
    return x + 1

@coppertop
def addOne2(x:pystr) -> pystr:
    '''addOne2(pystr) -> pystr'''
    return x + "One"

@coppertop
def _addOne2(x:pystr) -> pystr:
    '''_addOne2(pystr) -> pystr'''
    return x + "One"

@coppertop(style=unary1)
def fredU1(x:pystr) -> pystr:
    '''fredU1(pystr) -> pystr'''
    return x + "One"

@coppertop(style=binary2)
def fredB2(x:pystr, y:pystr) -> pystr:
    '''fredB2(pystr, pystr) -> pystr'''
    return x + y

@coppertop
def PP(x:(N**pyint)[tvseq]) -> pystr:
    return f'tvseq of {len(x)} pyint'

@coppertop
def PP(x:(N**pystr)[tvseq]) -> pystr:
    return f'tvseq of {len(x)} pystr'



def testSelectDispatcher():
    # via the function interface
    d, tByT = addOne2(pyint)
    d.__doc__ >> check >> equal >> 'addOne2(pyint) -> pyint'

    # test for md
    d, tByT = selectDispatcher(addOne2, (pystr,))
    d.__doc__ >> check >> equal >> 'addOne2(pystr) -> pystr'

    # test for sd
    d, tByT = selectDispatcher(_addOne2, (pystr,))
    d.__doc__ >> check >> equal >> '_addOne2(pystr) -> pystr'

    # test for u1
    d, tByT = selectDispatcher(fredU1, (pystr,))
    d.__doc__ >> check >> equal >> 'fredU1(pystr) -> pystr'

    # test for b2
    d, tByT = selectDispatcher(fredB2, (pystr, pystr))
    d.__doc__ >> check >> equal >> 'fredB2(pystr, pystr) -> pystr'


def testSignatureFitsWithin():
    (pyint ^ pyint) >> check >> fitsWithin >> (T1 ^ T2)
    with context(halt=True):
        (pyint ^ pyint) + (pystr ^ pystr) >> check >> fitsWithin >> (T1 ^ T2)



def testOverloaded():
    d1, tByT1 = each_((N ** pyint)[tvseq], addOne2(pyint).d._t)
    d2, tByT2 = each_((N ** pyint)[tvseq], addOne2._t)
    assert d2.module == '__main__' or d2.module == 'bones.core.tests.test_polymorphic'

    xs = tvseq((N ** pyint)[tvseq], [1, 2, 3])
    fxs = xs >> each_ >> addOne2
    fxs >> check >> typeOf >> (N**pyint)[tvseq]



def testPolyFitsWithin():
    (T1 ^ T2) >> fitsWithin >> (T1 ^ T2)
    with context(halt=True):
        (T2 ^ T1) >> doesNotFitWithin >> (T1 ^ T2)      # unless T1 == T2?
        (T1 ^ T1) >> fitsWithin >> (T1 ^ T2)
        (T1 ^ T2) >> fitsWithin >> (T3 ^ T4)
        (num ^ T2) >> fitsWithin >> (T3 ^ T4)
        (num ^ T2) >> fitsWithin >> (num ^ T4)
        (num ^ num) >> fitsWithin >> (num ^ T4)
        (num ^ num) >> fitsWithin >> (num ^ num)

        (T1 ^ T2) >> doesNotFitWithin >> (num ^ T4)           # partial fit
        (num+ascii ^ T2) >> doesNotFitWithin >> (num ^ T4)    # partial fit


def testPolymorhpic():
    xs = tvseq((N**pyint)[tvseq], [1, 2, 3])
    fxs = xs >> each_ >> polyAddOne
    fxs >> check >> typeOf >> (N**pyint)[tvseq]

    xs = tvseq((N ** pystr)[tvseq], ['One', 'Two', 'Three'])
    fxs = xs >> each_ >> polyAddOne
    fxs >> check >> typeOf >> (N ** pystr)[tvseq]

    xs = tvseq((N ** (pyint+pystr))[tvseq], [1, 'Two', 3])
    fxs = xs >> each_ >> polyAddOne
    fxs >> check >> typeOf >> (N ** (pyint+pystr))[tvseq]


def testExample():
    tvseq((N ** pyint)[tvseq], [1, 2, 3]) >> each_ >> polyAddOne >> PP >> check >> equal >> 'tvseq of 3 pyint'
    tvseq((N ** pystr)[tvseq], ['One', 'Two', 'Three']) >> each_ >> polyAddOne >> PP >> check >> equal >> 'tvseq of 3 pystr'



def main():
    testSelectDispatcher()
    testSignatureFitsWithin()
    testOverloaded()
    # testPolyFitsWithin()
    # testPolymorhpic()
    # testExample()


if __name__ == '__main__':
    main()
    print('pass')
