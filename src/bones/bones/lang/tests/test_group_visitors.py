# **********************************************************************************************************************
#
#                             Copyright (c) 2019-2021 David Briant. All rights reserved.
#
# **********************************************************************************************************************

from coppertop.std import assertEquals

from bones.lang import lex
from bones.lang import group
from bones.lang.group import determineGrouping, SnippetGroup, DepthFirstTGVisitor
from bones.lang.types import noun, unary
from coppertop.std import count
from bones.lang.sym import SymTable



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
    print("pass")


if __name__ == '__main__':
    main()
