# **********************************************************************************************************************
#
#                             Copyright (c) 2020-2021 David Briant. All rights reserved.
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



from coppertop.pipe import *
from coppertop.testing import assertRaises
from coppertop.std import _, check, equal


def prettyArgs(*args):
    return ', '.join([str(arg) for arg in args])


@coppertop(style=nullary)
def nullary0():
    return 'nullary0'

@coppertop(style=nullary)
def nullary1(a):
    return f'nullary1({prettyArgs(a)})'

@coppertop(style=nullary)
def nullary2(a, b):
    return f'nullary2({prettyArgs(a, b)})'

@coppertop
def unary1(a):
    return f'unary1({prettyArgs(a)})'

@coppertop
def unary2(a, b):
    return f'unary2({prettyArgs(a, b)})'

@coppertop
def unary3(a, b, c):
    return f'unary3({prettyArgs(a, b, c)})'

@coppertop(style=rau)
def rau1(a):
    return f'rau1({prettyArgs(a)})'

@coppertop(style=rau)
def rau2(a, b):
    return f'rau2({prettyArgs(a, b)})'

@coppertop(style=rau)
def rau3(a, b, c):
    return f'rau3({prettyArgs(a, b, c)})'

@coppertop(style=binary)
def binary2(a, b):
    return f'binary2({prettyArgs(a, b)})'

@coppertop(style=binary)
def binary3(a, b, c):
    return f'binary3({prettyArgs(a, b, c)})'

@coppertop(style=ternary)
def ternary3(a, b, c):
    return f'ternary3({prettyArgs(a, b, c)})'



def testNullary():
    str(nullary1(1)) >> check >> equal >> 'nullary1(1)'
    str(nullary2(1, _)) >> check >> equal >> 'nullary2(1, TBC{})'
    str(nullary2(1, _)(2)) >> check >> equal >> 'nullary2(1, 2)'

    with assertRaises(SyntaxError) as e:
        nullary1(_)(1, 2)
    e.exceptionValue.args[0] >> check >> equal >> 'nullary1 - too many args - got 2 needed 1'

    with assertRaises(SyntaxError) as e:
        2 >> nullary2(1, _)
    e.exceptionValue.args[0] >> check >> equal >> 'syntax not of form nullary()'


def testUnary():
    str(unary1(1)) >> check >> equal >> 'unary1(1)'
    str(unary2(1, _)) >> check >> equal >> 'unary2(1, TBC{})'
    str(2 >> unary2(1, _)) >> check >> equal >> 'unary2(1, 2)'

    with assertRaises(SyntaxError) as e:
        unary1(_)(1, 2)
    e.exceptionValue.args[0] >> check >> equal >> 'unary1 - too many args - got 2 needed 1'

    with assertRaises(SyntaxError) as e:
        2 >> unary3(1, _, _)
    e.exceptionValue.args[0] >> check >> equal >> 'unary3 needs 2 args but 1 will be piped'

    str(nullary1(1) >> unary1) >> check >> equal >> 'unary1(nullary1(1))'


def testRau():
    str(rau1(1)) >> check >> equal >> 'rau1(1)'
    str(rau2(1, _)) >> check >> equal >> 'rau2(1, TBC{})'
    str(rau2(1, _) >> 2) >> check >> equal >> 'rau2(1, 2)'

    with assertRaises(SyntaxError) as e:
        rau1(_)(1, 2)
    e.exceptionValue.args[0] >> check >> equal >> 'rau1 - too many args - got 2 needed 1'

    with assertRaises(SyntaxError) as e:
        rau3(1, _, _) >> 2
    e.exceptionValue.args[0] >> check >> equal >> 'needs 2 args but 1 will be piped'

    str(rau1 >> 1) >> check >> equal >> 'rau1(1)'
    str(rau1 >> nullary1(1)) >> check >> equal >> 'rau1(nullary1(1))'

    with assertRaises(TypeError) as e:
        rau1 >> unary1
    with assertRaises(TypeError) as e:
        rau1 >> binary2
    with assertRaises(TypeError) as e:
        rau1 >> ternary3



def testBinary():
    # in python we can't stop partial binding of binaries as we don't have access to the parser
    str(binary2(1, 2)) >> check >> equal >> 'binary2(1, 2)'
    str(1 >> binary3(_, 2, _)) >> check >> equal >> 'binary3(1, 2, TBC{})'
    str(1 >> binary3(_, 2, _) >> 3) >> check >> equal >> 'binary3(1, 2, 3)'
    str(1 >> binary2 >> 2) >> check >> equal >> 'binary2(1, 2)'
    str(1 >> binary2 >> unary1) >> check >> equal >> 'binary2(1, unary1)'



def testTernary():
    # consider the following - it shows that rau, binary, ternary overwrite any function as args r1 or r2
    str([1, 2] >> ternary3 >> binary2 >> [3, 4]) >> check >> equal >> 'ternary3([1, 2], binary2, [3, 4])'
    str([1, 2] >> ternary3 >> binary3(_, 2, _) >> [3, 4]) >> check >> equal >> 'ternary3([1, 2], binary3(TBC{}, 2, TBC{}), [3, 4])'



# def testExamples():
#     join = MultiFunction('join', Binary)
#     mul = MultiFunction('mul', Binary)
#     add = MultiFunction('add', Binary)
#     fred = MultiFunction('fred', Unary)
#     eachBoth = MultiFunction('eachBoth', Ternary)
#     each = MultiFunction('each', Binary)
#     inject = MultiFunction('inject', Binary)
#
#     str([1, 2] >> each >> fred) >> check >> equal >> 'each([1, 2], fred)'
#     str([1, 2] >> join >> mul >> fred) >> check >> equal >> 'fred(join([1, 2], mul))'
#     str([1, 2] >> inject(_, 0, _) >> add) >> check >> equal >> 'inject([1, 2], 0, add)'
#     str([1, 2] >> eachBoth >> mul >> [2, 4] >> fred) >> check >> equal >> 'fred(eachBoth([1, 2], mul, [2, 4]))'
#
#     with assertRaises(SyntaxError) as e:
#         [1, 2] >> each(_, fred)
#     e.exceptionValue.args[0] >> check >> equal >> 'needs 1 args but 2 will be piped'



def main():
    testNullary()
    testUnary()
    testRau()
    testBinary()
    testTernary()
    # testExamples()


if __name__ == '__main__':
    main()
    print('pass')


