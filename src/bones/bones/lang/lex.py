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

import sys
if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)


import re, collections, itertools
from coppertop.pipe import *
from coppertop.core import *


_tagIdSeed = itertools.count(start=0)

WHITE_BREAK = next(_tagIdSeed)
LEADING_SPACES = next(_tagIdSeed)

# NON-CODE
LINE_COMMENT = next(_tagIdSeed)
C_COMMENT = next(_tagIdSeed)
SECTION = next(_tagIdSeed)
CONTINUATION = next(_tagIdSeed)

# SEPARATORS
COLON = next(_tagIdSeed)
COMMA = next(_tagIdSeed)
SEMI_COLON = next(_tagIdSeed)
DOT = next(_tagIdSeed)
LINE_BREAK = next(_tagIdSeed)

# IDENTIFIERS
NAME = next(_tagIdSeed)             # fred.joe.sally - lookup attribute (`sally on (`joe on name fred))
OPERATOR = next(_tagIdSeed)
GLOBAL_NAME = next(_tagIdSeed)      # _..joe - joe is global scope lookup - e.g. _..sys.version, _..sys.stdout << "hello", stderr, cmd_line_args, env
CONTEXT_NAME = next(_tagIdSeed)     #_.joe - joe is contextual scope lookup
OUTER_NAME = next(_tagIdSeed)       #.joe - joe causes the name in the enclosing scope to be passed automatically

# COMPOUND
NAME_COLON = next(_tagIdSeed)
ASSIGN_RIGHT = next(_tagIdSeed)

# PROCESSED NAME_COLON
ASSIGN_LEFT = next(_tagIdSeed)
KEYWORD_FRAGMENT = next(_tagIdSeed)
GLOBAL_ASSIGN_LEFT = next(_tagIdSeed)
GLOBAL_ASSIGN_RIGHT = next(_tagIdSeed)
CONTEXT_ASSIGN_LEFT = next(_tagIdSeed)
CONTEXT_ASSIGN_RIGHT = next(_tagIdSeed)

# LITERALS
DECIMAL = next(_tagIdSeed)
INTEGER = next(_tagIdSeed)
STRING = next(_tagIdSeed)
SYMS = next(_tagIdSeed)
SYM = next(_tagIdSeed)
GLOBALTIMESTAMP_SS = next(_tagIdSeed)
GLOBALTIMESTAMP_S = next(_tagIdSeed)
GLOBALTIMESTAMP_M = next(_tagIdSeed)
LOCALTIMESTAMP_SS = next(_tagIdSeed)
LOCALTIMESTAMP_S = next(_tagIdSeed)
LOCALTIMESTAMP_M = next(_tagIdSeed)
DATE = next(_tagIdSeed)
GLOBALTIME_SS = next(_tagIdSeed)
GLOBALTIME_S = next(_tagIdSeed)
GLOBALTIME_M = next(_tagIdSeed)
LOCALTIME_SS = next(_tagIdSeed)
LOCALTIME_S = next(_tagIdSeed)
LOCALTIME_M = next(_tagIdSeed)
ELLIPSES = next(_tagIdSeed)

LITERAL1 = DECIMAL
LITERAL2 = ELLIPSES

# GROUPING
L_BRACE = next(_tagIdSeed)
R_BRACE = next(_tagIdSeed)
L_PAREN = next(_tagIdSeed)
R_PAREN = next(_tagIdSeed)
L_BRACKET = next(_tagIdSeed)
R_BRACKET= next(_tagIdSeed)
L_ANGLE_COLON = next(_tagIdSeed)
R_ANGLE = next(_tagIdSeed)
L_BRACE_BRACKET = next(_tagIdSeed)       # for functions
L_PAREN_BRACKET = next(_tagIdSeed)       # for tables
L_BRACE_PAREN = next(_tagIdSeed)         # for functions

