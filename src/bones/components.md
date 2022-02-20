
bones.lang.lex - fairly straightforwards

bones.lang.group - first pass of our parser that separates out individual expressions

bones.lang.parse - hand-crafted expression parser as the syntax is not context-free - e.g. names can only be of one piping style

bones.lang.tc - tree-code (TC) - basically an AST

bones.lang.types - types used in bones.lang

bones.lang.checker - checks / infers tc types 

bones.kernel
  - environment / state
    - global key value store, 
    - module names
    - parsed and compiled fragments - tc, bc, ir, jit mc, transpiled, ffi fns
    - handles
  - parse - source to tc
    - can invalidate prior binding optimisations, e.g. when a function is added, changed or removed
  - compile - tc to bc, ir, mc
  - call - fn with args
  - evaluate - parsed / compiled expression
  - can communicate over nng or via api (i.e. kernel is embedded in something else, e.g. python, repl, jupyer, excel etc)
  - debugger protocol

bones.core.metatypes - fitsWithin and the various type classes

bones.core.types - standard types

bones.core.structs

