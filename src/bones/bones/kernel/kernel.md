kernel is a global singleton that stores

- error explanations
- syms and enums
- strings and rope?
- types
- currently loaded code
  - coppertop fns
  - mir / ir
  - compiled code
  - abstract tc
  - tc
  - inference cache
- current values
  - sentinels (e.g. the sys singletons)
  - globals
  - context stack
  - handles
- memory allocations

It is the interface between bones and all other processes. APIs include:
  - jupyter kernel,
  - repl via stdin, stdout and stderr, 
  - as an actor (?) via nng, etc
  - python api
  - c api
  - debugging (VSCode and hopefully IntelliJ / PyCharm)