ILLEGAL_MANY_DOTS = next(_tagIdSeed)
ILLEGAL_TWO_DOTS = next(_tagIdSeed)
ILLEGAL_NAME = next(_tagIdSeed)
ILLEGAL_GLOBAL_NAME = next(_tagIdSeed)
ILLEGAL_GLOBAL_ASSIGN_LEFT = next(_tagIdSeed)
ILLEGAL_GLOBAL_ASSIGN_RIGHT = next(_tagIdSeed)
ILLEGAL_CONTEXT_NAME = next(_tagIdSeed)
ILLEGAL_CONTEXT_ASSIGN_LEFT = next(_tagIdSeed)
ILLEGAL_CONTEXT_ASSIGN_RIGHT = next(_tagIdSeed)
ILLEGAL_OUTER_NAME = next(_tagIdSeed)

ILLEGAL1 = ILLEGAL_MANY_DOTS
ILLEGAL2 = ILLEGAL_OUTER_NAME

_NUM_TAGS = next(_tagIdSeed)

prettyNameByTag = [''] *_NUM_TAGS
prettyNameByTag[LINE_COMMENT] = 'LINE_COMMENT'
prettyNameByTag[C_COMMENT] = 'C_COMMENT'
prettyNameByTag[SECTION] = 'SECTION'
prettyNameByTag[COLON] = 'COLON'
prettyNameByTag[COMMA] = 'COMMA'
prettyNameByTag[SEMI_COLON] = 'SEMI_COLON'
prettyNameByTag[DOT] = 'DOT'
prettyNameByTag[LINE_BREAK] = 'LINE_BREAK'
prettyNameByTag[NAME] = 'NAME'
prettyNameByTag[OPERATOR] = 'OPERATOR'
prettyNameByTag[DECIMAL] = 'DECIMAL'
prettyNameByTag[INTEGER] = 'INTEGER'
prettyNameByTag[STRING] = 'STRING'
prettyNameByTag[SYMS] = 'SYMS'
prettyNameByTag[SYM] = 'SYM'
prettyNameByTag[GLOBALTIMESTAMP_SS] = 'GLOBALTIMESTAMP_SS'
prettyNameByTag[GLOBALTIMESTAMP_S] = 'GLOBALTIMESTAMP_S'
prettyNameByTag[GLOBALTIMESTAMP_M] = 'GLOBALTIMESTAMP_M'
prettyNameByTag[LOCALTIMESTAMP_SS] = 'LOCALTIMESTAMP_SS'
prettyNameByTag[LOCALTIMESTAMP_S] = 'LOCALTIMESTAMP_S'
prettyNameByTag[LOCALTIMESTAMP_M] = 'LOCALTIMESTAMP_M'
prettyNameByTag[DATE] = 'DATE'
prettyNameByTag[GLOBALTIME_SS] = 'GLOBALTIME_SS'
prettyNameByTag[GLOBALTIME_S] = 'GLOBALTIME_S'
prettyNameByTag[GLOBALTIME_M] = 'GLOBALTIME_M'
prettyNameByTag[LOCALTIME_SS] = 'LOCALTIME_SS'
prettyNameByTag[LOCALTIME_S] = 'LOCALTIME_S'
prettyNameByTag[LOCALTIME_M] = 'LOCALTIME_M'
prettyNameByTag[L_BRACE] = 'L_BRACE'
prettyNameByTag[R_BRACE] = 'R_BRACE'
prettyNameByTag[L_PAREN] = 'L_PAREN'
prettyNameByTag[R_PAREN] = 'R_PAREN'
prettyNameByTag[L_BRACKET] = 'L_BRACKET'
prettyNameByTag[R_BRACKET] = 'R_BRACKET'
prettyNameByTag[L_ANGLE_COLON] = 'L_ANGLE_COLON'
prettyNameByTag[R_ANGLE] = 'R_ANGLE'
prettyNameByTag[L_BRACE_BRACKET] = 'L_BRACE_BRACKET'
prettyNameByTag[L_BRACE_PAREN] = 'L_BRACE_PAREN'
prettyNameByTag[L_PAREN_BRACKET] = 'L_PAREN_BRACKET'
prettyNameByTag[NAME_COLON] = 'NAME_COLON'
prettyNameByTag[ASSIGN_LEFT] = 'ASSIGN_LEFT'
prettyNameByTag[KEYWORD_FRAGMENT] = 'KEYWORD_FRAGMENT'
prettyNameByTag[ASSIGN_RIGHT] = 'ASSIGN_RIGHT'
prettyNameByTag[CONTINUATION] = 'CONTINUATION'
prettyNameByTag[ELLIPSES] = 'ELLIPSES'
prettyNameByTag[ILLEGAL_MANY_DOTS] = 'ILLEGAL_MANY_DOTS'
prettyNameByTag[ILLEGAL_TWO_DOTS] = 'ILLEGAL_TWO_DOTS'

