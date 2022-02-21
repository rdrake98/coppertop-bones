Like Smalltalk, bones is a simple language based around message sending - everything is reduced to lists of 
expressions with an expression being comprised of name access (get/set), literal values and multi-dispatch to 
functions.

The grammars of the lex, grouping and expression parsing components are not context free. (Type lang might be but 
I actually don't know as I haven't implemented it yet). The various parsers contain state machines that consume an 
input stream and typically operate independently but sometimes cooperatively. 

It is important to have a grasp of the overall grand scheme, i.e. the globally recognised tokens that demark lists.

dotlist -> `a. b`
commalist -> `a, b`
dotcommsemicolonlist is of the form `a. b, c. d; e. f, g. h`  - allows a matrix of parargraphs

We have no statements in bones (whatever that means) only expressions. An expression may return one or more values 
to one or more names and is a sequence of nouns and verbs. Thus we could term it a sentance. It is separated from 
other sentances by a full stop or with a bit more context by a new line. We term a sequence of sentances a paragraph.

Names may be nouns or verbs - higher-order-functions could be described as adverbs (like q/kdb) but that is probably
unnecessary and may be obfuscating.

words 

(matrixOfParagraphs)
\[matrixOfParagraphs]
{paragraph}
{[]paragraph}
{()paragraph}
'(...)...'
<:...>
(\[...]...)


'(requires) commalist' of module names

or

requires commalist


