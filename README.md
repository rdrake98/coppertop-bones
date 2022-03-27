## coppertop - some batteries Python didn't come with

(This readme covers _coppertop_,  for _bones_ see [here](https://github.com/DangerMouseB/coppertop-bones/blob/main/src/bones/README.md)
)

As well as some minor batteries that Python didn't come with (a couple of error types, module utils, 
and sentinals for missing, null, tbc, void, etc), coppertop provides a bones-style aggregation 
manipulation experience via the following:

* partial functions
* piping syntax
* multiple-dispatch
* type system with nominal, union, product, exponential and intersection types and type variables
* immutable updates
* contextual scope
* and a [standard library](https://github.com/DangerMouseB/examples/tree/main/src/dm/dm/std)


<br>

### Partial functions

By decorating a function with @coppertop (and importing _) we can easily create partial functions, for example:

syntax: `f(_, a) -> f(_)`  \
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

#### unary - takes 1 piped argument and 0+ called arguments

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

#### binary - takes 2 piped argument and 0+ called arguments

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

#### ternary - takes 3 piped argument and 0+ called arguments

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


### Templated type system

As an introduction, consider:

```
from bones.core.types import BTAtom, S, num, pyint, pystr, O
num = BTAtom.ensure('num')      # nominal
_ccy = BTAtom.ensure('_ccy')    # nominal
ccy = num & _ccy                # intersection
ccy + null                      # union
ccy * pyint * pystr             # tuple (sequence of types)
S(name=pystr, age=num)          # struct
N ** ccy                        # collection of ccy accessed by an ordinal
pystr ** ccy                    # collection of ccy accessed by a python string
(num*num) ^ num                 # (num, num) -> num - a function

I(domestic=ccy&T, foreign=ccy&T)  # named intersection (aka discrimated type)
```


### Example - Cluedo notepad

See [algos.py](https://github.com/DangerMouseB/examples/blob/main/src/dm/dm/examples/cluedo/algos.py), where 
we track a game of Cluedo and make inferences for who did it. See [games.py](https://github.com/DangerMouseB/examples/blob/main/src/dm/dm/examples/cluedo/games.py) 
for example game input.
