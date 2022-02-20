// first off we have a comment - the common double slash
/* we can also do block comments */

// to do anything use we need to add libraries to the kernel - we use the `include` statement to do that and the
// import statemet to add names from other modules into this one  - the usual basic operators are included by
// default


include coppertop.std

from coppertop.std import each, PP, both, check, equal

// let's define a binary function
add: {{[x:u8, y:u8] <:u8>.  x + y}}

1 add 2 check equal 3

(1,2,3) each both (1,2,3) check equal (2,4,6)




