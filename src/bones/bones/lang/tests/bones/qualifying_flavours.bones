

a: {x}         // unary (1 arg)
a: {x + y}     // unary (2 args)
a: {(x,y,z)}   // unary (3 args)
b: {{x + y}}   // binary
c: {x + y + z} <:ternary>
d: {} <:nullary>
e: {x} <:rau>



OVERLOADS

addOne: {x + 1}             // polymorphic
addOne: {x ~ y}             // polymorphic on ~ operator
addOne: {[x:num] x + 1}     // takes explicit num arg, inferred to return <:num>
addOne: {x ~ " ONE"}        // polymorphic on ~ and literal ""   <:utf8>, <:ascii>, <:pystr>

a: 1 to <:ascii>

from std uses array, string, table

array.join
string.join
table.join


name type error

a: {x + y}
a: {{x + y}}

literal integers, decimals and strings are mildly polymorphic - types can be inferred from the type check but
default to ascii, index and num
