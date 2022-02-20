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

import operator
from coppertop.pipe import *
from coppertop.std import inject, each, eachAsArgs, check, equal, to, shape, closeTo
from coppertop.std import matrix
from dm.pmf import pmfMul, normalise, uniform, sequence, mean, PMF, L, values, names



def test_MM():
    bag1994 = PMF(Brown=30, Yellow=20, Red=20, Green=10, Orange=10, Tan=10)
    bag1996 = PMF(Brown=13, Yellow=14, Red=13, Green=20, Orange=16, Blue=24)
    prior = PMF(hypA=0.5, hypB=0.5)
    likelihood = L(
        hypA=bag1994.Yellow * bag1996.Green,
        hypB=bag1994.Green * bag1996.Yellow
    )
    post = prior >> pmfMul >> likelihood >> normalise
    post.hypA >> check >> closeTo >> 20/27

def test_monty():
    prior = PMF(A=1, B=1, C=1)
    likelihood = L(  # i.e. likelihood of monty opening B given that the car is behind each, i.e. p(data|hyp)
        A=0.5,  # prob of opening B if behind A - he can choose at random so 50:50
        B=0,  # prob of opening B if behind B - Monty can't open B else he'd reveal the car, so cannot open B => 0%
        C=1,  # prob of opening B if behind C - Monty can't open C else he'd reveal the car, so must open B => 100%
    )
    posterior = prior >> pmfMul >> likelihood >> normalise
    posterior.C >> check >> closeTo(_,_,tolerance=0.001) >> 0.667


def main():
    test_MM()
    test_monty()

if __name__ == '__main__':
    main()
    print('pass')

