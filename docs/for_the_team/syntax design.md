Here we describe the bones syntax. 

### Decisions

Like the Smalltalk syntax bones syntax is intended to be very simple. Why? To reduce the amount of things one has to
be fluent in


There are two parts of bones 1) expressions / expression pipeline, 2) expression groups

we allow side inputs and outputs as part of expressions?

calculations
meta
i/o - intermediate and external (file, keyboard, graphs, grids, reports)
exceptions - I'm giving up, I quit, I can't do this

IMPORTANT
do we need try catch?



input from files / dbs / web etc
output to same


we might say it can only be done at top level BUT then we want to write a series of graphs and the restriction becomes 
annoying (and I can't see the value other than nannying)

bones should enable but not enforce, easy things should be simple and difficult things possible

tooling cannot enforce good coding, so should excel at what it does well






we only have four pairs of opening and closing symbols on the keyboard - (), {}, [], <> we need to use them wisely

() is for parentheses - a given
<> is nice for type but < and > are useful alone so open with <: and close with >
{} is nice for functions - also have {[...]...} for functions with arguments
[] is good for blocks so use for deferred lists

borrow ([...]...) from q/kdb for literal tables

. is good for named access (where the name fits {a-z, A-Z, 1-0, _})

person.name

fred.1 works for ordinal access

will use [] also for variable access

people[1][`name] same as people.1.name







