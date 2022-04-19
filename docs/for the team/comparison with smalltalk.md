https://wiki.c2.com/?IfSmalltalkIsSoGoodWhyDoesNobodyUseIt

I've been thinking about why was Smalltalk so productive for many years since I stopped using it professionally in 1997

I concluded it was the coming together of many things but some things got in the way that made it less usable


### DIFFERENCES

image / kernel - build up rather than whittle down

file based

no classes - classes strike me as a clunky module system (and more about implementation of dispatch than anything else)

business focussed rather than systems focussed (IT focussed)
- immutable DAGs - back pointers prevented - which is okay for business scripting

multi dispatch rather than receiver (aka single) dispatch
- I suggest that late binding means flexible binding, rather than dynamic binding - see 
  https://www.quora.com/What-aspects-of-Lisp-influenced-Smalltalk
  - "For me, it was spending a Sunday afternoon in the late 60s tracing through John McCarthy’s eval-apply for Lisp 
    that rotated my perspective to thinking about computing “that way”." - Alan Kay
  - "Peter had realized that if you’ve got a really good live language, that you don’t need a separate OS"

type system + code gen rather than pointer indirection to solve polymorphism

no meta programming - instead easy ffi to python and c

statically type checked


### SIMILARITIES

small composable functions that promote scalability - this I think is the killer feature

uniform programming model - see [Lisp, Smalltalk, and the Power of Symmetry](https://medium.com/smalltalk-talk/lisp-smalltalk-and-the-power-of-symmetry-8bd96aaa0c0c#:~:text=Smalltalk%2C%20like%20Lisp%2C%20runs%20in,)%20as%20an%20s%2Dexpression.)
- "What makes Lisp powerful isn’t its macros, it’s the fact that Lisp runs in the same context it’s written in."

- "When I studied computer languages in college, the second language we looked at after Lisp was Smalltalk. I 
  had been so impressed with the power and flexibility of Lisp that the first question out of my mouth that 
  day was “does Smalltalk have macros?” My professor, after thinking it over for a second, replied 
  that “Smalltalk doesn’t need macros.” Huh? Smalltalk doesn’t need macros? Why not? What does it have instead? 
  It took me three years to figure it out: Smalltalk doesn’t need macros because it has classes instead."

so everything is message sending
- and almost everything is in the library
- HoF provides control

more declarative than imperative

piping syntactic style

global variables are explicit

simple syntax, keyword style function naming

pool variables -> context scope


