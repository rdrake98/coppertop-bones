# **********************************************************************************************************************
#
#                             Copyright (c) 2021-2022 David Briant. All rights reserved.
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

from bones.core.metatypes import BTAtom as _BTAtom, BType as _BType, weaken as _weaken
_Void = sys._VOID
_ProgrammerError = sys._ProgrammerError
_Missing = sys._Missing

__all__ = []

i8 = _BTAtom.define('i8').setExclusive
u8 = _BTAtom.define('u8').setExclusive
i16 = _BTAtom.define('i16').setExclusive
u16 = _BTAtom.define('u16').setExclusive
i32 = _BTAtom.define('i32').setExclusive
u32 = _BTAtom.define('u32').setExclusive
i64 = _BTAtom.define('i64').setExclusive
u64 = _BTAtom.define('u64').setExclusive
f32 = _BTAtom.define('f32').setExclusive
f64 = _BTAtom.define('f64').setExclusive

__all__ += [
    'T',
    'i8', 'u8', 'i16', 'u16', 'i32', 'u32', 'i64', 'u64', 'f32', 'f64',
]


T = _BType('T')
for i in range(1, 21):
    t = T.ensure(_BType(f'{i}'))
    locals()[t.name] = t
for o in range(26):
    t = T.ensure(_BType(chr(ord('a')+o)))
    locals()[t.name] = t

__all__ += [
    'T',
    'T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9', 'T10',
    'T11', 'T12', 'T13', 'T14', 'T15', 'T16', 'T17', 'T18', 'T19', 'T20',
    'Ta', 'Tb', 'Tc', 'Td', 'Te', 'Tf', 'Tg', 'Th', 'Ti', 'Tj', 'Tk', 'Tl', 'Tm',
    'Tn', 'To', 'Tp', 'Tq', 'Tr', 'Ts', 'Tt', 'Tu', 'Tv', 'Tw', 'Tx', 'Ty', 'Tz'
]


N = _BType('N')
for i in range(1, 11):
    t = N.ensure(_BType(f'{i}'))
    locals()[t.name] = t
for o in range(26):
    t = N.ensure(_BType(chr(ord('a')+o)))
    locals()[t.name] = t

__all__ += [
    'N',
    'N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'N7', 'N8', 'N9', 'N10',
    'Na', 'Nb', 'Nc', 'Nd', 'Ne', 'Nf', 'Ng', 'Nh', 'Ni', 'Nj', 'Nk', 'Nl', 'Nm',
    'Nn', 'No', 'Np', 'Nq', 'Nr', 'Ns', 'Nt', 'Nu', 'Nv', 'Nw', 'Nx', 'Ny', 'Nz'
]


class tv(object):
    __slots__ = ['_t_', '_v_', '_hash']
    def __init__(self, _t, _v):
        assert isinstance(_t, (_BType, type))
        self._t_ = _t
        self._v_ = _v
        self._hash = _Missing
    def __setattr__(self, key, value):
        if key in ('_t_', '_v_', '_hash'):
            tv.__dict__[key].__set__(self, value)
        else:
            raise AttributeError()
    @property
    def _t(self):
        return self._t_
    @property
    def _v(self):
        return self._v_
    @property
    def _tv(self):
        return (self._t_, self._v_)
    def _asT(self, _t):
        return tv(_t, self._v)
    def __repr__(self):
        return f'tv({self._t_},{self._v_})'
    def __str__(self):
        return f'<{self._t_}:{self._v_}>'
    def __eq__(self, other):
        if not isinstance(other, tv):
            return False
        else:
            return (self._t_ == other._t_) and (self._v_ == other._v_)
    def __hash__(self):
        # tv will be hashable if it's type and value are hashable
        if self._hash is _Missing:
            self._hash = hash((self._t, self._v))
        return self._hash


class BIndex(int):
    # tv representing indices (1 based)
    def __new__(cls, t, v, *args, **kwargs):
        return super(cls, cls).__new__(cls, v)
    @property
    def _v(self):
        return self #super().__new__(int, self)
    @property
    def _t(self):
        return index
    def __repr__(self):
        return f'i{super().__repr__()}'

index = i64['index'].setCoercer(BIndex)
for o in range(26):
    locals()['I'+chr(ord('a')+o)] = index
__all__ += [
    'Ia', 'Ib', 'Ic', 'Id', 'Ie', 'If', 'Ig', 'Ih', 'Ii', 'Ij', 'Ik', 'Il', 'Im',
    'In', 'Io', 'Ip', 'Iq', 'Ir', 'Is', 'It', 'Iu', 'Iv', 'Iw', 'Ix', 'Iy', 'Iz'
]



class BOffset(int):
    # tv representing offsets (0 based)
    def __new__(cls, t, v, *args, **kwargs):
        return super(cls, cls).__new__(cls, v)
    @property
    def _t(self):
        return offset
    def _v(self):
        return self
    def __repr__(self):
        return f'o{super().__repr__()}'

offset = i64['offset'].setCoercer(BOffset)
for o in range(26):
    locals()['O'+chr(ord('a')+o)] = offset
