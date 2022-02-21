# **********************************************************************************************************************
#
#                             Copyright (c) 2019-2021 David Briant. All rights reserved.
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


# key components
#
# determineGrouping
#   inputs a stream of tokens
#   outputs a SnippetTokens
# it consumes the tokens one by one injecting the token into the group at the top of a stack
# new groups are created as openers are encountered
# groups are _finalised (checked for errors) and popped off the stack as closers are encountered
#
# expr - a list of tokens that will be parsed later
# exprs   is expr. expr. ...
# exprs1D is exprs, exprs, ...
# exprs2D is exprs1D;exprs1D;... i.e. exprs,exprs,... ; exprs,exprs,... ; ...


import sys
if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)


import inspect
from coppertop.core import Missing, ProgrammerError
from coppertop.pipe import coppertop

from bones.lang.core import GroupingError

from bones.lang.lex import Token, L_ANGLE_COLON, L_PAREN, L_BRACKET, L_BRACE, R_ANGLE, R_PAREN, R_BRACKET, \
    R_BRACE, COMMA, L_PAREN_BRACKET, L_BRACE_BRACKET, prettyNameByTag, NAME_COLON, LINE_COMMENT, \
    C_COMMENT, SECTION, L_BRACE_PAREN, CONTINUATION, LINE_BREAK, SEMI_COLON, COLON, DOT, \
    NAME, ASSIGN_RIGHT, ASSIGN_LEFT, GLOBAL_ASSIGN_LEFT, GLOBAL_ASSIGN_RIGHT, CONTEXT_ASSIGN_RIGHT, \
    CONTEXT_ASSIGN_LEFT



NOT_ENDING = 0
SUGGESTED_BY_LINE_BREAK = 1
SECTION_END = 2
GROUP_END = 3

MIN_INDENT_FOR_KEYWORD = 2
MIN_INDENT_FOR_REQUIRES = 2

from bones.lang.types import nullary, binary, rau, ternary, unary, noun




def determineGrouping(tokens, extraCatchers=[]):
    stack = _Stack()
    currentTG = stack.push(SnippetTokens(None, None))   # this one obviously doesn't need catching!!
    openers = (L_PAREN, L_BRACKET, L_ANGLE_COLON, L_BRACE_BRACKET, L_BRACE_PAREN, L_BRACE, L_PAREN_BRACKET)
    openingCatchers = (catchLParen, catchLBracket, catchLAngleColon, catchLBraceBracket, catchLBraceParen, catchLBrace, catchLParenBracket)
    closers = (R_PAREN, R_BRACKET, R_ANGLE, R_BRACE)
    for token in tokens:
        isOpener = token.tag in openers
        isCloser = token.tag in closers
        caught = False
        isInteruptable = currentTG.isInteruptable
        if isInteruptable:
            for catcher in extraCatchers:
                caught = catcher(token, currentTG, stack)
                if caught:
                    currentTG = caught
                    break
        # first give the current token group a chance to process or reject the token <<<<< not quite true
        if not caught:
            normal = not(isOpener or isCloser) or (token.tag == R_ANGLE and not isinstance(currentTG, TypeDescTG))
            if normal:
                currentTG._consumeToken(token, token.indent)
                caught = True
        # then give the extraCatchers to override the core bones grouping
        if not isInteruptable:
            if not caught:
                for catcher in extraCatchers:
                    caught = catcher(token, currentTG, stack)
                    if caught:
                        currentTG = caught
                        break
        # finally allow the normal grouping
        if not caught:
            if isCloser:
                wanted = currentTG._processCloserOrAnswerError(token)             # will cause anything that doesn't care to self _finalise
                if isinstance(wanted, str):
                    # TODO identify location of both opener and closer and maybe also print the relevant lines of source?
                    got = prettyNameByTag[token.tag]
                    raise GroupingError('Wanted %s got %s - %s' % (wanted, got, token))
                caught = True
            if isOpener:
                for catcher in openingCatchers:
                    caught = catcher(token, currentTG, stack)
                    if caught:
                        currentTG = caught
                        break
        if not caught:
            raise GroupingError('Unhandled token %s' % str(token))

        # pop groups off the stack that have finished consuming tokens
        while not currentTG._consuming:
            stack.pop()
            currentTG = stack.current
    while currentTG._consuming:
        currentTG._finalise()
        if stack.len > 1:
            stack.pop()
            currentTG = stack.current
    return stack.current



