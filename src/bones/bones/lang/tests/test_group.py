# **********************************************************************************************************************
#
#                             Copyright (c) 2019-2022 David Briant. All rights reserved.
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

from glob import glob

from coppertop.core import *
from coppertop.testing import assertRaises
from dm.std import assertEquals, PP

from bones.lang import lex
from bones.core.structs import GroupingError
from bones.lang.group import determineGrouping
from bones.core.sym import SymTable


# TODO
#
# GROUP
# blank lines should have indent = 0 - lexer change
# separate tokensInFlight and phrase as the conflation made the requires expression
# add continuation across multiple groups on same line
# add return types
# add binary functions {{x+y}}
# figure when to determine style of functions as needed as input for parser - should cast, i.e. |, be part of grouping?
# add from x.y.z uses (or from use? no, from define?)
# add from x.y.z usedef add, fred
# add syntax error tests
# improve error descriptions
#
# EXPR / PHRASE / PIPE - parse_tokens (lex), parse_groups, parse_pipes
# lex, group, parse_tokens,
# tokenise, group, parse_tokens




def main():
    test_current()
    test_errors()
    test()
    # test_group_bones_files()
    print("pass")


def test_current():
    src = r'''     
        
        requires 
            a
            
    '''
    tokens, lines = lex.lexBonesSrc(src, SymTable())
    snippet = determineGrouping(tokens)
    pp = snippet.PPGroup
    pp >> assertEquals >> '{I}'


def test_errors():
    src = '''
        {[] x}
    '''
    tokens, lines = lex.lexBonesSrc(src, SymTable())
    with assertRaises(GroupingError) as ex:
        determineGrouping(tokens)
    ex.exceptionValue.args[0] >> PP


    src = '''
        fred: {[a <:int>, b <:float>] ^ z <:string>}
    '''
    tokens, lines = lex.lexBonesSrc(src, SymTable())
    with assertRaises(GroupingError) as ex:
        determineGrouping(tokens)
    ex.exceptionValue.args[0] >> PP

    src = r'''     
            requires 

        '''
    tokens, lines = lex.lexBonesSrc(src, SymTable())
    with assertRaises(GroupingError) as ex:
        snippet = determineGrouping(tokens)
    ex.exceptionValue.args[0] >> PP

    src = r'''requires'''
    tokens, lines = lex.lexBonesSrc(src, SymTable())
    with assertRaises(GroupingError) as ex:
        snippet = determineGrouping(tokens)
    ex.exceptionValue.args[0] >> PP


    src = r'''     
            requires 
                dm.std,
        '''
    tokens, lines = lex.lexBonesSrc(src, SymTable())
    with assertRaises(GroupingError) as ex:
        snippet = determineGrouping(tokens)
    ex.exceptionValue.args[0] >> PP


    src = r'''     
            requires 
                dm.std,    
            fred * joe
        '''
    tokens, lines = lex.lexBonesSrc(src, SymTable())
    with assertRaises(GroupingError) as ex:
        snippet = determineGrouping(tokens)
    ex.exceptionValue.args[0] >> PP



