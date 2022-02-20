## coppertop standard library

The idea is two fold - to provide an efficient strongly typed ready set of functions to use, and provide names and 
operations that encourage a certain style of programming.

start off with everything aliased - do we need a deep copy for DAG ?

x: <:[(field+(N**field))**(str+int+pmf))[dag]>()
y: {}
y: y at: `a put: x
y: y at: `b put: (y at: `a)
y: y deepAt: `a`b put: cycles throw a runtime error

can lazy create or not




at, atPut, append - single element   N**T, T, singleAccessor
join, joinAll, interleave, drop, take, slice, takeAll, dropAll  N**T, manyAccessor -> N**T

depth versions

accessor access
count
fields / keys

sequencial access
first, list, front, back


ranges / iterators
kvs
each
enumerate

withIE
withKV
withVV
withVs


reduction
select

multi zoperation
zip




### AGGREGATION PROTOCOLS

applicable structs - list, dict, set, agg (soa), ndarray, ascii, utf8 \
categories - accessing elements, combining aggregations, complex, converting, dividing, generating, reordering, 
searching, transforming


#### ACCESSING ELEMENTS

append
at
atIfNone
atIfNonePut
atInsert
atPut
count
deepAt
deepAtPut
drop
dropBackUntil
dropBackWhile
dropUntil
dropWhile
fields
first
fvs
keys
kvs
last
rename
take
takeBackUntil
takeBackWhile
takeUntil
takeWhile
values


#### COMBINING AGGREGATIONS

atInsertAll
atJoin      (aka atSplice)
join        (splice, spliceAll, ideally + or ~)
override
underride
merge
zip
enlist      (wrapInList)
lj
rj
ij
oj
uj
aj
replace     (aka atAllPut)
replaceFirst


#### COMPLEX

complex higher order function, e.g.  similar to qsql - this is a compound style (i.e. for example more than a 
simple at put) as it involves indicators (including simple predicates) and generators (e.g. c = fn(a,b))

select      (similar to take)
delete      (similar to drop)
update      (similar to atPut)


#### CONVERTING

fromCsv     (from?)
fromJson    (or to(,json), to(_,csv))  
to


#### DIVIDING

split       (splitBy)
separate    (divide, diviUp, splitInto, divideInto, subset)
chunkBy
chunkWith   (chunkUsing?)
where       (select? filter? pick?)
groupBy


#### GENERATING

sequence
til


#### REORDERING

sort
sortBy
sortUsing   (sortWith)
sortRev     (or sortDown)
rev
shuffle


#### SEARCHING

endsWith
has         (contains)
indexesOf
intersects
replaceAll  (search by value and replace)
startsWith
subsetOf


#### TRANSFORMING

simple and compound higher order functions

both
each
eachi
eachkv
inject

<br>


### OTHER PROTOCOLS

#### TEXT

format
strip

#### testing

check
equal
different
sameFields
sameLen
smaeShape


#### linalg

matrix / tensor etc



