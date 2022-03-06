// first off we have a comment - the common double slash
/*
   we can also do block comments which
   can span multiple lines like this
*/

// we tell the kernel that we want to use functions defined in various libraries
from coppertop.std use *   // "*" here means that every function in coppertop.std is made available for our use

// we can also tell the kernel to include other libraries - this doens't make names available just adds functionality
// to names we have said we want to use
requires dm.stats.core


// let's define a binary function (remember "binary" means it takes in two arguments from the pipeline not that it
// can only take two arguments)
add: {{[x:u8, y:u8] <:u8> x + y}}

1 add 2 check equals 3

(1,2,3) both add (1,2,3) check equals (2,4,6)

// expressions can span multiple lines if subsequent lines after the phrase's start are indented
(1,2,3)
    both add (1,2,3)
    check equals (2,4,6)

// we can also separate phrases with a full stop
b: (1,2,3). b
    each both (1,2,3)
    check equals (2,4,6)

// btw the b: means bind the following to the name b. :c means bind the preceding to the name c.
d + c * x + b * (x * x :x2) + a * x * x2 :y

// take care, although it can help make code denser and is easier to follow than using =, style and good taste
// should prevail

