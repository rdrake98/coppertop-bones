


* lex -> tokens
* group -> token groups + some markup
* parse -> untyped / partially typed TC (Tree Code aka AST)
* infer and check types -> typed TC (fully concrete and type templated - i.e. with type variables)
* build & bind (rebind affected concrete TC) -> concrete TC
* at this point a snippet will be runnable (assuming no type errors) - snippets are run on import and REPL / jupyter execution
* functions in the kernel can be called from python via something like `x = kernel.module.fn(a,b,c)`

* compile - act of turning TC into BC, MC, IR etc


