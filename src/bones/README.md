## BONES

Bones is a scalable, minimalist, high level scripting language (intended for people ages 8 - 80+) for data wrangling 
and algorithm development combining the pithiness of kdb/q and the readability of Smalltalk with multiple-dispatch, 
partial functions and a strong algebraic type system.

<br>
Fundamental values

Bones should help us faithfully represent our ideas so we can use the computer for tasks we can't do in our heads.

- it should point out mistakes in our code like a word processing identifies spelling and grammatical errors
- it should be productive to express our thinking in a clear manner that can be reasoned about
- it should be accessible and discoverable

And, almost most importantly, it should be fun to do so and result in pleasing and elegant code.

<br>
Implementing the fundamental values

The language is designed and implemented such that:

- Values are immutable
- The scope of names are is controlled (in a way differnt to most langauge)
- Strong typing helps identify bugs
- Some weakness from source code (where the user lives) to first function call can ease the type burden safely
- Subtyping helps constrain and compartmentalise behaviour into understandable chunks
- Easy composition is key to expressivity
- Polymorphism helps reduce clutter and reuse ideas
- Type inference also helps to reduces clutter
- The programmer should have no anxiety that any slowness can't be addressed with ease

<br>

### SYNTAX

#### comments

```
// a comment
```

<br>

#### separators
Almost everything in bones is an expression. These are separated by either by full-stops, or by, 
new-lines with no following indentation.

```
(1,2,3) each print. (4,5,6) each print      // two expressions separated by .
1 + 1. 2+2
```

```
(1,2,3) each print                          // separated by a new line and no indentation
(4,5,6) each print
```

```
(1,2,3)                                     // a new line but next line is indented
    each print
(4,5,6)                                     // now we have a new expression
    each                                    // print has not collaspes the indentation so continue
    print
(7,8,9) each                                // (7,8.. terminates the indentation run
    print
```

<br>

#### some literals

```
1                       - a literal integer
1.0                     - a literal decimal
2000.01.01
16:15
"hello"
`fred                   - a symbol
`fred`joe`sally         - a list of symbols
(1,2,3)                 - a list of literal integers
(1,0,0;0,1,0;0,0,1)     - a 2 dimensional list of literal integers
```

<br>

#### function calls
```
aConstantValue()
join("Hello ", "world!")
```

#### pipe style

precedence is left to right with the exception of ^, * and / which follow elementary grade BODMAS

```
1 addOne
1 add 2
1 + 2
(1,2,3) each print
(1,2,3) both add (1,2,3)
expr ifTrue: "yes" ifFalse: "no"
(1 + 2) * 3
("a", "b", "c") (3, 2, 1)
```


<br>

#### ordinals
index, offset, excel, roman \
Default ordinal (i.e. how a literal int is interpreted) is the index rather than the offset

<br>

#### functions
```
{[a] a + 1}
{x + 1}
```

<br>

#### assignments
```
addOne: {x + 1}
{x join "One"} :addOne
pad`Re[player].state.1: YES         // product access, exponential access
a, b: (1,2)
```

<br>

#### names
values may be named a-z, A-Z, 0-9 and _ \
functions may be named with the same rules or alternatively by using +-=!@£$%^&*|\\/~?#<> \
()[]{}"`.,; are reserved by bones \
Some sequences are also reserved, i.e. //, <:..>, {...}, {[...]...}, ([...]...)

<br>

### type tags
```
1 <:offset>
{[x:num] x + 1}<:num> :addOne
```

<br>

#### including other code
```
requires bones.std                          // loads a module into the kernel
from bones.std use each, print           // adds the name each and print to this module's scope
```

<br>

#### scopes
```
_.contextVar
_..aGlobalVar
__.aClosureVarFromMyParentsScopeActuallyImplementedAsAPartial
__..aClosureVarFromMyParentsParentsScopeActuallyImplementedAsAPartial
```

<br>

### TYPE SYSTEM + TYPE LANG

core types \
atoms \
structs \
tuples \
lists \
maps \
functions \
variants \
sub-types 

auto converting

<br>

### THEORETICALLY

atoms, products (tuple, struct), exponentials (ordinals, maps, functions), unions and sums, 
intersections, weakness

