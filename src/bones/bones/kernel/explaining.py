# **********************************************************************************************************************
#
#                             Copyright (c) 2019-2021 David Briant. All rights reserved.
#
# This file is part of coppertop-bones.
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


# for the moment we'll hand-code src to descriptions - over time I think this will expand
# the purpose is to make bones accessible to people as opposed to programmers

# locationId = randomly assigned u32? reserve a range for bones?


import inspect
from coppertop.core import Missing

classType = type(object)

class ErrSite(object):
    def __init__(self, *args):
        frame = inspect.currentframe()
        if frame.f_code.co_name == '__init__':
            frame = frame.f_back
        self._moduleName = frame.f_globals.get('__name__', Missing)
        self._packageName = frame.f_globals.get('__package__', Missing)
        self._fnName = frame.f_code.co_name
        self._className = Missing
        self._label = Missing

        if len(args) == 0:
            pass
        elif len(args) == 1:
            # id or class
            if isinstance(args[0], classType):
                self._className = args[0].__name__
            else:
                self._label = args[0]
        elif len(args) == 2:
            # class, id
            if isinstance(args[0], classType):
                self._className = args[0].__name__
                self._label = args[1]
            elif isinstance(args[1], classType):
                self._label = args[0]
                self._className = args[1].__name__
        else:
            raise TypeError('too many args')

    @property
    def id(self):
        return (self._moduleName, self._className, self._fnName, self._label)

    def __repr__(self):
        return f'{self._moduleName}{"" if self._className is Missing else f".{self._className}"}>>{self._fnName}' + \
               f'{"" if self._label is Missing else f"[{self._label}]"}'



docsByErrId = {
    ('bones.lang.group', 'DefParamsGroup', '_finishPhrase', 'no args') : '...',
    ('bones.lang.group', 'DefParamsGroup', '_finishPhrase', 'Param must be a name') : '...',
    ('bones.lang.group', 'RequiresGroup', '_finalise', 'requires - no items specified') : '...',
    ('bones.lang.group', 'RequiresGroup', '_finalise', 'requires - missing items after last comma') : '...',

}