class _Tokens(object):

    def _consumeToken(self, tokenOrGroup, indent):                       # works in tandem with determineGrouping
        assert self._consuming

        if self._phraseEndCause or self._endOfCommaSection or self._endOfSemicolonSection:
            self._finishPhrase(indent, self._phraseEndCause)
            self._phraseEndCause = NOT_ENDING

        if self._endOfCommaSection or self._endOfSemicolonSection:
            self._finishCommaSection()
            self._endOfCommaSection = False

        if self._endOfSemicolonSection:
            self._finishSemicolonSection()
            self._endOfSemicolonSection = False


        if not isinstance(tokenOrGroup, Token):
            self._phraseIndent = self._phraseIndent or indent
            self._phrase.append(tokenOrGroup)
            
        elif tokenOrGroup.tag in (LINE_COMMENT, C_COMMENT, SECTION):
            pass

        elif tokenOrGroup.tag is CONTINUATION:
            self._phraseIndent = Missing

        elif tokenOrGroup.tag is LINE_BREAK:
            self._phraseEndCause = SUGGESTED_BY_LINE_BREAK

        elif tokenOrGroup.tag is DOT:
            self._phraseEndCause = SECTION_END
            self._dotEncountered()

        elif tokenOrGroup.tag is COMMA:
            self._phraseEndCause = SECTION_END
            self._commaEncountered()

        elif tokenOrGroup.tag is SEMI_COLON:
            self._phraseEndCause = SECTION_END
            self._semicolonEncountered()

        elif tokenOrGroup.tag == NAME_COLON:
            if len(self._phrase) == 0:
                tokenOrGroup = toAssignLeft(tokenOrGroup)
                self._phrase.append(tokenOrGroup)
            else:
                raise ProgrammerError("Should be handled by the keyword catcher?")

        elif tokenOrGroup.tag == ASSIGN_RIGHT:
            # check we are NOT at start of expr
            if not self._phrase:
                msg = f'{tokenOrGroup.src} (AssignRight) is not allowed at start of expression'
                raise GroupingError(msg)
            self._phrase.append(tokenOrGroup)

        else:
            self._phraseIndent = self._phraseIndent or indent
            self._phrase.append(tokenOrGroup)

        return True


    # serves a three fold propose -
    #   1) the current sink of tokens,
    #   2) abstract base class of all groups,
    #   3) abstract base class for single expression groups

    def __init__(self, parent, opener):
        self._id = _getId()
        self._opener = opener
        self._closer = Missing
        self.parent = parent
        self._tokens = Missing

        # state machine variables - private to the grouping process
        self._phrase = _Phrase()
        self._phraseIndent = Missing
        self._phraseEndCause = NOT_ENDING
        self._endOfCommaSection = False
        self._endOfSemicolonSection = False
        
        # COMMAS and SEMI_COLON are definite separators where as DOT and LINE_BREAK are optional terminators
        self._hasComma = False
        self._hasSemicolon = False
        self._consuming = True
        self.isInteruptable = True

    def _startNewPhrase(self):
        self._phrase = _Phrase()
        self._phraseIndent = Missing

    def _startNewCommaSection(self):
        raise NotImplementedError(_classAndMethodFor(self))

    def _startNewSemicolonSection(self):
        raise NotImplementedError(_classAndMethodFor(self))

    def _finishPhrase(self, indent, cause):
        raise NotImplementedError(_classAndMethodFor(self))

    def _finishCommaSection(self):
        raise NotImplementedError(_classAndMethodFor(self))

    def _finishSemicolonSection(self):
        raise NotImplementedError(_classAndMethodFor(self))

    def _dotEncountered(self):
        self._finishPhrase(Missing, self._phraseEndCause)
        self._phraseEndCause = NOT_ENDING
    
    def _commaEncountered(self):
        self._hasComma = True
        self._endOfCommaSection = True
        self._finishPhrase(Missing, self._phraseEndCause)
        self._phraseEndCause = NOT_ENDING
        self._finishCommaSection()
        self._endOfCommaSection = False

    def _semicolonEncountered(self):
        self._hasSemicolon = True
        self._endOfCommaSection = True
        self._endOfSemicolonSection = True
        self._finishPhrase(Missing, self._phraseEndCause)
        self._phraseEndCause = NOT_ENDING
        self._finishCommaSection()
        self._endOfCommaSection = False
        self._finishSemicolonSection()
        self._endOfSemicolonSection = False

    def _processCloserOrAnswerError(self, token):
        raise NotImplementedError(_classAndMethodFor(self))

    def _moveTokensToExpr(self):
        assert self._consuming
        self._tokens = self._phrase
        self._phrase = Missing

    def _finalise(self):
        assert self._consuming
        if self._phrase:
            raise ProgrammerError("Still have tokens in flight")
        self._consuming = False

    def _hasTokens(self):
        return len(self._phrase) > 0

    @property
    def _firstToken(self):
        return self._opener
        # return self._phrase[0] if self._consuming else self._tokens[0]

    @property
    def _lastToken(self):
        return self._phrase[-1] if self._consuming else self._tokens[-1]

    @property
    def expr(self):
        assert not self._consuming
        return self._tokens

    @property
    def indent(self):
        return self._firstToken.indent

    @property
    def c1(self):
        return self._firstToken.c1

    @property
    def c2(self):
        return self._lastToken.c2

    @property
    def l1(self):
        return self._firstToken.l1

    @property
    def l2(self):
        return self._lastToken.l2

    @property
    def PPGroup(self):
        raise NotImplementedError(_classAndMethodFor(self))



class _CommaSeparated(_Tokens):
    #  N**phrase separated by COMMA - e.g. parameters, keyword style call, table, table keys

    def __init__(self, parent, opener):
        super().__init__(parent, opener)
        self._commaList = _CommaList()

    def _startNewCommaSection(self):
        pass

    def _finishPhrase(self, indent, cause):
        tokens = self._phrase
        if tokens:
            if cause == SUGGESTED_BY_LINE_BREAK:
                if indent > self._phraseIndent:
                    pass
                else:
                    tokens = _procesAssigmentsInPhrase(tokens)
                    self._commaList.append(tokens)
                    self._startNewPhrase()
            elif cause == SECTION_END:
                tokens = _procesAssigmentsInPhrase(tokens)
                self._commaList.append(tokens)
                self._startNewPhrase()
            else:
                raise ProgrammerError()
        else:
            if cause == SECTION_END:
                self._commaList.append(Missing)
                self._startNewPhrase()
            else:
                raise ProgrammerError()

    def _finishCommaSection(self):
        # nothing to do as already finishe in the _finishPhrase method
        pass

    def _dotEncountered(self):
        raise SyntaxError("dot enountered - needs better description")

    def _semicolonEncountered(self):
        raise SyntaxError("semi colon enountered - needs better description")

    # @property
    # def _firstToken(self):
    #     return self._commaList[0][0]

    @property
    def _lastToken(self):
        return self._commaList[-1][-1]

    @property
    def exprList(self):
        assert not self._consuming
        return self._commaList

    @property
    def PPGroup(self):
        pps = [('' if tokenOrGroup is Missing else tokenOrGroup.PPTokens) for tokenOrGroup in self._commaList]
        return ', '.join(pps)

    def __repr__(self):
        return '%s<%r>( %r )' % (self.__class__.__name__, self._id, self._commaList)



