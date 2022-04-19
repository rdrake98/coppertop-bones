# **********************************************************************************************************************
#
#                             Copyright (c) 2019-2020 David Briant
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
# You should have received a copy of the GNU Affero General Public License along with coppertop-bones. If not, see
# <https://www.gnu.org/licenses/>.
#
# **********************************************************************************************************************

from bones.core.sym import SymTable


def test():
    symbols = SymTable()
    a = symbols.Sym("sally")
    b = symbols.Sym("joe")
    c = symbols.Sym("fred")
    d = symbols.Sym("arthur")

    assert a._id == 0
    assert b._id == 1
    assert c._id == 2
    assert d._id == 3

    assert not symbols._isSorted
    assert a > b
    assert b > c
    assert c > d
    assert symbols._isSorted

    e = symbols.Sym("sally2")
    f = symbols.Sym("joe2")
    g = symbols.Sym("fred2")
    h = symbols.Sym("arthur2")

    assert not symbols._isSorted
    assert e > a
    assert f > b
    assert g > c
    assert h > d
    assert symbols._isSorted

    a2 = symbols.Sym("sally")
    b2 = symbols.Sym("joe")
    c2 = symbols.Sym("fred")
    d2 = symbols.Sym("arthur")

    assert a2 is a
    assert b2 is b
    assert c2 is c
    assert d2 is d

    assert sorted((a,b,c,d)) == [d,c,b,a]



def main():
    test()
    print("pass")


if __name__ == '__main__':
    main()
