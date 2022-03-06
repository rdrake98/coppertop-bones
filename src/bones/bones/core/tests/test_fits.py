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

from coppertop.pipe import *
from coppertop.std import check, equal, fitsWithin

from bones.core.types import index, count, num, pystr, N,  T, T1, T2, T3, pyint, pyfloat, pylist, pydict
from bones.core.metatypes import BType, BTAtom, S, weaken, cacheAndUpdate, fitsWithin as _fitsWithin


tFred = BTAtom.ensure('fred')
tJoe = BTAtom.ensure('joe')
tSally = BTAtom.ensure('sally')



def testSimple():
    # exact
    num >> fitsWithin >> num >> check >> equal >> True
    num+pystr >> fitsWithin >> num+pystr >> check >> equal >> True

    # T
    num >> fitsWithin >> T >> check >> equal >> True
    num+pystr >> fitsWithin >> T >> check >> equal >> True
    num**num >> fitsWithin >> T >> check >> equal >> True

    # union
    num >> fitsWithin >> pystr+num >> check >> equal >> True
    pystr+num >> fitsWithin >> num >> check >> equal >> False

    # coercion via rules
    pyint >> fitsWithin >> num >> check >> equal >> True
    pyint >> fitsWithin >> pyfloat >> check >> equal >> False
    pyint >> fitsWithin >> index >> check >> equal >> True
    count >> fitsWithin >> index >> check >> equal >> False
    pyfloat >> fitsWithin >> pyint >> check >> equal >> False
    num >> fitsWithin >> pyfloat >> check >> equal >> False
    num >> fitsWithin >> pyfloat >> check >> equal >> False


def testNested():
    from coppertop.std.types import ccy
    GBP = ccy['GBP']
    USD = ccy['USD']
    weaken((pyint, pyfloat, pyint, pyfloat), (ccy[T], GBP, USD))

    pyint >> fitsWithin >> GBP >> check >> equal >> True
    GBP >> fitsWithin >> pyint >> check >> equal >> False
    pyint >> fitsWithin >> ccy >> check >> equal >> False
    pyfloat >> fitsWithin >> ccy[T] >> check >> equal >> True

    num*pystr >> fitsWithin >> (num+pyint)*(pystr+GBP) >> check >> equal >> True
    # (num, pystr) >> fitsWithin >> ((num + pyint), (pystr + GBP)) >> check >> equal >> True
    S(a=num, b=num) >> fitsWithin >> S(a=num) >> check >> equal >> True


def testTemplates():
    fred = BTAtom.ensure('fred')
    num*fred >> fitsWithin >> T*fred >> check >> equal >> True
    pyint*fred >> fitsWithin >> T1*T2 >> check >> equal >> True

    (fred ** N) >> fitsWithin >> (T ** N) >> check >> equal >> True

    # simple wildcards
    (N ** fred)[pylist] >> fitsWithin >> (N ** T1)[T2] >> check >> equal >> True
    (N ** fred)[pylist] >> fitsWithin >> (N ** T)[pydict] >> check >> equal >> False
    (pystr ** fred)[pylist] >> fitsWithin >> (N ** T1)[pylist] >> check >> equal >> False
    (fred ** pystr)[pylist] >> fitsWithin >> (T1 ** T2)[pylist] >> check >> equal >> True
    (fred ** pystr)[pylist] >> fitsWithin >> (T1 ** T2)[T3] >> check >> equal >> True
    (fred ** pystr)[pylist] >> fitsWithin >> (T1 ** T2)[pydict] >> check >> equal >> False
    (fred ** pystr)[pylist] >> fitsWithin >> (T1 ** T1)[pylist] >> check >> equal >> False


def testTemplates2():

    account = pystr['account']
    weaken(pystr, account)

    tvstruct = pystr['tvstruct2']
    pylist = pystr['pylist2']
    positions = (num ** account)[tvstruct]['positions']

    t1 = positions
    t2 = (N**account)[pylist]
    t3 = pyint

    tByT = {}
    r1, tByT, distances = cacheAndUpdate(_fitsWithin(t1, (T2**T1)[tvstruct][T3]), tByT)
    r2, tByT, distances = cacheAndUpdate(_fitsWithin(t2, (N**T1)[pylist]), tByT)
    r3, tByT, distances = cacheAndUpdate(_fitsWithin(t3, T2), tByT)

    assert r1 and r2 and r3

    # dispatch._fitsCache = {}
    tByT = {}
    r4, tByT, distances = cacheAndUpdate(_fitsWithin(t3, T2), tByT)
    r5, tByT, distances = cacheAndUpdate(_fitsWithin(t2, (N**T1)[pylist]), tByT)
    r6, tByT, distances = cacheAndUpdate(_fitsWithin(t1, (T2**T1)[tvstruct][T3]), tByT)

    assert r4 and r5 and r6

    t2 = pystr
    t3 = pyint

    tByT = {}
    r9, tByT, distances = cacheAndUpdate(_fitsWithin(t3, T2, tByT), tByT)
    r8, tByT, distances = cacheAndUpdate(_fitsWithin(t2, T1, tByT), tByT)
    r7, tByT, distances = cacheAndUpdate(_fitsWithin(t1, (T2**T1)[tvstruct][T3], tByT), tByT)

    assert r7
    assert r8
    assert r9



def main():
    testSimple()
    testNested()
    testTemplates()
    testTemplates2()


if __name__ == '__main__':
    main()
    print('pass')