prettyNameByTag[ILLEGAL_NAME] = 'ILLEGAL_NAME'
prettyNameByTag[ILLEGAL_GLOBAL_NAME] = 'ILLEGAL_GLOBAL_NAME'
prettyNameByTag[ILLEGAL_GLOBAL_ASSIGN_RIGHT] = 'ILLEGAL_GLOBAL_ASSIGN_RIGHT'
prettyNameByTag[ILLEGAL_CONTEXT_NAME] = 'ILLEGAL_CONTEXT_NAME'
prettyNameByTag[ILLEGAL_OUTER_NAME] = 'ILLEGAL_OUTER_NAME'
prettyNameByTag[ILLEGAL_GLOBAL_ASSIGN_LEFT] = 'ILLEGAL_GLOBAL_ASSIGN_LEFT'

prettyNameByTag[GLOBAL_ASSIGN_LEFT] = 'GLOBAL_ASSIGN_LEFT'
prettyNameByTag[GLOBAL_ASSIGN_RIGHT] = 'GLOBAL_ASSIGN_RIGHT'
prettyNameByTag[GLOBAL_NAME] = 'GLOBAL_NAME'
prettyNameByTag[CONTEXT_ASSIGN_LEFT] = 'CONTEXT_ASSIGN_LEFT'
prettyNameByTag[CONTEXT_ASSIGN_RIGHT] = 'CONTEXT_ASSIGN_RIGHT'
prettyNameByTag[CONTEXT_NAME] = 'CONTEXT_NAME'
prettyNameByTag[OUTER_NAME] = 'OUTER_NAME'

prettyNameByTag= tuple(prettyNameByTag)


# see https://regex101.com/r/mtZL62/1


# [abc]  a single character matching a b or c
# [^abc]  any single character except a b or c
# [a-z] a single character in range a...z  [A-Z] [0-9]
# .   any single character
# \s - any whitespace character,   \S - any non-whitespace character
# \d - any digit,  \D - any non-digit
# \w - word character i.e. [a-zA-Z0-9_],  \W -
# \v - vertical whitespace (newline and vertical tab)
# (a|b)    either a or b
# a? - zero or one
# a* - zero or more - greedy quantifier - e.g. `a.*a` for "greedy can be dangerous at times" matches "an be dangerous a"
# a*? - Matches as few characters as possible. /r\w*?/  r re regex
# a+ - one or more
# a{3} - exactly three of a
# a{3,} - three or more of a
# a{4-6} - four to six of a
# \b - b is any metacharacter, i.e.  [ ] ^ - \ ( ) | { } ? , . as well as \n, \t, \r \0

# (?#This is a comment)
# (?P<name>...) - named capture group rather than a number, (?P<firstName>Sally)
# (?P=name) - Matches the text matched by a previously named capture group. This is the python specific notation.
# (?(1)yes|no) - If capturing group 1 was matched so far, matches the pattern before the vertical bar. Otherwise,
#      matches the pattern after the vertical bar. A group name, or a relative position (-1) in PCRE, can be used. Global
#      flag breaks conditionals.

# (...)\n - Usually referred to as a `backreference`, this will match a repeat of `...` in a previous set of parentheses. To
#      reduce ambiguity one may also use `\gn`, or `\g{n}` where m is a digit. e.g. (.)\1
# (...) - CAPTURE everything enclosed, parts of the regex enclosed in parentheses may be referred to later in the
#      expression or extracted from the results of a successful match. `(abc)` checks for `abc`
# (?:...) - MATCH everything enclosed,  e.g. `(?:abc)` checks for `abc` - this construct is similar
#      to (...), but won't create a capture group.


