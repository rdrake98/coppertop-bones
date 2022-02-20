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

import operator, random
import numpy as np
import scipy.stats
from coppertop.pipe import *
from coppertop.std import sort, both, zip, nvs, values, names, override, select, to
from coppertop.std.structs import tvstruct, tvarray
from coppertop.std.linalg import matrix
from coppertop.std.types import adhoc
from bones.core.metatypes import S, BTAtom
from bones.core.types import num, pystr, T, T1, T2, T3, pylist, pydict, pyint, pytuple, pyfloat

from .misc import sequence


# numsEtAl models the storage mechanism for a pmf or likelihood and the multiplication thereof pre
# normalise, i.e. the numbers may not add up to one. Additionally for compactness we wish to be able
# to add tags, e.g to label a pmf as `d6`, etc, or to a likelihood with the data such as `PDoorBIf`


# noinspection PyUnreachableCode
if False:
    numsEtAl = BTAtom.ensure('numsEtAl')  # nominal for the moment
    # notionally a union of mappings for str**str, num**str and num**num

    @coppertop
    def at(x:numsEtAl[T], k:pystr) -> pystr+num:     # remember str is weakened to pystr and float to num
        return x[k]

    @coppertop
    def at(x:numsEtAl[T], k:num) -> num:
        return x[k]


# str**str and num**str above imply a dynamic type - i.e. return type depends on key value - however
# the reality is that the programmer always knows which one is needed

# bag1994.Red -> can always be dispatched to num
# d6[1] -> can be dispatched to num
#
# but
#
# jar.tag -> should be disallowed
# jar >> at[tag] can be allowed but is ambiguouse as str weakens to pystr
# conclusion type wise we need a tag discrimination

tbTag = BTAtom.ensure('dm.tbTag')         # since we don't have a tvstr we either box or add a subclass TBD
pyany = BTAtom.ensure('pyany')             # not sure about this - ideally it would be inferred but we're not there yet


def _makePmf(*args, **kwargs):
    return _normalisedInPlace(tvstruct(*args, **kwargs))

numsEtAl = S({pyany**tbTag:pyany**tbTag, num**num:num**num, num**pystr:num**pystr})['numEtAl'].setConstructor(tvstruct)
PMF = numsEtAl['PMF'].setConstructor(_makePmf)  # pmf
L = numsEtAl['L'].setConstructor(tvstruct)      # likelihood

@coppertop(style=unary1)
def nvs(x: numsEtAl[T]) -> pylist:
    return list(x._nvs())

@coppertop(style=unary1)
def values(x: numsEtAl[T]) -> pylist:
    return list(x._values())

@coppertop(style=unary1)
def values(x: PMF) -> pylist:
    return list(x._values())

@coppertop(style=unary1)
def names(x: numsEtAl[T]) -> pylist:
    return list(x._names())


@coppertop
def to(x:pylist, t:L) -> L:
    return t(x)


_matrix = matrix & tvarray



@coppertop(style=unary1)
def normalise(pmf:numsEtAl+L+adhoc) -> PMF:
    # immutable, asssumes non-numeric values are tags and all numeric values are part of pmf
    return _normalisedInPlace(adhoc(pmf)) | PMF

@coppertop(style=unary1)
def normalise(pmf:pydict) -> PMF:
    # immutable, asssumes non-numeric values are tags and all numeric values are part of pmf
    return _normalisedInPlace(adhoc(pmf)) | PMF

@coppertop(style=unary1)
def normalise(pmf:(T2**T1)[adhoc][T3]) -> (T2**T1)[adhoc][T3]:
    # immutable, asssumes non-numeric values are tags and all numeric values are part of pmf
    return _normalisedInPlace(adhoc(pmf))

def _normalisedInPlace(pmf:adhoc) -> adhoc:
    total = 0
    for k, v in pmf._nvs():
        if isinstance(v, (float, int)):
            total += v
    factor = 1 / total
    for k, v in pmf._nvs():
        if isinstance(v, (float, int)):
            pmf[k] = v * factor
    return pmf


@coppertop(style=unary1)
def uniform(nOrXs:pylist) -> PMF:
    '''Makes a uniform PMF. xs can be sequence of values or [length]'''
    # if a single int it is a count else there must be many xs
    answer = adhoc() | PMF
    if len(nOrXs) == 1:
        if isinstance(nOrXs[0], int):
            n = nOrXs[0]
            p = 1.0 / n
            for x in sequence(0, n-1):
                answer[float(x)] = p
            return answer
    p = 1.0 / len(nOrXs)
    for x in nOrXs:
        answer[float(x)] = p
    return answer