class _DotSeparated(_Tokens):
    # N**phrase separated by DOT / LINE_BREAK - e.g. snippet, function

    def __init__(self, parent, opener):
        super().__init__(parent, opener)
        self._dotList = _DotList()

    def _finishPhrase(self, indent, cause):
        tokens = self._phrase
        if tokens:
            if cause == SUGGESTED_BY_LINE_BREAK:
                if indent > self._phraseIndent:
                    # if new indent is greater than the prior indent it means we are continuing the phrawe
                    # TODO mark the indent at the start of the phrase not the last indent
                    pass
                else:
                    tokens = _procesAssigmentsInPhrase(tokens)
                    self._dotList << tokens
                    self._startNewPhrase()
            elif cause == SECTION_END:
                tokens = _procesAssigmentsInPhrase(tokens)
                self._dotList << tokens
                self._startNewPhrase()
            else:
                raise ProgrammerError()
        else:
            if cause == SUGGESTED_BY_LINE_BREAK:
                pass
            elif cause == SECTION_END:
                self._startNewPhrase()
            else:
                raise ProgrammerError()

    @property
    def _firstToken(self):
        return self._dotList[0][0]

    @property
    def _lastToken(self):
        return self._dotList[-1][-1]

    @property
    def exprs(self):
        assert not self._consuming
        return self._dotList

    @property
    def PPGroup(self):
        pps = [tokenOrGroup.PPGroup for tokenOrGroup in self._dotList]
        return '. '.join(pps)

    def __repr__(self):
        return '%s<%r>( %r )' % (self.__class__.__name__, self._id,  self._dotList)



class _Row(_DotSeparated):
    # list of exprs separated by COMMA - only as a row of IMList and DefList

    def __init__(self, parent, opener):
        super().__init__(parent, opener)
        self._row = _Row()

    def _startNewCommaSection(self):
        self._dotList = _DotList()

    def _finishCommaSection(self):
        if self._dotList:
            self._row << self._dotList
            self._startNewCommaSection()
        elif self._hasComma:
            self._row << Missing
            self._startNewCommaSection()

    @property
    def _firstToken(self):
        return self._row[0][0][0]

    @property
    def _lastToken(self):
        return self._row[-1][-1][-1]

    @property
    def exprs1D(self):
        assert not self._consuming
        return self._row

    @property
    def PPGroup(self):
        prettyExprs = [exprs.PPGroup for exprs in self._row]
        return ', '.join(prettyExprs)

    def __repr__(self):
        return '%s<%r>( %r )' % (self.__class__.__name__, self._id,  self._row)



class _Grid(_Row):
    # list of exprs1D separated by SEMI_COLON - e.g. ImList, DefList

    def __init__(self, parent, opener):
        super().__init__(parent, opener)
        self._grid = _Grid()

    def _startNewSemicolonSection(self):
        self._row = _Row()

    def _finishSemicolonSection(self):
        if self._row:
            self._grid << self._row
            self._startNewSemicolonSection()
        elif self._hasSemicolon:
            self._grid << Missing
            self._startNewSemicolonSection()

    @property
    def _firstToken(self):
        return self._grid[0][0][0][0]

    @property
    def _lastToken(self):
        return self._grid[-1][-1][-1][-1]

    @property
    def grid(self):
        assert not self._consuming
        return self._grid

    @property
    def PPGroup(self):
        prettyExprs = [exprs1D.PPGroup for exprs1D in self._grid]
        return '; '.join(prettyExprs)

    def __repr__(self):
        return '%s<%r>( %r )' % (self.__class__.__name__, self._id,  self._grid)



def _procesAssigmentsInPhrase(phrase):
    # check for assignments, converting ASSIGN_LEFT into ASSIGN_RIGHT

    # convert left assignments into terminal right assignments
    if isinstance(phrase[0], Token):
        if phrase[0].tag == ASSIGN_LEFT:
            assert len(phrase) >= 2, "Syntax error"       # must do - nice error message
            # move first token to end
            phrase = phrase[1:] + [toAssignRight(phrase[0])]
        elif phrase[0].tag == CONTEXT_ASSIGN_LEFT:
            assert len(phrase) >= 2, "Syntax error"       # must do - nice error message
            # move first token to end
            phrase = phrase[1:] + [toContextAssignRight(phrase[0])]
        elif phrase[0].tag == GLOBAL_ASSIGN_LEFT:
            assert len(phrase) >= 2, "Syntax error"       # must do - nice error message
            # move first token to end
            phrase = phrase[1:] + [toGlobalAssignRight(phrase[0])]

    elif len(phrase) >= 2:
        if isinstance(phrase[0], TypeDescTG) and isinstance(phrase[1], Token):
            if phrase[1].tag == ASSIGN_LEFT:
                assert len(phrase) >= 3, "Syntax error"       # must do - nice error message
                # move first two tokens to end
                phrase = phrase[2:] + phrase[0:1] + [toAssignRight(phrase[1])]
            elif phrase[1].tag == CONTEXT_ASSIGN_LEFT:
                assert len(phrase) >= 3, "Syntax error"       # must do - nice error message
                # move first two tokens to end
                phrase = phrase[2:] + phrase[0:1] + [toContextAssignRight(phrase[1])]
            elif phrase[1].tag == GLOBAL_ASSIGN_LEFT:
                assert len(phrase) >= 3, "Syntax error"       # must do - nice error message
                # move first two tokens to end
                phrase = phrase[2:] + phrase[0:1] + [toGlobalAssignRight(phrase[1])]

    # catch all right assignments
    for prior, each in pairwise(phrase):
        if isinstance(each, Token):
            if each.tag == ASSIGN_RIGHT:
                varName = each.src
            elif each.tag == CONTEXT_ASSIGN_RIGHT:
                varName = each.src[5:]
            elif each.tag == GLOBAL_ASSIGN_RIGHT:
                varName = each.src[5:]
    return _Phrase(phrase)