# ^ - start of string - Matches the start of a string without consuming any characters. If multiline mode is used, this will
#      also match immediately after a newline character. e.g. "start of string" >> RE >> "^\w+" answers "start"
# $ - end of string

# (?=...) - positive lookahead - without consuming characters does the expression match the FOLLOWING characters?
#      "foobaz" >> RE >> "foo(?=(bar|baz))" >> assertEquals >> (0, 3, 'foo')
# (?!...) - negative lookahead - without consuming characters does the expression NOT match the FOLLOWING characters?
#      "foobah" >> RE >> "foo(?!(bar|baz))" >> assertEquals >> (0, 3, 'foo')
# (?<=...) - positive lookbehind - without consuming characters does the expression match the PREVIOUS characters?
#      "afoobar" >> RE >> "\w{4}(?<=foo)bar" >> assertEquals >> (0, 7, 'afoobar')
# (?<!...) - negative lookbehind - without consuming characters does the expression NOT match the PREVIOUS characters?
#      "not bar" >> RE >> ".{4}(?<!(but ))bar" >> assertEquals >> (0, 7, 'not bar')


@coppertop
def RE(string, rule):
    regex = rule >> compileBonesRE
    match = regex.match(string, 0)
    if match:
        return match.start(), match.end(), string[match.start():match.end()], match.groups()
    else:
        return Missing

@coppertop
def compileBonesRE(rule):
    rule = "".join(re.split('\s', rule))    # strips out whitespace
    rule = " ".join(re.split('<sp>', rule))  # adds back in deliberate spaces
    return re.compile(rule)

    # rules is pretty much constant but used in unit tests

    # (r'(?<![.a-zA-Z])([a-zA-Z][a-zA-Z_0-9]*)', NAME),

_NAME_RE = '''
    ([a-zA-Z_]\w*\.)*   (?#zero or more {name,dot})
    ([a-zA-Z_]\w*)      (?#name)
'''

_OUTER_NAME_RE = r'''
    (\.+)               (?#dots)
    ([a-zA-Z_]\w*\.)*   (?#zero or more {name,dot})
    ([a-zA-Z_]\w*)      (?#name)
'''
#    \.*                (?one or more dots)

_CONTEXT_NAME_RE = r'''
    (_\.)               (?#underscore,dot)
    ([a-zA-Z_]\w*\.)*   (?#zero or more {name,dot})
    ([a-zA-Z_]\w*)      (?#name)
'''

_CONTEXT_ASSIGN_LEFT_RE = r'''
    (_\.)               (?#underscore,dot)
    ([a-zA-Z_]\w*\.)*   (?#zero or more {name,dot})
    ([a-zA-Z_]\w*)      (?#name)
    (:)                 (?#colon)
'''

_CONTEXT_ASSIGN_RIGHT_RE = r'''
    (:_\.)              (?#colon,underscore,dot)
    ([a-zA-Z_]\w*\.)*   (?#zero or more {name,dot})
    ([a-zA-Z_]\w*)      (?#name)
'''

_GLOBAL_NAME_RE = r'''
    (_\.\.)             (?#underscore,dot,dot)
    ([a-zA-Z_]\w*\.)*   (?#zero or more {name,dot})
    ([a-zA-Z_]\w*)      (?#name)
'''

_GLOBAL_ASSIGN_LEFT_RE = r'''
    (_\.\.)             (?#underscore,dot,dot)
    ([a-zA-Z_]\w*\.)*   (?#zero or more {name,dot})
    ([a-zA-Z_]\w*)      (?#name)
    (:)                 (?#colon)
'''

_GLOBAL_ASSIGN_RIGHT_RE = r'''
    (:_\.\.)            (?#colon,underscore,dot,dot)
    ([a-zA-Z_]\w*\.)*   (?#zero or more {name,dot})
    ([a-zA-Z_]\w*)      (?#name)
'''



