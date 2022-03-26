

For the cluedo pad I needed to figure how to populate a 2d PMF (stored as a matrix of num of cards by
num hand possibilities with each cell being the hand that the card is in). I adapted a [rosetta code
algo](https://rosettacode.org/wiki/Ordered_partitions#Python), also see [wikipedia](https://en.wikipedia.org/wiki/Permutation#Systematic_generation_of_all_permutations), thus:

```python
def partitions_(xs:N**T1, sizes:N2**count) -> N**N2**N**T1:
    sizes >> sum >> check >> equal >> (xs >> count)
    return _partitions(list(xs), xs >> count, sizes)

def _partitions(xs:N**T1, n:count, sizes:N2**count) -> N**N2**N**T1:
    if sizes:
        answer = []
        for comb, rest in _combRest(xs, n, sizes[0]):
            for partitions in _partitions(rest, n - sizes[0], sizes[1:]):
                answer.append([comb] + partitions)
        return answer
    else:
        return [[]]

def _combRest(xs:N**T1, n:count, m:count) -> N**( (N**T1)*(N**T1) ):
    '''answer [m items chosen from n items, the rest]'''
    if m == 0:
        return [([], xs)]
    elif m == n:
        return [(xs, [])]
    else:
        firstPart = [ (xs[0:1] + x, y) for x, y in _combRest(xs[1:], n - 1, m - 1)] 
        secondPart = [ (x, xs[0:1] + y) for x, y in _combRest(xs[1:], n - 1, m)]
        return firstPart + secondPart
```

```python
partitions(range(13), [5,4,4]) >> count >> PP
```

Answers 90090 as expected, but isn't fully typed (in python it's just ugly). Here's the coppertop-bones version.

```python
@coppertop(style=binary)
#def partitions_(es:N**T, sizes:N**pyint) -> N**N**N**T:
def partitions2_(es, sizes:pylist):
    sizes >> sum >> check >> equal >> (es >> count)
    return list(es) >> _partitions2(_, es >> count, sizes)


@coppertop
#def _partitions2(es:N**T, n:pyint, sizes:N**pyint) -> N**N**(N**T):
def _partitions2(es:pylist, n:pyint, sizes:pylist) -> pylist:
    if not sizes: return [[]]
    return es >> _combRest2(_, n, sizes >> first) \
        >> each >> unpack(lambda x, y: 
            y >> _partitions2(_, n - (sizes >> first), sizes >> drop >> 1) 
                >> each >> (lambda partitions:
                    x >> prependTo >> partitions
                )
        )  \
        >> joinAll
        

@coppertop
#def _combRest2(es:N**T, n:pyint, m:pyint) -> N**( (N**T)*(N**T) ):
def _combRest2(es:pylist, n:pyint, m:pyint) -> pylist:
    '''answer [m items chosen from n items, the rest]'''
    if m == 0: return [([], es)]
    if m == n: return [(es, [])]
    return \
        es >> drop >> 1 >> _combRest2(_, n - 1, m - 1) >> each >> unpack(lambda x, y: (es >> take >> 1 >> join >> x, y)) \
        >> join >> (
        es >> drop >> 1 >> _combRest2(_, n - 1, m) >> each >> unpack(lambda x, y: (x, es >> take >> 1 >> join >> y))
        )

    
range(9) >> partitions2_ >> [5,4] >> count >> PP
```

which answers 126 as expected.


The bones equivalent is something like:

```
// bones version

partitions: {{[es:N**T1, sizes:N2**count] <:N**N2**N**T1>
    sizes sum check equal (es count)
    es _partitions(, es count, sizes)
}}

_partitions: {[es:N**T1, n:count, sizes:N2**count] <:N**N2**N**T1>
    sizes isEmpty ifTrue: [^ (())]
    es _combRest(, n, sizes first) each {
        y _partitions(, .n - (.sizes first), .sizes drop 1) each {[partitions] 
            .x prependTo partitions
        }
    } joinAll
}

_combRest: {[es:N**T1, n:count, m:count] <:N**(N**T1)*(N**T1)>
    m == 0 ifTrue: [^ ( {(), es} )]
    m == n ifTrue: [^ ( {es, ()} )]
    es drop 1 _combRest(, n - 1, m - 1) each { {.es take 1 join x, y} }   
      join  (
    es drop 1 _combRest(, n - 1, m) each { {x, .es take 1 join y} }
    )
}

1 upto 9 partitions (5,4) count PP
```

This would be a hard yet good first target to aim for as it tests much of the language.

Currently `join` and `joinAll` allocate, but given that we know the required size upfront we only 
need to allocate once and can use the context to do non-aliased “immutable” destructive updates and 
some JAI like optimisation.

Tasks:

* write a python version with a single alloc and in-place arrays (x slots for the cards plus y slots 
for the subarray current sizes) x num combinations
* do fully typed coppertop-bones version (remove list comprehensions and for loops) (add logging)
* translate to bones
* group and parse the above code creating tdd tests as required to guide development with python std
  such that the resulting AST can produce the same output - may need to rely on python dynamic typing 
  and later on add type inference
  * need to finalise literal tuple syntax (e.g. `{x, .xs take 1 join y}` above)
  * need to finalise escape syntax (e.g. `^ (())` above)
  * distinguish between calling a fn and passing it a literal list
  