# **********************************************************************************************************************
# snippet
# **********************************************************************************************************************

class SnippetTokens(_DotSeparated):
    def _finalise(self):
        assert self._consuming
        # since a Snippet has no closing token we have to close when the main parsing loop calls _finalise
        self._finishPhrase(Missing, SECTION_END)
        super()._finalise()
    def _commaEncountered(self):
        raise GroupingError("COMMA not valid in snippet")
    def _semicolonEncountered(self):
        raise GroupingError("SEMI_COLON not valid in snippet")


# **********************************************************************************************************************
# [...
# **********************************************************************************************************************

def catchLBracket(token, currentTG, stack):
    if not (token.tag == L_BRACKET): return None
    dl = DefListTokens(currentTG, token)
    currentTG._consumeToken(dl, token.indent)
    return stack.push(dl)

class DefListTokens(_Grid):
    def _processCloserOrAnswerError(self, token):
        if token.tag != R_BRACKET: return prettyNameByTag(R_BRACKET)
        self._finishPhrase(Missing, SECTION_END)
        self._finishCommaSection()
        self._finishSemicolonSection()
        self._finalise()
    @property
    def PPGroup(self):
        ppRows = [('' if tokenGroupOrRow is Missing else tokenGroupOrRow.PPGroup) for tokenGroupOrRow in self._grid]
        return f"[{'; '.join(ppRows)}]"


# **********************************************************************************************************************
# (...
# **********************************************************************************************************************

def catchLParen(token, currentTG, stack):
    if not (token.tag == L_PAREN): return None
    il = ImListTokens(currentTG, token)
    currentTG._consumeToken(il, token.indent)
    return stack.push(il)

class ImListTokens(_Grid):
    def _processCloserOrAnswerError(self, token):
        if token.tag != R_PAREN: return prettyNameByTag(R_PAREN)
        self._finishPhrase(Missing, SECTION_END)
        self._finishCommaSection()
        self._finishSemicolonSection()
        self._finalise()
    @property
    def PPGroup(self):
        ppRows = [('' if tokenGroupOrRow is Missing else tokenGroupOrRow.PPGroup) for tokenGroupOrRow in self._grid]
        return '(' + ('; '.join(ppRows)) + ')'



# **********************************************************************************************************************
# {... {[... and {(...
# **********************************************************************************************************************

def catchLBrace(token, currentTG, stack):
    if not (token.tag == L_BRACE): return None
    f = FunctionTokens(currentTG, token)
    currentTG._consumeToken(f, token.indent)
    return stack.push(f)

def catchLBraceBracket(token, currentTG, stack):
    if not (token.tag == L_BRACE_BRACKET): return None
    f = FunctionTokens(currentTG, token)
    currentTG._consumeToken(f, token.indent)
    stack.push(f)
    dp = DefParamsTokens(f, token)
    f._params = dp
    return stack.push(dp)

def catchLBraceParen(token, currentTG, stack):
    if not (token.tag == L_BRACE_PAREN): return None
    f = FunctionTokens(currentTG, token)
    currentTG._consumeToken(f, token.indent)
    stack.push(f)
    ip = ImParamsTokens(f, token)
    f._params = ip
    return stack.push(ip)


class FunctionTokens(_DotSeparated):
    def __init__(self, parent, opener):
        super().__init__(parent, opener)
        self._params = Missing
        self._retType = Missing
    def _processCloserOrAnswerError(self, token):
        if token.tag != R_BRACE: return prettyNameByTag(R_BRACE)
        self._finishPhrase(Missing, SECTION_END)
        self._finalise()
    def _finalise(self):
        assert self._consuming
        super()._finalise()
    @property
    def PPGroup(self):
        if self._params:
            ppParams = self._params.PPGroup + ' '
        else:
            ppParams = ''
        return '{' + ppParams + self._dotList.PPGroup + '}'
    @property
    def _firstToken(self):
        return self._params[0][0] if self._params else self._dotList[0][0]
    @property
    def _lastToken(self):
        return self._dotList[-1][-1]



