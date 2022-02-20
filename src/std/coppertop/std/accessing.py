# **********************************************************************************************************************
#
#                             Copyright (c) 2017-2021 David Briant. All rights reserved.
#
# This file is part of bones.
#
# bones is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# bones is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License along with Foobar. If not, see
# <https://www.gnu.org/licenses/>.
#
# **********************************************************************************************************************

import sys
if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)


import builtins

from coppertop.pipe import *
from coppertop.core import *
from coppertop.std.structs import tvstruct, tvarray, tvseq
from bones.core.types import T, T1, T2, T3, pylist, tv, pyint, pystr, count as tCount, \
    index, offset, pytuple, pydict, N, pydict_keys, pydict_items, pydict_values, pyfunc, pyset

from coppertop.std.types import adhoc, agg

dict_keys = type({}.keys())
dict_values = type({}.values())


# **********************************************************************************************************************
# append
# **********************************************************************************************************************

@coppertop(style=binary2)
def append(xs:pylist, x) -> pylist:
    return xs + [x]

@coppertop(style=binary2)
def append(xs:(N**T1)[tvseq], x:T1) -> (N**T1)[tvseq]:
    xs = tvseq(xs)
    xs.append(x)
    return xs


# **********************************************************************************************************************
# at
# **********************************************************************************************************************

@coppertop
def at(xs, accesor):
    return xs[accesor]

@coppertop
def at(xs:tvseq+pylist+pytuple, o:offset):
    return xs[o]

@coppertop
def at(xs:tvseq[N**T1], o:offset, tByT) -> T1:
    x = xs[o]
    if hasattr(x, '_t'):
        return x
    else:
        return tv(tByT[T1], x)

@coppertop
def at(xs:tvseq+pylist+pytuple, i:index):
    return xs[i - 1]

@coppertop
def at(xs:tvseq[N**T1], i:index, tByT) -> T1:
    x = xs[i-1]
    if hasattr(x, '_t'):
        return x
    else:
        return tv(tByT[T1], x)

@coppertop
def at(s:tvstruct+pydict+adhoc, k:pystr):
    return s[k]

@coppertop
def at(xs:pylist+pytuple, os:pylist):
    answer = []
    for o in os:
        answer.append(xs[o])
    return answer

@coppertop
def at(xs:pylist, s1:pyint, s2: pyint):
    return xs[s1:s2]

@coppertop
def at(a:(N**T)[agg], o:offset):  # -> T:
    # answers a struct if o is an offset or an array if o is a name
    raise NotYetImplemented('(agg, offset) -> T')

@coppertop
def at(a:agg, f:pystr) -> tvarray:
    return a[f]

@coppertop
def at(a:(N**T1)[agg], f:pystr) -> (N**T2)[tvarray]:
    # T2 is a column in  the struct T1
    return a[f]


# **********************************************************************************************************************
# atIfNone
# **********************************************************************************************************************

# **********************************************************************************************************************
# atIfNonePut
# **********************************************************************************************************************

# **********************************************************************************************************************
# atInsert
# **********************************************************************************************************************

# **********************************************************************************************************************
# atInsertAll
# **********************************************************************************************************************


# **********************************************************************************************************************
# atPut
# **********************************************************************************************************************


@coppertop
def atPut(m:pydict, k:T1, v:T2) -> pydict:
    m[k] = v
    return m

@coppertop
def atPut(m:(T2**T1)[tvstruct][T3], ks:(N**T1)[pylist], v:T2) -> (T2**T1)[tvstruct][T3]:
    for k in ks._v:
        m[k] = v
    return m

@coppertop
def atPut(m:(T2**T1)[tvstruct][T3], k:T1, v:T2) -> (T2**T1)[tvstruct][T3]:
    m[k] = v
    return m

@coppertop
def atPut(m:adhoc, k, v) -> adhoc:
    m[k] = v
    return m

@coppertop
def atPut(xs:pylist, iOrIs, yOrYs) -> pylist:
    # immutable??
    # xs = list(xs)
    if isinstance(iOrIs, (list, tuple)):
        for fromI, toI in enumerate(iOrIs):
            xs[toI] = yOrYs[fromI]
    else:
        xs[iOrIs] = yOrYs
    return xs

@coppertop
def atPut(a:agg, o:pyint, col:tvstruct) -> agg:
    # o may be an offset or name, e may be a tvstruct or an array
    raise NotYetImplemented()

@coppertop
def atPut(a:agg, f:pystr, col:tvarray) -> agg:
    # o may be an offset or name, e may be a tvstruct or an array
    a[f] = col
    return a


