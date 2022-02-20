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

import abc
from collections import UserDict
from typing import Iterable


dict_keys = type({}.keys())
dict_values = type({}.values())
tZip = type(zip([]))


class tvstruct(UserDict):
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance._t_ = cls
        return instance

    def __init__(self, *args, **kwargs):
        super().__init__()
        if len(args) == 0:
            # tvstruct(), tvstruct(**kwargs)
            if kwargs:
                super().update(kwargs)
        elif len(args) == 1:
            arg = args[0]
            if isinstance(arg, (dict, list, tuple, zip)):
                # tvstruct(dictEtc)
                super().update(arg)
            elif isinstance(arg, tvstruct):
                # tvstruct(tvmapOrSubclass)
                self._t_ = arg._t
                super().update(arg)
            else:
                # tvstruct(t)
                self._t_ = arg
                #tvstruct(t, **kwargs)
                if kwargs:
                    super().update(kwargs)
        else:
            # tvstruct(t, dictEtc)
            arg1, arg2 = args
            self._t_ = arg1
            super().update(arg2)

            if kwargs:
                raise TypeError('No kwargs allowed when 2 args are provided')

    def __dir__(self) -> Iterable[str]:
        answer = list(super().keys())
        return answer

    def _asT(self, t):
        self._t_ = t
        return self

    def __getattribute__(self, name):

        if name[0:2] == '__':
            if name == '__class__':
                return tvstruct
            raise AttributeError()

        if name[0:1] == "_":
            if name == '_asT':
                return super().__getattribute__('_asT')
            if name == '_v':
                return self

            if name == '_t':
                return super().__getattribute__('__dict__')['_t']

            data = super().__getattribute__('__dict__')['data']

            if name == '_keys':
                return data.keys
            if name == '_nvs':
                return data.items
            if name == '_values':
                return data.values
            if name == '_pop':
                return data.pop
            if name == '_update':
                return data.update
            if name == '_setdefault':
                return data.setdefault
            if name == '_get':
                return data.get
            raise AttributeError()

        # I think we can get away without doing the following
        # if name == 'items':
        #     # for pycharm :(   - pycharm knows we are a subclass of dict so is inspecting us via items
        #     # longer term we may return a BTStruct instead of struct in response to __class__
        #     return {}.items

        if name == 'items':
            return super().__getattribute__('items')

        if name == 'keys':
            return super().__getattribute__('keys')

        if name == 'data':
            return super().__getattribute__('__dict__')['data']

        try:
            return super().__getattribute__('__dict__')['data'][name]
        except KeyError:
            raise AttributeError(f"'tvstruct' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        if name == '_t':
            raise AttributeError(f"Can't set _t on tvstruct")
        if name == '_v':
            raise AttributeError(f"Can't set _v on tvstruct")
        __dict__ = super().__getattribute__('__dict__')
        if name == 'data':
            return __dict__.__setitem__(name, value)
        if name == '_t_':
            return __dict__.__setitem__('_t', value)
        return __dict__['data'].__setitem__(name, value)

    def __call__(self, **kwargs):
        __dict__ = super().__getattribute__('__dict__')
        data = __dict__['data']
        for name, value in kwargs.items():
            data.__setitem__(name, value)
        return self

    def __getitem__(self, nameOrNames):
        if isinstance(nameOrNames, (list, tuple)):
            nvs = {name: self[name] for name in nameOrNames}
            return tvstruct(nvs)
        else:
            return super().__getattribute__('__dict__')['data'].__getitem__(nameOrNames)

    def __repr__(self):
        __dict__ = super().__getattribute__('__dict__')
        data = __dict__['data']
        itemStrings = (f"{str(k)}={repr(v)}" for k, v in data.items())
        if type(self._t) is abc.ABCMeta:
            name = self._t.__name__
        else:
            name = str(self._t)
        rep = f'{name}({", ".join(itemStrings)})'
        return rep