_bonesLexRules = [
    (r'[<sp>]+', LEADING_SPACES),
    (r'[<sp>\t]+', WHITE_BREAK),

    # the lexer captures all the enclosed text of these next three
    (r"(\'\()(([\S\s]*?[^\\](\\\\)*))(\')", SECTION),      # starts '(sectionType)... ends '
    (r"(/\*)(([\S\s]*?[^\\](\\\\)*))(\*/)", C_COMMENT),  # starts /* ends */
    (r'\/\/[^\n]*', LINE_COMMENT),  # starts // ends \n
    (r'[\n]+', LINE_BREAK),
    (r'(\")(([\S\s]*?[^\\](\\\\)*))\1', STRING),
    (r'(`\w+){2,}', SYMS),
    (r'(`\w+)', SYM),
    (_GLOBAL_ASSIGN_LEFT_RE, GLOBAL_ASSIGN_LEFT),
    (_GLOBAL_NAME_RE, GLOBAL_NAME),
    (_GLOBAL_ASSIGN_RIGHT_RE, GLOBAL_ASSIGN_RIGHT),
    (_CONTEXT_ASSIGN_LEFT_RE, CONTEXT_ASSIGN_LEFT),
    (_CONTEXT_NAME_RE, CONTEXT_NAME),
    (_CONTEXT_ASSIGN_RIGHT_RE, CONTEXT_ASSIGN_RIGHT),
    (_OUTER_NAME_RE, OUTER_NAME),
    (_NAME_RE, NAME),
    (r'[1-2][0-9][0-9][0-9]\.[0-1][0-9]\.[0-3][0-9]D[0-9][0-9]:[0-9][0-9]:[0-9][0-9]\.[0-9]+[A-Z][A-Z][A-Z]', GLOBALTIMESTAMP_SS),          # must come before DATE
    (r'[1-2][0-9][0-9][0-9]\.[0-1][0-9]\.[0-3][0-9]D[0-9][0-9]:[0-9][0-9]:[0-9][0-9][A-Z][A-Z][A-Z]', GLOBALTIMESTAMP_S),
    (r'[1-2][0-9][0-9][0-9]\.[0-1][0-9]\.[0-3][0-9]D[0-9][0-9]:[0-9][0-9][A-Z][A-Z][A-Z]', GLOBALTIMESTAMP_M),
    (r'[1-2][0-9][0-9][0-9]\.[0-1][0-9]\.[0-3][0-9]D[0-9][0-9]:[0-9][0-9]:[0-9][0-9]\.[0-9]+', LOCALTIMESTAMP_SS),  # must come before DATE
    (r'[1-2][0-9][0-9][0-9]\.[0-1][0-9]\.[0-3][0-9]D[0-9][0-9]:[0-9][0-9]:[0-9][0-9]', LOCALTIMESTAMP_S),
    (r'[1-2][0-9][0-9][0-9]\.[0-1][0-9]\.[0-3][0-9]D[0-9][0-9]:[0-9][0-9]', LOCALTIMESTAMP_M),
    (r'[1-2][0-9][0-9][0-9]\.[0-1][0-9]\.[0-3][0-9]', DATE),          # must come before DECIMAL
    (r'[0-9][0-9]:[0-9][0-9]:[0-9][0-9]\.[0-9]+[A-Z][A-Z][A-Z]', GLOBALTIME_SS),
    (r'[0-9][0-9]:[0-9][0-9]:[0-9][0-9][A-Z][A-Z][A-Z]', GLOBALTIME_S),
    (r'[0-9][0-9]:[0-9][0-9][A-Z][A-Z][A-Z]', GLOBALTIME_M),
    (r'[0-9][0-9]:[0-9][0-9]:[0-9][0-9]\.[0-9]+', LOCALTIME_SS),
    (r'[0-9][0-9]:[0-9][0-9]:[0-9][0-9]', LOCALTIME_S),
    (r'[0-9][0-9]:[0-9][0-9]', LOCALTIME_M),
    (r'\((\s)*\[', L_PAREN_BRACKET),
    (r'{(\s)*\[', L_BRACE_BRACKET),
    (r'{(\s)*\(', L_BRACE_PAREN),
    (r'\(', L_PAREN),
    (r'\)', R_PAREN),
    (r'\[', L_BRACKET),
    (r'\]', R_BRACKET),
    (r'{', L_BRACE),
    (r'}', R_BRACE),
    (r'<:', L_ANGLE_COLON),
    (r'>', R_ANGLE),
    (r'[0-9]+\.[0-9]+', DECIMAL),                           # must come before INTEGER and after DATE etc
    (r'[0-9]+', INTEGER),
    (r'\\(^\t| )*[\n]', CONTINUATION),                     # consumes just one \n
    (r'[<>!=#_@$%^&*+/|~\'\?\-]{1,3}', OPERATOR),  # comes after STRING, and NAME
    (r'[\.]{4,}', ILLEGAL_MANY_DOTS),
    (r'(\.\.\.)', ELLIPSES),
    (r'(\.\.)', ILLEGAL_TWO_DOTS),
    (r'\.', DOT),
    (r',', COMMA),
    (r';', SEMI_COLON),
    (r':', COLON),

]