# **********************************************************************************************************************
# count
# **********************************************************************************************************************

@coppertop(style=unary1)
def count(x:tvstruct) -> tCount:
    return len(x._names())

@coppertop(style=unary1)
def count(x) -> tCount:
    return len(x)

@coppertop(style=unary1)
def count(x:pystr+pylist+pytuple+pyset+pydict_keys+pydict_values) -> tCount:
    return len(x)


# **********************************************************************************************************************
# drop
# **********************************************************************************************************************

# @coppertop(style=binary2)
# def drop(xs:(T2**T1)[pylist], ks:(T2**T1)[pylist]) -> (T2**T1)[pylist]:
#     answer = []
#     for x in xs:
#         if x not in ks:
#             answer.append(x)
#     return answer

@coppertop(style=binary2)
def drop(xs:(N**T)[pylist], ks:(N**T)[pylist]) -> (N**T)[pylist]:
    raise ProgrammerError("Don't need to box pylist now we have tvseq")
    # answer = []
    # for x in xs._v:
    #     if x not in ks._v:
    #         answer.append(x)
    # return tv(xs._t, answer)

# (N**T1)[tvseq]
@coppertop(style=binary2)
def drop(xs:(N**T1)[tvseq], indexes:pylist+pytuple, tByT) -> (N**T1)[tvseq]:
    answer = tvseq((N**tByT[T1])[tvseq])
    for i, x in enumerate(xs._v):
        if i not in indexes:
            answer.append(x)
    return answer

@coppertop(style=binary2)
def drop(xs:(N**T1)[tvseq], element:T1, tByT) -> (N**T1)[tvseq]:
    answer = tvseq((N**tByT[T1])[tvseq])
    for e in xs:
        if e is not element:
            answer.append(e)
    return answer

@coppertop(style=binary2)
def drop(xs:(N**T1)[tvseq], n:tCount, tByT) -> (N**T1)[tvseq]:
    return tvseq((N**tByT[T1])[tvseq], xs[n:])



@coppertop(style=binary2)
def drop(xs:pylist+pydict_keys, ks:pylist) -> pylist:
    answer = []
    if isinstance(ks[0], str):
        for x in xs:
            if x not in ks:
                answer.append(x)
    elif isinstance(ks[0], int):
        for o, e in enumerate(xs):
            if o not in ks:
                answer.append(e)
    else:
        raise NotYetImplemented()
    return answer

@coppertop(style=binary2)
def drop(xs:pylist+pydict_keys+pydict_values, e:pystr) -> pylist:    #(T1**N, T1)-> T1**N
    answer = []
    for x in xs:
        if x != e:
            answer.append(x)
    return answer

@coppertop(style=binary2)
def drop(xs:pylist, n:tCount) -> pylist:    #(T**N(im), count)-> T**N(im)
    return xs[n:]

@coppertop(style=binary2)
def drop(xs:pystr, n:index) -> pystr:     #(T**N(utf8), count)-> T**N(utf8)
    if n > 0:
        return xs[n:]
    else:
        raise NotYetImplemented('drop(xs:pystr, n:index) -> pystr')

@coppertop(style=binary2)
def drop(xs:pylist, ss:pytuple) -> pylist:
    s1, s2 = ss
    if s1 is Ellipsis:
        if s2 is Ellipsis:
            return []
        else:
            return xs[s2:]
    else:
        if s2 is Ellipsis:
            return xs[:s1]
        else:
            raise NotYetImplemented()

@coppertop(style=binary2)
def drop(d:pydict, ks: pylist) -> pydict:
    return {k:d[k] for k in d.keys() if k not in ks}

@coppertop(style=binary2)
def drop(d:pydict, k:pystr) -> pydict:
    return {k2:d[k2] for k2 in d.keys() if k2 != k}

@coppertop(style=binary2)
def drop(s:adhoc, names:pylist) -> adhoc:
    # names may be a list[str] or list[int]
    answer = adhoc(s)
    if not names: return answer
    if type(names[0]) is str:
        del answer[names]
    elif type(names[0]) is int:
        raise NotImplementedError()
    else:
        raise TypeError(f'Unhandled type list[{str(type(names[0]))}]')
    return answer

@coppertop(style=binary2)
def drop(s:adhoc, name:pystr) -> adhoc:
    answer = adhoc(s)
    del answer[name]
    return answer

@coppertop(style=binary2)
def drop(a:agg, k:pystr) -> agg:
    raise NotYetImplemented()

