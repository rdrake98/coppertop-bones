# **********************************************************************************************************************
#
#                             Copyright (c) 2021 David Briant. All rights reserved.
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

from coppertop.core import Missing, NotYetImplemented
from typing import Iterable
import abc


class tvstruct(object):
    __slots__ = ['_pub', '_pvt']

    def __init__(self, *args, **kwargs):
        super().__init__()
        super().__setattr__('_pvt', {})
        super().__setattr__('_pub', {})
        super().__getattribute__('_pvt')['_t'] = type(self)
        super().__getattribute__('_pvt')['_v'] = self

        if len(args) == 0:
            # tvstruct(), tvstruct(**kwargs)
            if kwargs:
                super().__getattribute__('_pub').update(kwargs)
        elif len(args) == 1:
            # tvstruct(tvstruct), tvstruct(dictEtc)
            arg = args[0]
            if isinstance(arg, tvstruct):
                # tvstruct(tvstruct)
                super().__getattribute__('_pvt')['_t'] = arg._t
                super().__getattribute__('_pub').update(arg._pub)
            elif isinstance(arg, (dict, list, tuple, zip)):
                # tvstruct(dictEtc)
                super().__getattribute__('_pub').update(arg)
            else:
                # tvstruct(t), tvstruct(t, **kwargs)
                super().__getattribute__('_pvt')['_t'] = arg
                if kwargs:
                    # tvstruct(t, **kwargs)
                    super().__getattribute__('_pub').update(kwargs)
        elif len(args) == 2:
            # tvstruct(t, tvstruct), tvstruct(t, dictEtc)
            arg1, arg2 = args
            if kwargs:
                raise TypeError('No kwargs allowed when 2 args are provided')
            super().__getattribute__('_pvt')['_t'] = arg1
            if isinstance(arg2, tvstruct):
                # tvstruct(t, tvstruct)
                super().__getattribute__('_pub').update(arg2._pub)
            else:
                # tvstruct(t, dictEtc)
                super().__getattribute__('_pub').update(arg2)
        else:
            raise TypeError(
                'tvstruct(...) must be of form tvstruct(), tvstruct(**kwargs), tvstruct(tvstruct), tvstruct(dictEtc), ' +
                'tvstruct(t), tvstruct(t, **kwargs), tvstruct(t, tvstruct), tvstruct(t, dictEtc), '
            )

    def __asT__(self, t):
        super().__getattribute__('_pvt')['_t'] = t
        return self

    def __copy__(self):
        return tvstruct(self)

    def __getattribute__(self, f):
        if f[0:2] == '__':
            try:
                answer = super().__getattribute__(f)
            except AttributeError as e:
                answer = super().__getattribute__('_pvt').get(f, Missing)
            if answer is Missing:
                if f in ('__class__', '__len__', '__members__', '__getstate__'):
                    # don't change behaviour
                    raise AttributeError()
            return answer

        if f[0:1] == "_":
            if f == '_pvt': return super().__getattribute__('_pvt')
            if f == '_pub': return super().__getattribute__('_pub')
            if f == '_asT': return super().__getattribute__('__asT__')
            if f == '_t': return super().__getattribute__('_pvt')['_t']
            if f == '_v': return super().__getattribute__('_pvt')['_v']
            # if f == '_asT': return super().__getattribute__('_asT')
            if f == '_names': return super().__getattribute__('_pub').keys
            if f == '_nvs': return super().__getattribute__('_pub').items
            if f == '_values': return super().__getattribute__('_pub').values
            if f == '_update': return super().__getattribute__('_pub').update
            if f == '_get': return super().__getattribute__('_pub').get
            # if names have been added e.g. by self['_10y'] allow access as long as not double entered
            pub = super().__getattribute__('_pub').get(f, Missing)
            pvt = super().__getattribute__('_pvt').get(f, Missing)
            if pub is Missing: return pvt
            if pvt is Missing: return pub
            raise AttributeError(f'public and private entries exist for {f}')
        # print(f)
        # I think we can get away without doing the following
        # if f == 'items':
        #     # for pycharm :(   - pycharm knows we are a subclass of dict so is inspecting us via items
        #     # longer term we may return a BTStruct instead of struct in response to __class__
        #     return {}.items
        v = super().__getattribute__('_pub').get(f, Missing)
        if v is Missing:
            raise AttributeError(f'{f} is Missing')
        else:
            return v

    def __setattr__(self, f, v):
        if f[0:1] == "_":
            if f == '_t_': return super().__getattribute__('_pvt').__setitem__('_t', v)
            # if f in ('_t', '_v', '_pvt', '_pub'): raise AttributeError(f"Can't set {f} on tvstruct")
            if f in ('_pvt', '_pub'): raise AttributeError(f"Can't set {f} on tvstruct")
            return super().__getattribute__('_pvt').__setitem__(f, v)
        return super().__getattribute__('_pub').__setitem__(f, v)

    def __getitem__(self, fOrFs):
        if isinstance(fOrFs, (list, tuple)):
            nvs = {f: self[f] for f in fOrFs}
            return tvstruct(self._t, nvs)
        else:
            return super().__getattribute__('_pub').__getitem__(fOrFs)

    def __setitem__(self, f, v):
        if isinstance(f, str):
            if f[0:1] == "_":
                if f in ('_pvt', '_pub', '_names', '_nvs', '_values', '_update', '_get'):
                    raise AttributeError(f'name {f} is reserved for use by tvstruct')
                # if f in super().__getattribute__('_pvt'):
                #     raise AttributeError(f'name {f} is already in pvt use')
        super().__getattribute__('_pub').__setitem__(f, v)

    def __delitem__(self, fOrFs):
        if isinstance(fOrFs, (list, tuple)):
            for f in fOrFs:
                super().__getattribute__('_pub').__delitem__(f)
        else:
            super().__getattribute__('_pub').__delitem__(fOrFs)

    def __contains__(self, f):
        return super().__getattribute__('_pub').__contains__(f)

    def __call__(self, **kwargs):
        _pub = super().__getattribute__('_pub')
        for f, v in kwargs.items():
            _pub.__setitem__(f, v)
        return self
    
    def __dir__(self) -> Iterable[str]:
        # return super().__getattribute__('_pub').keys()
        return [k for k in super().__getattribute__('_pub').keys() if isinstance(k, str)]

    def __repr__(self):
        _pub = super().__getattribute__('_pub')
        _t = super().__getattribute__('_pvt')['_t']
        itemStrings = (f"{str(k)}={repr(v)}" for k, v in _pub.items())

        if type(_t) is abc.ABCMeta or _t is tvstruct:
            name = _t.__name__
        else:
            name = str(self._t)
        rep = f'{name}({", ".join(itemStrings)})'
        return rep

    def __len__(self):
        return len(super().__getattribute__('_pub'))

    def __eq__(self, rhs):      # self == rhs
        if isinstance(rhs, dict):
            raise NotYetImplemented()
        elif isinstance(rhs, tvstruct):
            return self._nvs() == rhs._nvs()
        else:
            return False


