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
# You should have received a copy of the GNU Affero General Public License along with coppertop-bones. If not, see
# <https://www.gnu.org/licenses/>.
#
# **********************************************************************************************************************

from dm.std import assertEquals

from bones.lang import lex
from bones.lang import group
from bones.lang.group import determineGrouping, SnippetGroup, DepthFirstTGVisitor
from bones.core.types import noun, unary
from dm.std import count
from bones.core.sym import SymTable



def _ppGroup(snippet):
    r = DepthFirstTGVisitor(snippet)

    pp = ""
    functions = []
    while not r.empty:
        if r.frontIsNewExpr:
            pp += "; "
        if r.frontIsNewBlock:
            pp += ", "
        if r.frontIsOpening:
            if not (r.frontIsNewExpr or r.frontIsNewBlock or r.frontIsFirstToken):
                pp += " "
            if isinstance(r.front, group.DefListGroup):
                pp += "["
            elif isinstance(r.front, group.ImListGroup):
                pp += "("
            elif isinstance(r.front, group.FunctionGroup):
                functions.append(r.front)
                pp += "{"
            elif isinstance(r.front, group.TypeLangGroup):
                pp += " <:"
            elif isinstance(r.front, SnippetGroup):
                pass
            else:
                raise NotImplementedError()
        elif r.frontIsClosing:
            if isinstance(r.front, group.DefListGroup):
                pp += "]"
            elif isinstance(r.front, group.ImListGroup):
                pp += ")"
            elif isinstance(r.front, group.FunctionGroup):
                pp += "}"
            elif isinstance(r.front, group.TypeTagGroup):
                pp += ">"
            elif isinstance(r.front, SnippetGroup):
                pass
            else:
                raise NotImplementedError()
        else:
            if not (r.frontIsNewExpr or r.frontIsNewBlock or r.frontIsFirstToken):
                pp += " "
            t = r.front
            pp += r.front.PPGroup
        if isinstance(r.front, group.FunctionTG) and r.frontIsOpening:
            r.popGroup()
        else:
            r.popFront()
    return pp, functions


def test_depthFirstTokenRange():

    src = '(0;1)'
    tokens, lines = lex.lexBonesSrc(src, SymTable())
    snippet = determineGrouping(tokens)
    pp = snippet.PPGroup
    pp >> assertEquals >> '(l; l)'

    pp, functions = _ppGroup(snippet)
    pp >> assertEquals >> '(l; l)'
    functions >> count >> assertEquals >> 0

    src = '''
        x switch[
            1, [
                <:num> _...a: 1;
                b: 2 <:offset>
            ],
            2, (
            ),
            3, {
                1 + 1
                _...d: {}
            },
            1 :c
        ]
    '''

    tokens, lines = lex.lexBonesSrc(src, SymTable())
    snippet = determineGrouping(tokens)
    pp, functions = _ppGroup(snippet)
    pp >> assertEquals >> 'n n [l, [l <n> {:_...a}; l <n> {:b}], l, (), l, {}, l {:c}]'
    functions >> count >> assertEquals >> 1
    pp.localScope.names.nameDetails >> assertEquals >> {'b': (noun, 1), 'c': (noun, 1)}
    pp.repoScope.names.nameDetails >> assertEquals >> {'a': (noun, 1), 'd': (unary, 1)}



def main():
    test_depthFirstTokenRange()


if __name__ == '__main__':
    main()
    print("pass")