class _ParamsTokens(_CommaSeparated):
    
    def __init__(self, parent, opener):
        super().__init__(parent, opener)
        assert parent._params is Missing
        parent._params = self
        self._actualParams = Missing
        
    def _finishPhrase(self, indent, cause):
        # five cases "fred: num", "fred:num", "fred :num",  "fred : num", "fred" - we could add some context to the
        # lexer to simplify our job here but for the moment let's not make it more complex
        phrase = self._phrase
        for token in phrase:
            if not isinstance(token, Token):
                raise GroupingError(f'Parameter must be a name - got {token} - handle in _consumeToken')
        if len(phrase) == 0:
            raise GroupingError(f'{{[] has no arguments @{self.l1}:{self.c1}')
        elif len(phrase) == 1:
            firstToken = phrase[0]
            if firstToken.tag == ASSIGN_LEFT:
                raise GroupingError(f'{{[... {firstToken.src} is missing type @{self.l1}:{self.c1}')
            elif firstToken.tag != NAME:
                raise GroupingError(f'{{[... contains {firstToken.src} which is not a name @{self.l1}:{self.c1}')
            phrase2 = [SingleParamTokens(self, firstToken, [])]
        else:
            firstToken = phrase[0]
            if firstToken.tag == ASSIGN_LEFT:
                # fred:num or fred: num
                newNameToken = Token(firstToken.src, NAME, firstToken.indent, firstToken.n, firstToken.c1, firstToken.c2, firstToken.l1, firstToken.l2)
                phrase2 = [SingleParamTokens(self, newNameToken, phrase[1:])]
            elif firstToken.tag == NAME and (secondToken := phrase[1]).tag == ASSIGN_RIGHT:
                # fred :num
                firstTypeName = Token(secondToken.src, NAME, secondToken.indent, secondToken.n, secondToken.c1, secondToken.c2, secondToken.l1, secondToken.l2)
                phrase2 = [SingleParamTokens(self, firstToken, [firstTypeName] + phrase[2:])]
            elif len(phrase) >= 3 and firstToken.tag == NAME and phrase[1].tag == COLON and phrase[2].tag == NAME:
                # fred : name
                phrase2 = [SingleParamTokens(self, firstToken, phrase[2:])]
            else:
                raise SyntaxError()
        self._commaList << _Phrase(phrase2)
        self._startNewPhrase()

    def _processCloserOrAnswerError(self, token):
        self._finishPhrase(Missing, SECTION_END)
        self._finalise()
        
    def _finalise(self):
        assert self._consuming
        if len(self._commaList) == 0:
            raise GroupingError("No parameters in list")
        for phrase in self._commaList:
            # [a :int, b] is max allowed (i.e. 2 tokens - a name and a type)
            if phrase is not Missing and (len(phrase) < 1 or len(phrase) > 3):
                raise GroupingError("Parameters can only be one assigment expression each or a name")
        super()._finalise()
        
    # @property
    # def _firstToken(self):
    #     return self._commaList[0][0]
    
    @property
    def _lastToken(self):
        return self._commaList[-1][-1]


class DefParamsTokens(_ParamsTokens):
    def _processCloserOrAnswerError(self, token):
        if token.tag != R_BRACKET: return prettyNameByTag(R_BRACKET)
        super()._processCloserOrAnswerError(token)
    @property
    def PPGroup(self):
        pps = [('' if tokenOrGroup is Missing else tokenOrGroup.PPGroup) for tokenOrGroup in self._commaList]
        return f'[{", ".join(pps)}]'


class ImParamsTokens(_ParamsTokens):
    def _processCloserOrAnswerError(self, token):
        if token.tag != R_PAREN: return prettyNameByTag(R_PAREN)
        super()._processCloserOrAnswerError(token)
    @property
    def PPGroup(self):
        pps = [('' if tokenOrGroup is Missing else tokenOrGroup.PPGroup) for tokenOrGroup in self._commaList]
        return f'({", ".join(pps)})'


class SingleParamTokens(_Tokens):
    def __init__(self, parent, nameToken, typeExpr):
        super().__init__(parent, nameToken)
        self._closer = typeExpr[-1] if typeExpr else nameToken  # handle no typeExpr
        self.nameToken = nameToken
        self.typeExpr = typeExpr
    @property
    def PPGroup(self):
        return self.nameToken.PPGroup + ":t"
    def __repr__(self):
        return self.nameToken.src + (":TBI" if not self.typeExpr else ':...')



# **********************************************************************************************************************
# ([...
# **********************************************************************************************************************

def catchLParenBracket(token, currentTG, stack):
    if not (token.tag == L_PAREN_BRACKET): return None
    ttg = TableTokens(currentTG, token)
    currentTG._consumeToken(ttg, token.indent)
    stack.push(ttg)
    tktg = TableKeys(ttg, token)
    return stack.push(tktg)

class TableTokens(_CommaSeparated):
    def _processCloserOrAnswerError(self, token):
        if token.tag != R_PAREN: return prettyNameByTag(R_PAREN)
        self._finalise()

class TableKeys(_CommaSeparated):
    def _processCloserOrAnswerError(self, token):
        if token.tag != R_BRACKET: return prettyNameByTag(R_BRACKET)
        self._finalise()



# **********************************************************************************************************************
# <:...
# **********************************************************************************************************************

def catchLAngleColon(token, currentTG, stack):
    if not (token.tag == L_ANGLE_COLON): return None
    tttg = TypeDescTG(currentTG, token)
    currentTG._consumeToken(tttg, token.indent)
    return stack.push(tttg)

class TypeDescTG(_Tokens):
    def _processCloserOrAnswerError(self, token):
        if token.tag != R_ANGLE: return prettyNameByTag(R_ANGLE)
        self._moveTokensToExpr()
        self._finalise()
    @property
    def PPGroup(self):
        return 't'



# **********************************************************************************************************************
# keyword style calls
# **********************************************************************************************************************

