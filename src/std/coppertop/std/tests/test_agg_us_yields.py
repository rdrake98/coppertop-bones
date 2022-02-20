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



import os

from coppertop.std import _, join, startsWith, inject, to, take, tvarray, names, fromCsv, drop, agg, at, \
    atPut, select, stats, check, different, sameShape
import coppertop.std.vec as vec
from bones.core.types import pydate, pyfloat

path = os.path.dirname(os.path.abspath(__file__))


def test():
    renames = {
        'Date'  : 'date',
        '1 Mo'  : '_1m',
        '2 Mo'  : '_2m',
        '3 Mo'  : '_3m',
        '6 Mo'  : '_6m',
        '1 Yr'  : '_1y',
        '2 Yr'  : '_2y',
        '3 Yr'  : '_3y',
        '5 Yr'  : '_5y',
        '7 Yr'  : '_7y',
        '10 Yr' : '_10y',
        '20 Yr' : '_20y',
        '30 Yr' : '_30y'
    }


    conversions = dict(
        date=vec.to(_, pydate, 'MM/DD/YY'),
        _1m=vec.to(_, pyfloat),
        _2m=vec.to(_, pyfloat),
        _3m=vec.to(_, pyfloat),
        _6m=vec.to(_, pyfloat),
        _1y=vec.to(_, pyfloat),
        _2y=vec.to(_, pyfloat),
        _3y=vec.to(_, pyfloat),
        _5y=vec.to(_, pyfloat),
        _7y=vec.to(_, pyfloat),
        _10y=vec.to(_, pyfloat),
        _20y=vec.to(_, pyfloat),
        _30y=vec.to(_, pyfloat),
    )


    filename = 'us yields.csv'
    ytms = (path + '/' + filename) >> fromCsv(_, renames, conversions)

    # take logs
    ytms2 = ytms \
        >> names >> drop >> ['date', '_2m'] \
        >> inject(_, agg(ytms), _) >> (lambda prior, name:
            prior >> atPut(_,
                'log' >> join >> (name >> drop >> 1),
                prior >> at(_, name) >> vec.log
            )
        )


    # select the desired date range
    d1 = '2021.01.01' >> to(_, pydate, 'YYYY.MM.DD')
    d2 = '2021.04.01' >> to(_, pydate, 'YYYY.MM.DD')
    usD1ToD2 = ytms2 >> select >> (lambda r: d1 <= r.date and r.date < d2)


    # diff and calc covariance matrices
    usDiffs = usD1ToD2 \
        >> names >> drop >> 'date' \
        >> inject(_, agg(), _) >> (lambda p, f:
            p >> atPut(_, f, usD1ToD2 >> at(_, f) >> vec.diff)
        )

    t1 = usDiffs >> names
    t2 = t1 >> select >> startsWith(_, '_')

    usDiffCov = usDiffs \
        >> take >> (usDiffs >> names >> select >> startsWith(_, '_')) \
        >> to(_, tvarray) >> stats.core.cov

    usLogDiffCov = usDiffs \
        >> take >> (usDiffs >> names >> select >> startsWith(_, 'log')) \
        >> to(_, tvarray) >> stats.core.cov

    usDiffCov >> check >> sameShape >> usLogDiffCov
    usDiffCov >> check >> different >> usLogDiffCov



def main():
    test()


if __name__ == '__main__':
    main()
    print('pass')