@coppertop(style=binary2)
def drop(a:agg, i:pyint) -> agg:
    raise NotYetImplemented()

@coppertop(style=binary2)
def drop(a:agg, isOrKs:pylist) -> agg:
    if not isOrKs:
        return agg
    elif isinstance(isOrKs[0], str):
        raise NotYetImplemented()
    elif isinstance(isOrKs[0], int):
        raise NotYetImplemented()
    else:
        raise TypeError()

@coppertop(style=binary2)
def drop(a:agg, ss:pytuple) -> agg:
    raise NotYetImplemented()


@coppertop(style=binary2)
def dropAll(xs, ys):
    answer = []
    for x in xs:
        if x not in ys:
            answer.append(x)
    return answer


# **********************************************************************************************************************
# eachAsArgs
# **********************************************************************************************************************

@coppertop(style=binary2)
def eachAsArgs(listOfArgs, f):
    """eachAsArgs(f, listOfArgs)
    Answers [f(*args) for args in listOfArgs]"""
    return [f(*args) for args in listOfArgs]


# **********************************************************************************************************************
# names
# **********************************************************************************************************************

@coppertop
def names(x:(T1**T2)[adhoc][T3]) -> (N**T1)[pydict_keys]:
    return tv(
        (N**x._t.parent.parent.indexType)[pylist],
        x._names()
    )

@coppertop(style=unary1)
def names(s:adhoc) -> pydict_keys:
    return s._names()

@coppertop(style=unary1)
def names(s:adhoc) -> pydict_keys:
    return s._names()

@coppertop(style=unary1)
def names(a:agg) -> pydict_keys:
    return a._names()

@coppertop(style=unary1)
def names(s:(tvstruct & T1)+tvstruct) -> pydict_keys: #(N**pystr)[pydict_keys]: needs a tvdict_keys!!!
    return s._names()



# **********************************************************************************************************************
# first
# **********************************************************************************************************************

@coppertop
def first(a:agg):
    # answers first row
    raise NotYetImplemented()

@coppertop
def first(x:pylist):
    return x[0]

@coppertop
def first(xs:pydict_values+pydict_keys):
    # https://stackoverflow.com/questions/30362391/how-do-you-find-the-first-key-in-a-dictionary
    for x in xs:
        return x


# **********************************************************************************************************************
# nvs
# **********************************************************************************************************************

@coppertop(style=unary1)
def nvs(x:adhoc) -> pydict_items:
    return x._nvs()

@coppertop(style=unary1)
def nvs(x:adhoc) -> pydict_items:
    return x._nvs()

@coppertop(style=unary1)
def nvs(x:(T1**T2)[tvstruct][T]) -> pydict_items:
    return x._v._nvs()

@coppertop(style=unary1)
def nvs(x:(T1**T2)[tvstruct][T]) -> pydict_items:
    return x._v._nvs()


# **********************************************************************************************************************
# keys
# **********************************************************************************************************************

@coppertop(style=unary1)
def keys(d:pydict) -> pydict_keys:     # (T2**T1)(map) -> (T1**N)(iter)
    return d.keys()


# **********************************************************************************************************************
# kvs
# **********************************************************************************************************************

@coppertop(style=unary1)
def kvs(x:pydict) -> pydict_items:
    return x.items()


# **********************************************************************************************************************
# last
# **********************************************************************************************************************

@coppertop
def last(a:agg):
    # answers last row
    raise NotYetImplemented()

@coppertop
def last(x):
    raise NotYetImplemented()


# **********************************************************************************************************************
# subset
# **********************************************************************************************************************

@coppertop(style=binary2)
def subset(a:adhoc, f2:pyfunc) -> pytuple:
    A, B = adhoc(), adhoc()
    for k, v in a._nvs():
        if f2(k, v):
            A[k] = v
        else:
            B[k] = v
    return A, B


# **********************************************************************************************************************
# take
# **********************************************************************************************************************

@coppertop(style=binary2)
def take(xs:pylist, os:pylist) -> pylist:
    return [xs[o] for o in os]

@coppertop(style=binary2)
def take(xs:pylist, c:pyint) -> pylist:
    return xs[0:c]

@coppertop(style=binary2)
def take(xs:(N**T1)[tvseq], n:tCount, tByT) -> (N**T1)[tvseq]:
    if n == 0:
        return xs
    elif n > 0:
        return tvseq((N**tByT[T1])[tvseq], xs[:n])
    elif n < 0:
        raise NotYetImplemented()