def catchKeyword(token, currentTG, stack):
    if token.tag != NAME_COLON:
        return None
    if len(currentTG._phrase) == 0 or isinstance(currentTG, SingleParamTokens):
        # either there's nothing to the left so it can't be a keyword call, or we're parsing parameters for a function
        return None
    # if the potential keyword is on the same line then ok, or if it adds at least MIN_INDENT_FOR_KEYWORD to
    # the indent of the first token in the expression
    indentOverFirstToken = token.indent - currentTG._phrase[0].indent
    if (currentTG._phrase[0].l2 != token.l2) and not (indentOverFirstToken >= MIN_INDENT_FOR_KEYWORD):
        return None
    ketg = KeywordCatcher(currentTG, token)
    return stack.push(ketg)


# a: fred joe ifTrue: sally ugh ifFalse: []  => if encounter DOT, COMMA, SEMI_COLON then self._phraseEndCause = SECTION_END
# answers ifTrue:ifFalse (fred joe, sally ugh, []) :a

def lastKv(d):
    k, v = d.popitem()
    d[k] = v
    return k, v

def atIfNonePut(d, k, v):
    return d.setdefault(k, v)

class KeywordCatcher(_CommaSeparated):

    def _consumeToken(self, tokenOrGroup, indent):
        assert self._consuming
        if self._phraseEndCause == SUGGESTED_BY_LINE_BREAK:
            if indent > self._phraseIndent:
                self._phraseEndCause = NOT_ENDING
            else:
                tokens = self._phrase
                if tokens:
                    tokens = _procesAssigmentsInPhrase(tokens)
                    self._commaList << tokens
                    self._latestToken = tokens[-1]
                    self._phrase = []
                else:
                    self._commaList << Missing
                    self._phrase = []
                return self._completeKeyWordAndPassToParent(tokenOrGroup, indent)
        elif self._phraseEndCause == SECTION_END:
            tokens = self._phrase
            if tokens:
                tokens = _procesAssigmentsInPhrase(tokens)
                self._commaList << tokens
                self._phrase = []
            else:
                self._commaList << Missing
                self._phrase = []
            self._phraseEndCause = NOT_ENDING
        if isinstance(tokenOrGroup, Token):
            if tokenOrGroup.tag in (LINE_COMMENT, C_COMMENT, SECTION):
                pass
            elif tokenOrGroup.tag is CONTINUATION:
                self._phraseIndent = Missing
            elif tokenOrGroup.tag is LINE_BREAK:
                self._phraseEndCause = SUGGESTED_BY_LINE_BREAK
            elif tokenOrGroup.tag in (DOT, COMMA, SEMI_COLON):
                return self._completeKeyWordAndPassToParent(tokenOrGroup, indent)
            elif tokenOrGroup.tag == NAME_COLON:
                if self._phrase:
                    self._keywordTokens.append(tokenOrGroup)
                    self._commaList << self._phrase
                    self._startNewPhrase()
                else:
                    self._keywordTokens.append(tokenOrGroup)
                    self._commaList << Missing          # creating a partial
                    self._startNewPhrase()
                self._latestToken = tokenOrGroup
            elif tokenOrGroup.tag == ASSIGN_RIGHT:
                if not self._phrase:
                    raise GroupingError('AssignRight not only allowed at start of expression - %s')
                self._phrase.append(tokenOrGroup)
            else:
                if self._phraseIndent is Missing: self._phraseIndent = indent
                self._phrase.append(tokenOrGroup)
        else:
            if self._phraseIndent is Missing: self._phraseIndent = indent
            self._phrase.append(tokenOrGroup)

        return True

    def __init__(self, parent, opener):
        super().__init__(parent, opener)
        self.isInteruptable = False
        parentTokens = parent._phrase
        parent._phrase = Missing                # doing this will cause an error if we don't do this right :)
        self._phraseIndent = parentTokens[0].indent
        self._keywordTokens = [opener]
        self._tokensForParent = []
        if isinstance(parentTokens[0], Token) and parentTokens[0].tag == ASSIGN_LEFT:
            self._tokensForParent = [parentTokens[0]]
            firstArgTokens = parentTokens[1:]
        else:
            firstArgTokens = parentTokens

        assert firstArgTokens                     # instead could allow partial of first arg?
        self._commaList << _Phrase(firstArgTokens)          # << store args in this
        self._parentTokens = parentTokens
        self._latestToken = parentTokens[-1]

    def _processCloserOrAnswerError(self, token):
        tokens = self._phrase
        if tokens:
            tokens = _procesAssigmentsInPhrase(tokens)
            self._commaList << tokens
        else:
            self._commaList << Missing
        self._replaceSelfInParent()
        super()._finalise()
        desiredTokenStringOrNone = self.parent._processCloserOrAnswerError(token)
        if desiredTokenStringOrNone: return desiredTokenStringOrNone

    def _finalise(self):
        assert self._consuming
        tokens = self._phrase
        if tokens:
            tokens = _procesAssigmentsInPhrase(tokens)
            self._commaList << tokens
            self._phrase = []
        else:
            self._commaList << Missing
        self._replaceSelfInParent()
        super()._finalise()

    def _replaceSelfInParent(self):
        newNameToken = Token(
            "".join([t.src + ":" for t in self._keywordTokens]),
            NAME,
            self._firstToken.indent,
            Missing,
            self._firstToken.c1,
            self._lastToken.c2,
            self._firstToken.l1,
            self._lastToken.l2
        )
        self._tokensForParent.append(newNameToken)

        argsImList = ImListTokens(self.parent, self._opener)

        exprs1D = _Row()
        for expr in self._commaList:
            for tokenOrGroup in expr:
                if isinstance(tokenOrGroup, _Tokens):
                    tokenOrGroup.parent = argsImList
            _dotList = _DotList()
            _dotList << expr
            exprs1D << _dotList
        grid = _Grid()
        grid << exprs1D
        argsImList._grid = _Grid(grid)
        argsImList._finalise()

        self._tokensForParent.append(argsImList)
        self.parent._phrase = self._tokensForParent
        self.parent._finishPhrase(Missing, SECTION_END)

    def _completeKeyWordAndPassToParent(self, tokenOrGroup, indent):
        self._replaceSelfInParent()
        super()._finalise()
        return self.parent._consumeToken(tokenOrGroup, indent)

    @property
    def _firstToken(self):
        return self._parentTokens[0]
    @property
    def _lastToken(self):
        return self._latestToken