_atomicTags = set([
    DOT, COMMA, SEMI_COLON, COLON, CONTINUATION, ELLIPSES, WHITE_BREAK, LEADING_SPACES, LINE_BREAK,
    L_PAREN, L_BRACKET, L_BRACE, L_ANGLE_COLON, L_PAREN_BRACKET, L_BRACE_BRACKET, L_BRACE_PAREN,
    R_PAREN, R_BRACKET, R_BRACE, R_ANGLE
])



Token = collections.namedtuple('Token', 'src, tag, indent, n, c1, c2, l1, l2')
# n - token number in output
# l1, l2 - line number
# c1, c2 - offset in line
# Token.__str__ = Token.__repr__
Token.__repr__ = lambda self:('{%s}' % (prettyNameByTag[self.tag])) if (self.tag in _atomicTags) else ('{%s:%s}' % (prettyNameByTag[self.tag], self.src))
@property
def _PPGroup(self):
    tag = self.tag
    if tag == ASSIGN_LEFT:
        return '{%s:}' % self.src
    if tag == ASSIGN_RIGHT:
        return '{:%s}' % self.src
    if tag == GLOBAL_ASSIGN_LEFT or tag == GLOBAL_ASSIGN_RIGHT:
        return '{%s}' % self.src
    if LITERAL1 <= tag and tag <= LITERAL2:
        return 'l'
    if tag == NAME:
        return 'n'
    if tag == OUTER_NAME:
        return '.n'
    if tag == OPERATOR:
        return 'o'
    return self.__repr__()
Token.PPGroup = _PPGroup

TagSrc = collections.namedtuple('TagSrc', 'tag, src')

Line = collections.namedtuple('Line', 'num, c1, c2, src')


