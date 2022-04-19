Here we keep plans that can be worked on - they need to be executable (see (Execution)[https://www.goodreads.com/book/show/1635.Execution]). 
We will define requirements at a vision / big picture level and a specific level. We use [critical thinking](https://www.criticalthinking.org/pages/defining-critical-thinking/766) 
as a framework for rigourously applying the many of the principles discussed in c2.com especially [evolutionary delivery](https://wiki.c2.com/?EvolutionaryDelivery) 
and [Objective's take on evolutionary delivery](https://wiki.c2.com/?SevenPillarsOfCred).

We express the requirements as failing acceptance tests.


## MINI PROJECT OVERVIEWS

<br>

### Next - Putting it all together

This is a biggie. Every component at some point has been working in some form and over time my understanding has 
evolved. It is time to get a minimal end-to-end, source to actual result example working.

test: /coppertop-bones/src/bones/bones/lang/tests/end_to_end_tests.py test_addOne

See /coppertop-bones/docs/for the team/building process/building.md etc for how source code is transformed into 
functions that can be called via the kernel.

steps in the building process:
* lex -> tokens
* group -> token groups + some markup
* parse -> untyped / partially typed TC (Tree Code aka AST)
* infer and check types -> typed TC (fully concrete and type templated - i.e. with type variables)
* build & bind (rebind affected concrete TC) -> concrete TC
* at this point a snippet will be runnable (assuming no type errors) - snippets are run on import and REPL / jupyter execution
* functions in the kernel can be called from python via something like `x = kernel.module.fn(a,b,c)`

TODO

* write tests for each step - to break the development down
* share tc.py and parse.py
* writes tests for BreadthFirstGroupVisitor and implement
* kernel namespace + stack scope and frame need defining




<br>

### Optimising filter-map

Consider \
python: `(1,2,3,4,5) >> select >> (lambda x: x >= 3) >> each >> (lambda x: x * x) >> sum` \
bones:  `(1,2,3,4,5) select {x >= 5} each {x*x} sum`

There are at least four approaches to implementing this.

1) unoptimised - each step outputs a value in memory (aka a buffer), e.g. `(1,2,3,4,5) -> (3,4,5) -> (9,16,25) -> 50`
   and the functions are called for each element in the loops
2) vectorised - again each step outputs a value but the loops are implemented in a higher performance langauge (e.g. 
   MC). This is simular to rewriting the code as something like `(1,2,3,4,5) :a where (a >= 5) :x * x sum`.
3) visited - each step answers a stateful visitor object which pulls the result from the prior step - similarly to 
   ranges, iterators, generators, etc.
4) faster imperative code is generated under-the-hood, e.g. [GHC optimisations](https://wiki.haskell.org/GHC_optimisations#Fusion)

The bones type system should be powerful enough to allow all four to be done as a PoC in Python.

See /examples/src/dm/dm/examples/deferred/test_deferred.py

In-place optimisation can also be included.

A key issue in this is the experience of the user trying to debug their code. If we assume that 1) gives the most 
intuitive execution sequence then the others can be hard to follow in a stepper (which steps in time order). We should
add a logger that can order log msgs in either time order or in intuitive order (i.e. as if the code were implemented
as 1) ).

#### TODO
* implement the logger
* implement the simple example in all four styles exploring how to indicate to the reader which style is being used and 
  giving control to the author to select a chosen style