# **********************************************************************************************************************
# requires ...
# **********************************************************************************************************************

def catchRequires(token, currentTG, stack):
    if not (token.tag == NAME and token.src == 'requires'):
        return None
    ietg = RequiresCatcher(currentTG, token)
    currentTG._consumeToken(ietg, token.indent)
    return stack.push(ietg)

class RequiresCatcher(_CommaSeparated):
    # include sdf.sdf.sdf, sdf.sdf   -> list of modules to include
    # alternative [asdf.asdf.asd, sdf.sdf.sf] include - but the asd.asd.asd are special and need to be interpreted
    # differently to other names

    def __init__(self, parent, opener):
        super().__init__(parent, opener)
        self.isInteruptable = False
        self._requiresIndent = Missing
        self._awaitingTokensPostComma = False

    def _processCloserOrAnswerError(self, token):
        self._finalise()
        return self.parent._processCloserOrAnswerError(token)

    def _finalise(self):
        if self._phrase: self._finishPhrase(Missing, SECTION_END)
        if len(self._commaList) == 0:
            raise GroupingError(f'requires - no items specified - needs better error msg')
        if self._awaitingTokensPostComma:
            raise GroupingError(f'requires - missing items after last comma - needs better error msg')
        super()._finalise()

    @property
    def PPGroup(self):
        return '{I}'

    def _consumeToken(self, tokenOrGroup, indent):
        assert self._consuming

        if self._phraseEndCause or self._endOfCommaSection:
            self._finishPhrase(indent, self._phraseEndCause)
            if self._phraseEndCause == GROUP_END:
                return self._completeKeyWordAndPassToParent(tokenOrGroup, indent)
            self._phraseEndCause = NOT_ENDING

        if not isinstance(tokenOrGroup, Token):
            raise GroupingError("No groups allowed in requires - better error msg needed")
        
        elif tokenOrGroup.tag in (LINE_COMMENT, C_COMMENT, SECTION):
            pass

        elif tokenOrGroup.tag is CONTINUATION:
            pass

        elif tokenOrGroup.tag is LINE_BREAK:
            self._phraseEndCause = SUGGESTED_BY_LINE_BREAK

        elif tokenOrGroup.tag is DOT:
            self._phraseEndCause = GROUP_END

        elif tokenOrGroup.tag is COMMA:
            if self._phrase:
                self._commaList << self._phrase
                self._startNewPhrase()
                self._awaitingTokensPostComma = True
            else:
                raise GroupingError(f"Encountered COMMA without a NAME - better error msg needed")

        elif tokenOrGroup.tag in (SEMI_COLON, NAME_COLON, ASSIGN_RIGHT):
            raise GroupingError(f"{prettyNameByTag(tokenOrGroup.tag)} not allowed in requires - better error msg needed")

        else:
            self._phrase.append(tokenOrGroup)
            self._awaitingTokensPostComma = False

        self._requiresIndent = self._requiresIndent or indent
        return True

    def _finishPhrase(self, indent, cause):
        phrase = self._phrase
        if phrase:
            if cause == SUGGESTED_BY_LINE_BREAK:
                if indent > self._requiresIndent:
                    pass
                else:
                    phrase = _procesAssigmentsInPhrase(phrase)
                    self._commaList.append(phrase)
                    self._startNewPhrase()
                    self._phraseEndCause = GROUP_END
            elif cause == SECTION_END:
                phrase = _procesAssigmentsInPhrase(phrase)
                self._commaList.append(phrase)
                self._startNewPhrase()
            else:
                raise ProgrammerError()
        else:
            if cause == SUGGESTED_BY_LINE_BREAK:
                if indent >= self._requiresIndent + MIN_INDENT_FOR_REQUIRES:
                    # e.g. new line after requires, new line after COMMA
                    pass
                else:
                    # end the requires phrase
                    self._finalise()
            elif cause == SECTION_END:
                self._finalise()
            else:
                raise ProgrammerError()

    def _completeKeyWordAndPassToParent(self, tokenOrGroup, indent):
        self.parent._finishPhrase(Missing, SECTION_END)
        super()._finalise()
        return self.parent._consumeToken(tokenOrGroup, indent)



# **********************************************************************************************************************
# from ... uses ...
# **********************************************************************************************************************

def catchFromUses(token, currentTG, stack):
    if not (token.tag == NAME and token.src == 'from'): return None
    fietg = FromImportCatcher(currentTG, token)
    currentTG._consumeToken(fietg, token.indent)
    return stack.push(fietg)