@coppertop(style=binary2)
def take(xs:pylist, ss:pytuple) -> pylist:
    s1, s2 = ss
    if s1 is Ellipsis:
        if s2 is Ellipsis:
            return xs
        else:
            return xs[:s2]
    else:
        if s2 is Ellipsis:
            return xs[s1:]
        else:
            return xs[s1:s2]

@coppertop(style=binary2)
def take(d:pydict, ks:pylist) -> pydict:
    return {k:d[k] for k in ks}

@coppertop(style=binary2)
def take(d:pydict, k:pystr) -> pydict:
    return {k:d[k]}

@coppertop(style=binary2)
def take(a:agg, k:pystr) -> agg:
    return agg({k:a[k]})

@coppertop(style=binary2)
def take(a:agg, i:pyint) -> agg:
    raise NotYetImplemented()

@coppertop(style=binary2)
def take(a:agg, isOrKs:pylist) -> agg:
    if not isOrKs:
        return agg
    elif isinstance(isOrKs[0], str):
        return agg({k:a[k] for k in isOrKs})
    elif isinstance(isOrKs[0], int):
        raise NotYetImplemented()
    else:
        raise TypeError()

@coppertop(style=binary2)
def take(a:agg, ss:pytuple) -> agg:
    raise NotYetImplemented()


# **********************************************************************************************************************
# values
# **********************************************************************************************************************

@coppertop
def values(x:(T1**T2)[tvstruct][T3]) -> (N**T2)[pylist]:
    return tv(
        (N**x._t.parent.parent.mappedType)[pylist],
        list(x._values())
    )

@coppertop(style=unary1)
def values(x:pydict) -> pylist:
    return list(x.values())

@coppertop(style=unary1)
def values(x:adhoc) -> pylist:
    return list(x._values())

@coppertop(style=unary1)
def values(x:adhoc) -> pylist:
    return list(x._values())

@coppertop(style=unary1)
def values(a:agg) -> pylist:
    return list(a._values())


# **********************************************************************************************************************
# zip
# **********************************************************************************************************************

@coppertop(style=unary1)
def zip(x):
    return builtins.zip(*x)









@coppertop(style=binary2)
def takeUntil(iter, fn):
    items = []
    if isinstance(iter, dict):
        for k, v in iter.items():
            if fn(k, v):
                break
            else:
                items.append([k,v])
        return dict(items)
    else:
        raise NotYetImplemented()

@coppertop
def replaceAll(xs, old, new):
    assert isinstance(xs, tuple)
    return (new if x == old else x for x in xs)

@coppertop
def indexesOf(xs, x):
    answer = []
    for i, e in enumerate(xs):
        if x == e:
            answer.append(i)
    return answer


@coppertop
def fromto(x, s1, s2=None):
    return x[s1:s2]


@coppertop(style=binary2)
def intersects(a, b):
    if not isinstance(a, (list, tuple, set, dict_keys, dict_values)):
        if not isinstance(b, (list, tuple, set, dict_keys, dict_values)):
            return a == b
        else:
            return a in b
    else:
        if not isinstance(b, (list, tuple, set, dict_keys, dict_values)):
            return b in a
        else:
            for e in a:
                if e in b:
                    return True
            return False

@coppertop(style=binary2)
def subsetOf(a, b):
    if not isinstance(a, (list, set, tuple, dict_keys, dict_values)):
        if not isinstance(b, (list, set, tuple, dict_keys, dict_values)):
            # 1, 1
            return a == b
        else:
            # 1, 1+
            return a in b
    else:
        if not isinstance(b, (list, set, tuple, dict_keys, dict_values)):
            # 1+, 1
            return False
        else:
            # 1+, 1+
            for e in a:
                if e not in b:
                    return False
            return True

@coppertop
def rename(d:pydict, old, new):
    d = dict(d)
    d[new] = d.pop(old)
    return d

@coppertop
def rename(d:adhoc, old, new):
    d = adhoc(d)
    d[new] = d._pop(old)
    return d

@coppertop
def replace(d:adhoc, f:pystr, new):
    d = adhoc(d)
    d[f] = new
    return d

@coppertop
def replace(d:pydict, f:pystr, new):
    d = dict(d)
    d[f] = new
    return d

@coppertop(style=binary2)
def where(s:adhoc, bools) -> adhoc:
    assert isinstance(s, adhoc)
    answer = adhoc(s)
    for f, v in s._nvs():
        answer[f] = v[bools].view(tvarray)
    return answer

@coppertop
def wrapInList(x):
    l = list()
    l.append(x)
    return l



