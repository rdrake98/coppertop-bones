THE TC BUILDING PROCESS

Our first target is to end up with executable tree code (TC). We have a multi step process:

1. lex - convert strings into tokens (which are tagged for easier consumption) - we also store int indent for the 
   line and source code locators (line and character ordinals)
2. group - the tokens are parsed into expression groups. Expression groups (EG) represent the overall structure 
   of the TC, for example:
    - SnippetEG represents a single chunk of source code from a client wanting to compile and call some bones code,
      such as a REPL, or a module etc
    - FunctionEG represents a bones function
   Each 'expression' in the group is a list of tokens for a single bones expression
3. parse - parse the tokens in the expression groups into TC fragments
4. assemble - combine the individual fragments into a syntactically valid TC whole
5. partial inference - run the inference algorithm on the TC as if it has no impact on the current kernel state
6. integrate - this may involve rebinding dispatches and generating new concrete functions and re-inferring kernel 
   state
7. accept / reject - in the perfect world we'd be able to try incorporating a piece of code whilst keeping the current 
   kernel state intact if the code turns out to be unacceptable
8. execute any top level expressions

   
Rollback on reject

It is easy to protect the current kernel state from errors in the lexing, grouping, parsing, assembling, and first 
inference stage, but it seems unlikely that integration errors will be recoverable - either the whole kernel would 
need to be persistent (even if just with two points in time) or a checkpoint would need to be created.


Key gotchas

The piping style of a function must be known before the parser encounters the function. This is because we allow bones 
code to define functions with any of the pipeline styles - nullary, unary, binary, ternary and 
right-associative-unaries (rau).

If there is a change in the set of functions that a dispatch can be bound to, for example adding a new function to the
kernel, then any existing dispatch sites that depend on that set of functions needs invalidating.

An 'operator' is merely a function with a non-alphabetical name.

Type lang has a different parser than bones and the 'operators' (+, -, *, **, ^) have an unusual precedence that 
increases brevity at the cost of unfamiliarity.

Functions are not created at execution time like they are with python but during the TC building process.


Important directional decisions

It is probably more important that really helpful error descriptions are generated - both for the user and for any 
tooling - than type inference is complete. Our inference should focus on helping the user and tooling rather than 
trying to be clever.