def test():

    src = '''
        a ifTrue: 1
        b do: 2
    '''
    tokens, lines = lex.lexBonesSrc(src, SymTable())
    snippet = determineGrouping(tokens)
    pp = snippet.PPGroup
    pp >> assertEquals >> 'n (n, l). n (n, l)'


    src = '''
        a: (1,2,3; 4,5,6) each {[x :count+index+offset, y : count, z: count, other:num] x + y}(,1,2,3)
        a each {x*2} <:matrix> 
    '''
    tokens, lines = lex.lexBonesSrc(src, SymTable())
    snippet = determineGrouping(tokens)
    pp = snippet.PPGroup
    pp >> assertEquals >> '(l, l, l; l, l, l) n {[n:t, n:t, n:t, n:t] n o n} (, l, l, l) {:a}. n n {n o l} t'


    # a: a was returning '{a:} (, n)' rather than '{a:} n'
    src = 'b: a. b: 2. b: 2 + a. a: 2 + 1. a'
    tokens, lines = lex.lexBonesSrc(src, SymTable())
    snippet = determineGrouping(tokens)
    pp = snippet.PPGroup
    pp >> assertEquals >> 'n {:b}. l {:b}. l o n {:b}. l o l {:a}. n'


    # ensure missing elements are captured - vital for partial syntax
    src = '''
        ()
        ("one thing")
    '''
    tokens, lines = lex.lexBonesSrc(src, SymTable())
    snippet = determineGrouping(tokens)
    pp = snippet.PPGroup
    pp >> assertEquals >> '(). (l)'


    # ensure missing elements are captured - vital for partial syntax
    src = '''
        ( , )
        (,,)
        (;)
        (;;)
        [;,]
    '''
    tokens, lines = lex.lexBonesSrc(src, SymTable())
    snippet = determineGrouping(tokens)
    pp = snippet.PPGroup
    pp >> assertEquals >> '(, ). (, , ). (; ). (; ; ). [; , ]'


    # simple optional terminator
    src = '''
        a: 1
        b: 2
    '''
    tokens, lines = lex.lexBonesSrc(src, SymTable())
    snippet = determineGrouping(tokens)
    pp = snippet.PPGroup
    pp >> assertEquals >> 'l {:a}. l {:b}'


    src = '''
        {a: [expr *] -> [expr *]:a}
        a: getInt[] <:float>                // type coercion
        10 <:float> :x  <:int> :y * 2 :z
        fred: {[a:int, b :float] ^ z <:string>}
    '''
    tokens, lines = lex.lexBonesSrc(src, SymTable())
    snippet = determineGrouping(tokens)
    pp = snippet.PPGroup
    pp >> assertEquals >> '{[n o] o [n o] {:a} {:a}}. n [] t {:a}. l t {:x} t {:y} o l {:z}. {[n:t, n:t] o n t} {:fred}'


    # keys, assignment, type tagging, module scope, comments, continuation, blank lines, \n and ;
    src = r'''
        a: 2 // a comment

        a square \
            <:num> :b * 2 :c. c * 2
        d: c <:num>
    '''
    tokens, lines = lex.lexBonesSrc(src, SymTable())
    snippet = determineGrouping(tokens)
    pp = snippet.PPGroup
    pp >> assertEquals >> 'l {:a}. n n t {:b} o l {:c}. n o l. n t {:d}'


    # 3D list - 2D list of exprs with new line suggesting expr separation
    src = '''
        [
            a: 1
            b: 2 , c:3. d:4 ; 1
            ;
        ]
    '''
    tokens, lines = lex.lexBonesSrc(src, SymTable())
    snippet = determineGrouping(tokens)
    pp = snippet.PPGroup
    pp >> assertEquals >> '[l {:a}. l {:b}, l {:c}. l {:d}; l; ]'


    # add lists, for fun show a switch
    src = '''
        x switch[
            1, [
                a: 1
                b: 2
            ],
            2, ( ,
            )
        ]
    '''
    tokens, lines = lex.lexBonesSrc(src, SymTable())
    snippet = determineGrouping(tokens)
    pp = snippet.PPGroup
    pp >> assertEquals >> 'n n [l, [l {:a}. l {:b}], l, (, )]'


    # handle keyword names, descoping, function
    src = '''
        a: fred joe
            sally
                ifTrue: [.b]
                ifFalse: {.c}
        1 + 1
    '''
    tokens, lines = lex.lexBonesSrc(src, SymTable())
    snippet = determineGrouping(tokens)
    pp = snippet.PPGroup
    pp >> assertEquals >> 'n (n n n, [.n], {.n}) {:a}. l o l'


    # handle R_ANGLE
    src = '''
        1 > 2 <:fred>
        a == b
    '''
    tokens, lines = lex.lexBonesSrc(src, SymTable())
    snippet = determineGrouping(tokens)
    pp = snippet.PPGroup
    pp >> assertEquals >> 'l {R_ANGLE} l t. n o n'


    # TDD - functions and descoping <:DD2><:DD1>
    src = '''
        (1,2,3) do: {[x] (x square * .a) + (x * .b) + .c}    // <:unary> is the default for functions
    '''
    tokens, lines = lex.lexBonesSrc(src, SymTable())
    snippet = determineGrouping(tokens)
    pp = snippet.PPGroup
    pp >> assertEquals >> 'n ((l, l, l), {[n:t] (n n o .n) o (n o .n) o .n})'


    # TDD - functions and descoping <:DD2><:DD1>
    src = '''
        2 :a + 2 :b +2 :c    // i.e. a: 2; b: 4; c: 6
        b > 2 ifTrue: {
            b: 2   // we have a local b in the local scope here
            (.a * b, .a * .b)
        }
        (1,2,3) do: {[x] (x square * .a) + (x * .b) + .c}    // <:unary> is the default for functions
    '''
    tokens, lines = lex.lexBonesSrc(src, SymTable())
    snippet = determineGrouping(tokens)
    pp = snippet.PPGroup


    # PLAY FROM HERE
    src = '''
        x switch[
            1, [a: 1 * c; b: 2 * c],
            2, [
                a: 2 * c
                b: 1 * c
            ],
            3, {
                a = 1
                .a
            }
        ]
    '''
    tokens, lines = lex.lexBonesSrc(src, SymTable())
    snippet = determineGrouping(tokens)
    pp = snippet.PPGroup


    src = '''
        x switch[
            1, [
                a: 1
                b: 2
            ];
            2, {
                a: 2
                b: 1
            };
            "Default val"
        ]
        (1,2,3) fold[seed=0, {[prior, each] prior + each}]
        a ifTrue: {a: false} else: {a: true}
        a ifTrue: [a: false] else: [a: true]
        a ifTrueIfFalse [
            a:true
            ,
            a: false
        ]
        a doThis 
            thenThat[with a arg] 
            thenSomethingElse[...] 
            finishingWith(aHat)
    '''
    tokens, lines = lex.lexBonesSrc(src, SymTable())
    snippet = determineGrouping(tokens)
    pp = snippet.PPGroup


    src = r'''
        //from my_first_bones.lang uses *       // defines op+, op-, op*, op/, tNum, tStr, fRau, fUnary, fBinary, tAny in global scope
        //from std_bones.bones.stdio uses stdout, stderr
        requires 
            my_first_bones.conversions, 
            constants             // constants added to stretch the requires parsing

        stdout "Hello " "world!"
        a: 1
        2 :b + a my_first_bones.conversions.intToStr :c
        stdout c

        stderr (1.0 / constants.zero)          // what are we going to do about this?
    '''
    tokens, lines = lex.lexBonesSrc(src, SymTable())
    snippet = determineGrouping(tokens)
    pp = snippet.PPGroup
    pp >> assertEquals >> '{I}. n l l. l {:a}. l {:b} o n n {:c}. n n. n (l o n)'



def test_group_bones_files():
    for pfn in glob('./bones/*.bones', recursive=True):
        pfn >> PP
        with open(pfn) as f:
            src = f.read()
        tokens, lines = lex.lexBonesSrc(src, SymTable())
        snippet = determineGrouping(tokens)
        snippet.PPGroup >> PP



if __name__ == '__main__':
    main()
