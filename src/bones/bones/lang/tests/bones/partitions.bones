// *********************************************************************************************************************
//
//                            Copyright (c) 2022 David Briant. All rights reserved.
//
// *********************************************************************************************************************


partitions: {{[xs:N**T1, sizes:N2**count] <:N**N2**N**T1>
    sizes sum check equal (xs count)
    xs _partitions(, xs count, sizes)
}}

_partitions: {[xs:N**T1, n:count, sizes:N2**count] <:N**N2**N**T1>
    sizes isEmpty ifTrue: [^ (())]
    xs _combRest(, n, sizes first) each {
        _partitions(b, .n - (.sizes first), .sizes drop 1) each {[row]
            .a prependTo row
        }
    } joinAll
}

_combRest: {[xs:N**T1, n:count, m:count] <:N**(N**T1)*(N**T1)>
    m = 0 ifTrue: [^ ( {(), xs} )]
    m = n ifTrue: [^ ( {xs, ()} )]
    s1, s2: xs takeDrop 1
    _combRest(s2, s2 count, m - 1) each { {.s1 join a, b} }    // #1
      join
      _combRest(s2, s2 count, m) each { {a, .s1 join b} }      // #2
}

1 upto 9 partitions (5,4) count PP
