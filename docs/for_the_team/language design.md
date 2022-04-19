This doc is targeted at bones developers rather than bones users, though, as always, the terminology is more 
geared to the latter than the former. Not withstanding that we do refer to computer science concepts to show 
linkage to theory.


NOMENCLATURE

value

function

type

name
a name is a label comprised of alphabetical characters (a-z and A-Z) and _
names can refer to values, functions, and types

operator
an operator is a name that is comprised of non-alphabetical characters


scope
in bones we group names into sets - if we kept all the names in one global set we would find that limits the scale of 
the problems we can solve with bones. we term these sets "scopes".



PRINCIPLES


1. reasonable

This means bones code should be easy to reason about (not that it treats you fairly!).


1.1. easy to know the thing a name refers to

type lang names are global in nature.

function names are inherited from a function's parent, a function's parent's parent and so on.

value names explicitly state the scope in which the value lives - i.e. there is no inheritance of value names.

no prefix - local scope
_.name contextual scope
_..name global scope
.name parent scope
..name parent's parent scope

Values from a parent are fixed when the function definition is first encountered when executing code in a scope - the 
function is already assembled at this point but no parent values have been bound. We don't allow these functions to 
be passed out of the local scope though can be passed to a child scope.

Our purpose in this restriction is to increase the ease of referential transparency. It is inspired by q/kdb and turned
out to be surprisingly helpful in reducing bugs and not so onerous as a programmer might first think.


1.2. explicit rather than implicit

This is captured in The Zen of Python but this point has been made many times elsewhere.


1.3. BIDMAS precedence



2. scalable




2.1. the how vs the what and the why

In any piece of code we want to reduce the amount of ink devoted to the how, make the what as clear as possible and 
possibly even hint at the why. 



