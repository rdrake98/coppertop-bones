## coppertop - some batteries Python didn't come with

(This readme covers _coppertop_,  for _bones_ see [here](https://github.com/DangerMouseB/coppertop-bones/blob/main/src/bones/README.md)
)

As well as some minor batteries that Python didn't come with (a couple of error types, module utils, 
and sentinals for missing, null, tbc, void, etc), coppertop provides a bones-style aggregation 
manipulation experience via the following:

* partial functions
* piping syntax
* multiple-dispatch
* type system with nominal, intersection, union, product, and exponential types with type variables
* immutable updates
* contextual scope
* and a embryonic [library](https://github.com/DangerMouseB/examples/tree/main/src/dm/dm/std) of common pipeable functions 


<br>

### Partial functions

By decorating a function with @coppertop (and importing _) we can easily create partial functions, for example:

syntax: `f(_, a)` -> `f(_)`  \
where `_` is used as a sentinel place-holder for arguments yet to be confirmed (TBC)

```
from coppertop.pipe import *

@coppertop
def appendStr(x, y):
    assert isinstance(x, str) and isinstance(y, str)
    return x + y

appendWorld = appendStr(_, " world!")

assert appendWorld("hello") == "hello world!"
```

<br>


### Piping syntax

The @coppertop function decorator also extends functions with the `>>` operator
and so allows code to be written in a more essay style format - i.e. left-to-right and 
top-to-bottom. The idea is to make it easy to express the syntax (aka sequence) of a solution.


<br>

#### unary style - takes 1 piped argument and 0+ called arguments

syntax: `A >> f(args)` -> `f(args)(A)`

```
from dm.std import anon

@coppertop
def addOne(x):
    return x + 1

1 >> addOne
"hello" >> appendStr(_," ") >> appendStr(_, "world!")

1 >> anon(lambda x: x +1)
```

<br>

#### binary style - takes 2 piped argument and 0+ called arguments

syntax: `A >> f(args) >> B` -> `f(args)(A, B)`

```
from coppertop.core import NotYetImplemented
from dm.std import each, inject

@coppertop(style=binary)
def add(x, y):
    return x + y

@coppertop(style=binary)
def op(x, action, y):
    if action == "+":
        return x + y
    else:
        raise NotYetImplemented()

1 >> add >> 1
1 >> op(_,"+",_) >> 1
[1,2] >> each >> (lambda x: x + 1)
[1,2,3] >> inject(_,0,_) >> (lambda x,y: x + y)
```

<br>

#### ternary style - takes 3 piped argument and 0+ called arguments

syntax: `A >> f(args) >> B >> C` -> `f(args)(A, B, C)`

```
from dm.std import both, check, equal

[1,2] >> both >> (lambda x, y: x + y) >> [3,4] >> check >> equal >> [4, 6]
```

<br> 

#### as an exercise for the reader
```
[1,2] >> both >> (lambda x, y: x + y) >> [3,4] 
   >> each >> (lambda x: x * 2)
   >> inject(_,1,_) >> (lambda x,y: x * y)
   >> addOne >> addOne >> addOne
   >> to(_,pystr) >> appendStr(" red balloons go by")
   >> check >> equal >> ???
```

<br>


### Multiple-dispatch

Just redefine functions with different type annotations. Missing annotations are taken as 
fallback wildcards. Class inheritance is ignored when matching caller and function signatures.

```
@coppertop
def addOne(x:pyint) -> pyint:
    return x + 1
    
@coppertop
def addOne(x:pystr) -> pystr:
    return x + 'One'
    
@coppertop
def addOne(x):                 # fallback
    if isinstance(x, list):
        return x + [1]
    else:
        raise NotYetImplemented()

1 >> addOne >> check >> equal >> 2
'Three Two ' >> addOne >> check >> equal >> 'Three Two One'
[0] >> addOne >> check >> equal >> [0, 1]
```

<br>


### Type system

As an introduction, consider:

```
from bones.core.types import BTAtom, S, num, pyint, pystr, O
num = BTAtom.ensure('num')      # nominal
_ccy = BTAtom.ensure('_ccy')    # nominal
ccy = num & _ccy                # intersection
ccy + null                      # union
ccy * pyint * pystr             # tuple (sequence of types)
S(name=pystr, age=num)          # struct
N ** ccy                        # collection of ccy accessed by an ordinal (N)
pystr ** ccy                    # collection of ccy accessed by a python string
(num*num) ^ num                 # (num, num) -> num - a function
T, T1, T2, ...                  # type variable - to be inferred at build time

I(domestic=ccy&T, foreign=ccy&T)  # named intersection (aka discrimated type)
```

<br>

### Example - Cluedo notepad

See [algos.py](https://github.com/DangerMouseB/examples/blob/main/src/dm/dm/examples/cluedo/algos.py), where 
we track a game of Cluedo and make inferences for who did it. See [games.py](https://github.com/DangerMouseB/examples/blob/main/src/dm/dm/examples/cluedo/games.py) 
for example game input.

<br>

### Next

#### example bones code working end to end

For a suite of example .bones files:

* lex -> tokens
* group -> token groups + some markup
* parse -> untyped / partially typed TC (Tree Code aka AST)
* infer and check types -> typed TC (fully concrete and type templated - i.e. with type variables)
* build & bind (rebind affected concrete TC) -> concrete TC
* at this point a snippet will be runnable (assuming no type errors) - snippets are run on import and REPL / jupyter execution
* functions in the kernel can be called from python via something like `x = kernel.module.fn(a,b,c)`


#### determine how to do exception handling

We can easily add a trap function that converts a signal into a error value however we want to be pluralistic with 
implementation languages so may need a better sense of signal trapping at the TC or (hopefully not) langauge level.
In the sorts of use cases that bones is intended ofr typically errors can be modelled as data and although one can 
imagine that a far reaching escape (e.g. the ^ borrowed from Smalltalk) from the current path (e.g. over several 
functions) could be useful it is not clear that there isn't an elegant alternative.


#### collaborative / community developent / selection of a bones.std

Currently dm.std contains bits and pieces of library style code but Jeff Atwood's [The Delusion of Reuse and the Rule of Three](https://blog.codinghorror.com/the-delusion-of-reuse/) 
(also [Rule Of Three](https://blog.codinghorror.com/rule-of-three/))
implies that more than one common / standard library will emerge for bones and that it will arise from a 
joint focus and application into multiple use cases. Needless to say any bones.std should be as integrated and well 
designed as Smalltalk-80's / VisualWorks.


#### error messages

These should be outstandingly good. Grouping helps. ErrSite should help. They should be built into the type inference 
process too. The goal is that the error message should be enough for the program to instantly know how to fix the 
problem and not to have to hunt around to understand the message.


#### profiling

There's a popular quote about premature optimisation. The deeper question is why do people favour  fast 
code over clear code (asuuming they could write well and are not in a rush) when then code in question is not on the 
critical path? A couple of answers come to mind - the thrill of speed and an anxiety of not being fast enough. To
help bones programmers avoid this trap, we should have first class profiling - aggregated time within a scope as well 
as stopwatch style end to end aggregated time. I'm with Paul Graham on this one.

<br>

### Later

* Convert TC to Byte Code (BC), Internal Representation (IR) for a compiler (e.g. (MIR)[https://github.com/vnmakarov/mir/]
or possibly QBE, LLVM, etc) and / or Machine Code (MC).

