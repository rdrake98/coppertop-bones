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


from coppertop.pipe import *
from coppertop.testing import assertRaises
from bones.core.metatypes import S, fitsWithin as fullFitsWithin
from bones.core.types import T1, T2, tvfloat
from coppertop.std.types import ccy, fx
from coppertop.std import check, fitsWithin




GBP = ccy['GBP'][tvfloat].setCoercer(tvfloat)
USD = ccy['USD'][tvfloat].setCoercer(tvfloat)
tvccy = ccy & tvfloat

GBPUSD = fx[S(domestic=GBP, foreign=USD)].nameAs('GBPUSD')[tvfloat].setCoercer(tvfloat)
fxT1T2 = fx[S(domestic=tvccy[T1], foreign=tvccy[T2])] & tvfloat


@coppertop(style=binary2)
def addccy(a:tvccy[T1], b:tvccy[T1]) -> tvccy[T1]:
    return (a + b) | a._t

@coppertop(style=binary2)
def mul(dom:tvccy[T1], fx:fxT1T2, tByT) -> tvccy[T2]:
    assert dom._t == tvccy[tByT[T1]]
    return (dom * fx) | tvccy[tByT[T2]]

@coppertop(style=binary2)
def mul(dom:tvccy[T2], fx:fxT1T2, tByT) -> tvccy[T1]:
    assert dom._t == tvccy[tByT[T2]]
    return (dom / fx) | tvccy[tByT[T1]]


def testFx():
    a = (100|GBP)
    b = (1.3|GBPUSD)
    cacheId1, fits1, tByT1, distance1 = fullFitsWithin(GBP, tvccy[T1])
    cacheId2, fits2, tByT2, distance2 = fullFitsWithin(GBPUSD, fxT1T2)
    assert (100|GBP) >> mul >> (1.3|GBPUSD) >> addccy >> (20|USD) == (150|USD)
    assert (130|USD) >> mul >> (1.3|GBPUSD) == (100|GBP)

    with assertRaises(TypeError):
        (100|GBP) >> addccy >> (100|USD)

    assert (100|GBP) >> addccy >> (100|GBP) == (200|GBP)




def main():
    testFx()


if __name__ == '__main__':
    main()
    print('Pass')