__all__ += [
    'Oa', 'Ob', 'Oc', 'Od', 'Oe', 'Of', 'Og', 'Oh', 'Oi', 'Oj', 'Ok', 'Ol', 'Om',
    'On', 'Oo', 'Op', 'Oq', 'Or', 'Os', 'Ot', 'Ou', 'Ov', 'Ow', 'Ox', 'Oy', 'Oz'
]



class BCount(int):
    # tv representing counts, natural numbers starting at 0
    def __new__(cls, t, v, *args, **kwargs):
        return super(cls, cls).__new__(cls, v)
    def __add__(self, other):
        return NotImplemented
    def __sub__(self, other):
        return NotImplemented
    def __mul__(self, other):
        return NotImplemented
    def __div__(self, other):
        return NotImplemented
    @property
    def _t(self):
        return count
    @property
    def _v(self):
        return self
    def __repr__(self):
        return f'c{super().__repr__()}'

count = i64['count'].setCoercer(BCount)
__all__ += ['count']


class tvfloat(float):
    # tv representing 64 bit float point numbers
    def __new__(cls, t, v, *args, **kwargs):
        instance = super(cls, cls).__new__(cls, v)
        instance._t_ = t
        return instance
    @property
    def _v(self):
        return super().__new__(float, self)
    @property
    def _t(self):
        return self._t_
    def __repr__(self):
        return f'{self._t}{super().__repr__()}'
    def _asT(self, t):
        self._t_ = t
        return self

num = f64['num'].setCoercer(tvfloat)
__all__ += ['num']


class Holder(object):
    # a rebindable holder of a sum-type and a tv
    __slots__ = ['_st_', '_tv_']
    def __init__(self, _st, *args):
        self._st_ = _st
        self._tv_ = args[0] if len(args) == 1 else _Void
    def __setattr__(self, key, value):
        if key in ('_st_', '_tv_'):
            Holder.__dict__[key].__set__(self, value)
        elif key == '_tv':
            if not isinstance(value, self._st_): raise TypeError()
            Holder.__dict__['_tv_'].__set__(self, value)
        else:
            raise AttributeError()
    @property
    def _st(self):
        return self._st_
    @property
    def _tv(self):
        tv = self._tv_
        if tv is _Void: raise _ProgrammerError("Trying to access a value before setting it")
        return self._tv_
    def __repr__(self):
        return f'Holder({self._st_},{self._tv_})'



pystr = _BTAtom.define('pystr').setExclusive
pylist = _BTAtom.define('pylist').setExclusive
pytuple = _BTAtom.define('pytuple').setExclusive
pydict = _BTAtom.define('pydict').setExclusive
pyset = _BTAtom.define('pyset').setExclusive
pybool = _BTAtom.define('pybool').setExclusive
pyint = _BTAtom.define('pyint').setExclusive
pyfloat = _BTAtom.define('pyfloat').setExclusive
npfloat = _BTAtom.define('npfloat').setExclusive
pydatetime = _BTAtom.define('pydatetime').setExclusive
pydate = _BTAtom.define('pydate').setExclusive
pydict_keys = _BTAtom.define('pydict_keys').setExclusive
pydict_values = _BTAtom.define('pydict_values').setExclusive
pydict_items = _BTAtom.define('pydict_items').setExclusive
pyfunc = _BTAtom.define('pyfunc').setExclusive

__all__ += [
    'pystr', 'pylist', 'pytuple', 'pydict', 'pyset', 'pybool', 'pyint', 'pyfloat', 'npfloat', 'pydatetime', 'pydate',
    'pydict_keys', 'pydict_values', 'pydict_items', 'pyfunc',
]


null = _BTAtom.define('null')           # the null set - something that isn't there and that's okay
void = _BTAtom.define('void')           # something that isn't there and shouldn't be there
missing = _BTAtom.define('missing')     # something that isn't there and should be there

anon = _BTAtom.define('anon').setOrthogonal
named = _BTAtom.define('named').setOrthogonal
aliased = _BTAtom.define('aliased').setImplicit
_weaken(anon, aliased)
_weaken(named, aliased)

__all__ += [
    'null', 'void', 'missing',
]


litint = _BTAtom.define('litint').setExclusive
litdec = _BTAtom.define('litdec').setExclusive
litstring = _BTAtom.define('litstring').setExclusive
litdate = _BTAtom.define('litdate').setExclusive
litbool = _BTAtom.define('litbool').setExclusive

ascii = _BTAtom.define('ascii').setExclusive
utf8 = _BTAtom.define('utf8').setExclusive

sym = _BTAtom.define('sym').setExclusive
bool = _BTAtom.ensure("bool")
pair = _BTAtom.define('pair')

__all__ += [
    'litint', 'litdec', 'litstring', 'litdate', 'litbool',
    'ascii', 'utf8', 'sym', 'bool', 'pair',
]



# could make +, -, / and * be type aware (index, offset, count should be orthogonal as well as exclusive)


if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__ + ' - done')
