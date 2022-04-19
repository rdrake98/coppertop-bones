Bones design

reduce the amount to IT things one has to be fluent in so that brain space can be devoted to business problems instead

transactions are very important and quite hard - ensuring atomic meaningful changes to a dataset reuires a non-trivial 
amount of energy.

On the other hand analytics is hard in a different way and can be usefully done without transactions. We can reasonably
make either-or, all-or-nothing decisions either the data is there or we can abandon the analysis.

Business people probably don't need to program transactions, nor do complex UI. E.g. the kdb style of events


so our categories are:

buffered - result right now
on demand - ranges, iterators etc - have to be aware of recalculation and caching policy
    - some things don't need calculating so we can save effort there
    - buffer allocation is expensive and can add up
reactive - UI, CEP, systems


use a single threaded non-shared memory agent model like kdb (&erlang) but we could do in same process - comms is
via messages

transactional - updates require effort - acid, distribution, coordination etc
non-transactional - 



on a shoestring budget bootstrap a serious analytical language - is this julia?

performance is a concern - no matter how fast I can do something I've always then wanted to be able to add an outer 
loop and thus far the outer loop has been manual



IMPOSITION OF GOOD PRACTICE - NANNYING

there is a certain amount of learning anyone will need to do to solve problems in bones - we wish to minimise this
whilst acknowledging it is not removable

scalability and layering help here - the CEO has a point and click / email reports, the quant writes lego bricks like
partition, the systems guy makes the container / sandbox work with the outside world

we are a little bit prescriptive - providing structure so larger solutions can be reached as the expense of a little 
clunkiness / constraining to start with
    - variable scoping (explicit access for accessing parent, contextual and global scope)
    - no mutation of values -> DAG only no cycles

When we do we explain good practice



GOOD PRACTICE

maximum readability at the call site - referential integrity

named arguments - allow hints (with warnings) but enforce order so the server is not constrained - argument names 
should be private, argument order is the public interface

easy access to other scopes is prevented - 

culture - the atoms in the common library are a vital part of the culture










