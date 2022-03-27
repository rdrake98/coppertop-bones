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

import sys
# sys._TRACE_IMPORTS = True
if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)


from coppertop.core import Missing, ProgrammerError
from coppertop.testing import assertRaises
from dm.std import check, equal, each, to, joinAll, _, sortUsing, box, tvstruct

from bones.core.metatypes import BTAtom, BType, BTArray, BTMap, BTFn, S, isT
from bones.core.types import Holder, index, count, offset, num, pystr, N, null, T, T1, T2, T3



tFred = BTAtom.ensure('fred')
tJoe = BTAtom.ensure('joe')
tSally = BTAtom.ensure('sally')



def testNominalAndAtoms():
    assert repr(tFred) == 'fred'
    assert tFred == BType('fred')
    assert tFred is BType('fred')

    x = 'hello' >> box | tFred
    assert isinstance(x, tFred)
    assert x._v == 'hello'

    i1 = 1 | index
    assert i1._t == index
    c1 = 1 | count
    assert c1._t == count
    o1 = 1 | offset
    assert o1._t == offset
    n1 = 1 | num
    assert n1._t == num


def testHolder():
    fred = Holder(pystr+int)
    assert fred._st == pystr+int
    with assertRaises(ProgrammerError):
        assert fred._tv == Missing
    with assertRaises(TypeError):
        fred._tv = 'joe'
    with assertRaises(AttributeError):
        fred._st = str
    fred._tv = ('hello' >> box | pystr)
    assert fred._tv._t == pystr
    fred._tv = 1
    assert fred._tv == 1
    assert isinstance(fred._tv, int)
    assert isinstance(fred._tv, int+pystr)


def testBTUnion():
    s = tFred+tJoe

    assert (repr(s) == '(fred + joe)') or (repr(s) == '(joe + fred)')
    assert tFred in s
    assert tSally not in s
    assert tJoe+tFred == s   # summing is commutative

    assert isinstance('hello' >> box | tFred, s)


def testBTTuple():
    p1 = tFred*tJoe
    assert repr(p1) == '(fred * joe)'
    assert p1 != tJoe*tFred              # the product is not commutative
    assert p1 == tFred*tJoe


def testBTArray():
    tArr = N ** (num+null)
    repr(tArr) >> check >> equal >> f'(N ** {num+null})'
    assert isinstance(tArr, BTArray)


def testBTMap():
    tMap = index ** (num+null)
    repr(tMap) >> check >> equal >> f'(index ** {num+null})'
    assert isinstance(tMap, BTMap)


def testBTFn():
    fn = (tSally+null) ^ (tFred*tJoe)
    rep = [tSally, null] \
        >> sortUsing >> (lambda x: x.id) \
        >> each >> (lambda x: x >> to(_, pystr)) \
        >> joinAll(_, ' + ')
    repr(fn) >> check >> equal >> f'(({rep}) -> (fred * joe))'
    assert isinstance(fn, BTFn)


def testStructCreation():
    label = BTAtom.ensure('label').setConstructor(tvstruct)
    title = label(text='My cool Tufte-compliant scatter graph')
    title._keys() == ['text']


def test_hasT():
    assert isT(T)
    assert isT(T1)

    matrix = BTAtom.ensure('matrix2')
    inout = BTAtom.ensure('inout')
    out = BTAtom.ensure('out')
    assert matrix[inout, T1].hasT

    ccy = BType('ccy')
    fx = BType('fx')
    GBP = ccy['GBP']
    USD = ccy['USD']
    assert fx[S(domestic=GBP, foreign=T1)].hasT

    N = BType('N')
    assert (T**N).hasT
    assert ((T*num)^num).hasT
    assert ((num*num)^T).hasT

    assert S(name=T, age=num).hasT
    assert (T**num).hasT
    assert (num**T).hasT
    assert (num**T).hasT

    with assertRaises(TypeError):
        1 | T


def testNaming():
    tUnusualThing = (num+pystr).nameAs('tUnusualThing')
    assert BType('tUnusualThing') == tUnusualThing



def main():
    testNominalAndAtoms()
    testHolder()
    testBTUnion()
    testBTTuple()
    testBTArray()
    testBTMap()
    # testBTFn()
    test_hasT()
    testStructCreation()
    testNaming()


if __name__ == '__main__':
    main()
    print('pass')