@coppertop(style=unary1)
def mix(args:pylist) -> PMF:
    """answer a mixture pmf, each arg is (beta, pmf) or pmf"""
    t = {}
    for arg in args:
        beta, pmf = arg if isinstance(arg, (tuple, list)) else (1.0, arg)
        for x, p in pmf._nvs():
            t[x] = t.setdefault(x, 0) + beta * p
    return t >> sort >> normalise


@coppertop(style=unary1)
def mean(pmf:PMF) -> num:
    fs = pmf >> names
    ws = pmf >> values
    try:
        return np.average(fs, weights=ws) >> to(_,pyfloat)
    except TypeError:
        fs, ws = list([fs, ws] >> zip) >> select >> (lambda fv: not isinstance(fv[0], str)) >> zip
        return np.average(fs, weights=ws) >> to(_,pyfloat)
    # if pmf:
    #     answer = 0
    #     for x, p in pmf >> nvs:
    #         answer += x * p
    #     return answer
    # else:
    #     return np.nan


@coppertop
def gaussian_kde(data) -> scipy.stats.kde.gaussian_kde:
    return scipy.stats.gaussian_kde(data)

@coppertop
def to(xs:pylist, t:PMF, kde:scipy.stats.kde.gaussian_kde) -> adhoc:
    answer = adhoc()
    answer._kde = kde
    for x in xs:
        answer[x] = kde.evaluate(x)[0]
    return answer >> normalise

@coppertop
def toCmf(pmf:PMF+adhoc):
    running = 0.0
    answer = adhoc()
    answer2 = adhoc()
    for k, v in pmf._nvs():
        if isinstance(v, float):
            running += v
            answer[k] = running
        else:
            answer2[k] = v
    cmf = np.array(list(answer._nvs()))
#    cmf[:, 1] = np.cumsum(cmf[:, 1])
    answer = answer >> override >> answer2
    answer['_cmf'] = cmf
    return answer

@coppertop(style=binary2)
def sample(cmf:adhoc, n:pyint) -> _matrix:
    vals = []
    sortedCmf = cmf['_cmf']
    for _ in range(n):
        p = random.random()
        i = np.searchsorted(sortedCmf[:, 1], p, side='left')
        vals.append(sortedCmf[i, 0])
    return _matrix(vals)

@coppertop(style=binary2)
def sample(kde:scipy.stats.kde.gaussian_kde, n:pyint) -> _matrix:
    return kde.resample(n).flatten()



@coppertop(style=binary2)
def pmfMul(lhs:numsEtAl[T1], rhs:numsEtAl[T2]) -> numsEtAl:
    # pmf(lhs kvs '{(x.k, x.v*(y.v)} (rhs kvs)) normalise
    return adhoc(both(
        lhs >> nvs,
        lambda fv1, fv2: (fv1[0], fv1[1] * fv2[1]),
        rhs >> nvs
    )) | numsEtAl



@coppertop(style=binary2)
def rvAdd(lhs:PMF, rhs:PMF) -> PMF:
    return _rvOp(lhs, rhs, operator.add)

@coppertop(style=binary2)
def rvSub(lhs:PMF, rhs:PMF) -> PMF:
    return _rvOp(lhs, rhs, operator.sub)

@coppertop(style=binary2)
def rvMul(lhs:PMF, rhs:PMF) -> PMF:
    return _rvOp(lhs, rhs, operator.mul)

@coppertop(style=binary2)
def rvDiv(lhs:PMF, rhs:PMF) -> PMF:
    return _rvOp(lhs, rhs, operator.truediv)

@coppertop(style=binary2)
def rvMax(lhs:PMF, rhs:PMF) -> PMF:
    return _rvOp(lhs, rhs, max)

def _rvOp(lhs, rhs, op):
    xps = {}
    for x1, p1 in lhs._nvs():
        for x2, p2 in rhs._nvs():
            x = op(x1, x2)
            xps[x] = xps.setdefault(x, 0.0) + p1 * p2
    return _normalisedInPlace(adhoc(
        sorted(
            xps.items(),
            key=lambda xp: xp[0]
        )
    )) | PMF


@coppertop(style=unary1)
def toXsPs(pmf:PMF) -> pytuple:
    return tuple(zip(pmf._nvs()))