def lexBonesSrc(src, symbols):

    rules = _bonesLexRules

    # CAPTURE LINE NUMBERS
    lines = ['THE START']           # lines start at 1 so need something to take up slot 0
    NL = re.compile(r'[\n]')
    allUpToNL = re.compile(r'[^\n]*')
    pos = 0
    lineNum = 1
    # get the first ine
    match = allUpToNL.match(src, pos)
    line = match.group()
    c1 = match.start()
    c2 = match.end()
    lines.append(Line(lineNum, c1, c2, line) )
    # print('lexing.lexBonesSrc: %r %r %r %r \n' % (lineNum, c1, c2, line))
    pos = c2
    while match:
        # move to the next line
        match = NL.match(src, pos)
        if match:
            pos = match.end()
            lineNum += 1
            # get the line
            match = allUpToNL.match(src, pos)
            line = match.group() if match else ""
            c1 = match.start()
            c2 = match.end()
            lines.append(Line(lineNum, c1, c2, line))
            # print('%r %r %r %r' % (lineNum, c1, c2, line))
            pos = c2


    # TOKENISE SRC
    pos = 0
    tokens = []
    rules = [(pattern >> compileBonesRE, tag) for (pattern, tag) in rules]
    l1 = 1
    indent = 0
    priorTag = None
    while pos < len(src):
        for regex, tag in rules:
            match = regex.match(src, pos)
            if match:
                if tag == LEADING_SPACES:
                    if indent == 0:
                        indent = match.end() - match.start()
                elif tag == WHITE_BREAK:
                    pass
                else:
                    c1 = match.start()
                    c2 = match.end()
                    while c1 > lines[l1].c2:
                        l1 += 1
                    l2 = l1
                    while c2 > lines[l2].c2:
                        l2 += 1
                    text = match.group()
                    # the name regexes consume any extra dots - these are illegal so change the tag name accordinglys
                    if text[-1] == '.':
                        if tag == NAME: tag = ILLEGAL_NAME
                        if tag == GLOBAL_NAME: tag = ILLEGAL_GLOBAL_NAME
                        if tag == GLOBAL_ASSIGN_RIGHT: tag = ILLEGAL_GLOBAL_ASSIGN_RIGHT
                        if tag == CONTEXT_NAME: tag = ILLEGAL_CONTEXT_NAME
                        if tag == OUTER_NAME: tag = ILLEGAL_OUTER_NAME
                    if tag == GLOBAL_ASSIGN_LEFT:
                        if text[-2] == '.':
                            tag = ILLEGAL_GLOBAL_ASSIGN_LEFT
                    # I'm not confident that it's quicker for me to implement the following in regex, and I'm not
                    # confident regex will execute it any faster. Adding state to the lex loop feels a little hacky but
                    # appropiate if lexing is taken as a whole however I suspect this little state machine could
                    # be generalised. The following implies that a:b is NAME_COLON and
                    # that a space is needed for ASSIGN_RIGHT, i.e. a :b
                    if  (priorTag in (NAME, )) and tag == COLON:
                        # merge NAME COLON sequence (with no WHITE_BREAK in between) into a NAME_COLON
                        tag = NAME_COLON
                        priorToken = tokens[-1]
                        tokens[-1] = Token(priorToken.src, tag, indent, priorToken.n, priorToken.c1, c2, priorToken.l1, l2)
                    elif priorTag == COLON and (tag in (NAME, GLOBAL_NAME)):
                        # merge COLON NAME sequence (with no WHITE_BREAK in between) into a ASSIGN_RIGHT
                        tag = ASSIGN_RIGHT
                        tokens[-1] = Token(text, tag, indent, len(tokens), c1, c2, l1, l2)
                    elif tag == SYM:
                        sym = symbols.Sym(text[1:])
                        tokens.append(Token(sym, tag, indent, len(tokens), c1, c2, l1, l2))
                    elif tag == SYMS:
                        syms = [symbols.Sym(t) for t in text.split('`')[1:]]
                        tokens.append(Token(syms, tag, indent, len(tokens), c1, c2, l1, l2))
                    elif tag in (L_BRACE_BRACKET, L_PAREN_BRACKET):
                        tokens.append(Token(''.join(text.split()), tag, indent, len(tokens), c1, c2, l1, l2))
                    else:
                        if tag == LINE_BREAK and indent + 1 == (c2 - lines[l1].c1):
                            # set blank lines to have indent of 0 (thus forcing a new phrase)
                            tokens.append(Token(text, tag, 0, len(tokens), c1, c2, l1, l2))
                        else:
                            tokens.append(Token(text, tag, indent, len(tokens), c1, c2, l1, l2))
                if tag in (LINE_BREAK, CONTINUATION):
                    indent = 0
                break
        if (ILLEGAL1 <= tag and tag <= ILLEGAL2):
            token = tokens[-1]
            raise RuntimeError(f'Illegal token: {token.src} @line {token.l1}:  {lines[token.l1].src}')
        if not match:
            token = tokens[-1]
            raise RuntimeError(f'Illegal character: {src[pos:pos+1]} @line {token.l1}:  {lines[token.l1].src}')
        pos = match.end()
        priorTag = tag

    # OUTPUTS - line number src, tokens, symbols
    return tokens, lines