class FromImportCatcher(_Tokens):
    def __init__(self, parent, opener):
        super().__init__(parent, opener)
        self.isInteruptable = False
    def _processCloserOrAnswerError(self, token):
        self._finalise()
        self.parent._processCloserOrAnswerError(token)
    def _finalise(self):
        self._phraseEndCause = SECTION_END
        super()._finalise()
    @property
    def PPGroup(self):
        return '{FI}'
    def _consumeToken(self, tokenOrGroup, indent):
        assert self._consuming
        if isinstance(tokenOrGroup, Token) and tokenOrGroup.tag in (LINE_BREAK, SEMI_COLON):
            self._finalise()
        return True



# **********************************************************************************************************************
# Utilities
# **********************************************************************************************************************

@coppertop
def PPGroup(x):
    return x.PPGroup


_idSeed = 0
def _getId():
    global _idSeed
    _idSeed += 1
    return _idSeed


class _Phrase(list):
    # aka sentance, expression / expr
    # N**Token - space separated
    def __lshift__(self, other):   # self << other
        if not isinstance(other, (Token, _Tokens)):
            raise TypeError()
        self.append(other)
        return self
    @property
    def first(self):
        return self[0]
    @property
    def last(self):
        return self[-1]
    @property
    def PPGroup(self):
        pps = [tokenOrGroup.PPGroup for tokenOrGroup in self]
        return ' '.join(pps)
    def append(self, other):
        if not isinstance(other, (Token, _Tokens)):
            raise TypeError()
        return super().append(other)


class _CommaList(list):
    # comma separated list of names or phrases
    def __lshift__(self, other):   # self << other
        if not isinstance(other, _Phrase) and other is not Missing:
            raise TypeError()
        self.append(other)
        return self
    @property
    def first(self):
        return self[0]
    @property
    def last(self):
        return self[-1]
    @property
    def PPGroup(self):
        pps = [('' if phrase is Missing else phrase.PPGroup) for phrase in self]
        return ', '.join(pps)
    def append(self, other):
        if not isinstance(other, _Phrase) and other is not Missing:
            raise TypeError()
        return super().append(other)


class _DotList(list):
    # aka paragraph
    # dot separated list of phrases
    def __lshift__(self, other):   # self << other
        if not isinstance(other, _Phrase):
            raise TypeError()
        self.append(other)
        return self
    @property
    def first(self):
        return self[0]
    @property
    def last(self):
        return self[-1]
    @property
    def PPGroup(self):
        pps = [phrase.PPGroup for phrase in self]
        return '. '.join(pps)
    def append(self, other):
        if not isinstance(other, _Phrase):
            raise TypeError()
        return super().append(other)


class _Row(list):
    # comma separated list of paragraph (_DotList)
    def __lshift__(self, other):   # self << other
        if not isinstance(other, _DotList) and other is not Missing:
            raise TypeError()
        self.append(other)
        return self
    @property
    def first(self):
        return self[0]
    @property
    def last(self):
        return self[-1]
    @property
    def PPGroup(self):
        pps = [('' if tokenGroupOrDots is Missing else tokenGroupOrDots.PPGroup) for tokenGroupOrDots in self]
        return ', '.join(pps)
    def append(self, other):
        if not isinstance(other, _DotList) and other is not Missing:
            raise TypeError()
        return super().append(other)


class _Grid(list):
    # aka matrix (of paragraphs)
    # list of _Row
    def __lshift__(self, other):  # self << other
        if not isinstance(other, _Row) and other is not Missing:
            raise TypeError()
        self.append(other)
        return self
    @property
    def first(self):
        return self[0]
    @property
    def last(self):
        return self[-1]
    @property
    def PPGroup(self):
        pps = [('' if tokenGroupOrRow is Missing else tokenGroupOrRow.PPGroup) for tokenGroupOrRow in self]
        return '; '.join(pps)
    def append(self, other):
        if not isinstance(other, _Row) and other is not Missing:
            raise TypeError()
        return super().append(other)


def toAssignLeft(alokf):
    assert alokf.tag == NAME_COLON
    return Token(
        alokf.src, ASSIGN_LEFT, alokf.indent,
        alokf.n, alokf.c1, alokf.c2, alokf.l1, alokf.l2
    )

def toAssignRight(al):
    assert al.tag == ASSIGN_LEFT
    return Token(
        al.src, ASSIGN_RIGHT, al.indent,
        al.n, al.c1, al.c2, al.l1, al.l2
    )

def toContextAssignRight(cal):
    assert cal.tag == CONTEXT_ASSIGN_LEFT
    return Token(
        cal.src, CONTEXT_ASSIGN_RIGHT, cal.indent,
        cal.n, cal.c1, cal.c2, cal.l1, cal.l2
    )

def toGlobalAssignRight(gal):
    assert gal.tag == GLOBAL_ASSIGN_LEFT
    return Token(
        ':'+gal.src[:-1], GLOBAL_ASSIGN_RIGHT, gal.indent,
        gal.n, gal.c1, gal.c2, gal.l1, gal.l2
    )


class _Stack(object):
    def __init__(self):
        self._list = []
    def push(self, x):
        self._list.append(x)
        return x
    def pop(self):
        self._list = self._list[0:-1]
    @property
    def current(self):
        return self._list[-1]
    @property
    def len(self):
        return len(self._list)


# from more_itertools import pairwise

from itertools import tee
def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def _classAndMethodFor(obj):
    frame = inspect.currentframe()
    if frame.f_code.co_name == '_classAndMethodFor':
        frame = frame.f_back
    return f'{obj.__class__.__name__}.{frame.f_code.co_name}'
