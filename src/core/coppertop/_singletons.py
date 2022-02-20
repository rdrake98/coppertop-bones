# **********************************************************************************************************************
#
#                             Copyright (c) 2011-2022 David Briant. All rights reserved.
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

from contextlib import contextmanager as _contextmanager
import copy, itertools
from ctypes import c_long

__all__ = [
    'TBC', 'Missing', 'Null', 'Err', 'Void', 'ProgrammerError', 'UnhappyWomble', 'PathNotTested', 'NotYetImplemented',
    'context', 'Scope'
]

_from_address = c_long.from_address
_numCopies = 0
_numNotCopied = 0


def _ensureSingletons():
    # These are kept on sys so their identity isn't changed on reload (a frequent
    # occurrence in Jupyter)

    # To Be Confirmed - i.e. missing for the moment
    if not hasattr(sys, '_TBC'):
        sys._TBC = Scope()
        # class Scope(object):pass
        # sys._TBC = Scope()

    # error sentinels - cf missing, null, nan in databases

    # something should / could be there but it is definitely not there
    if not hasattr(sys, '_Missing'):
        class Missing(object):
            def __bool__(self):
                return False
            def __repr__(self):
                # for pretty display in pycharm debugger
                return 'Missing'
        sys._Missing = Missing()

    # the null set
    if not hasattr(sys, '_NULL'):
        class _NULL(object):
            def __repr__(self):
                # for pretty display in pycharm debugger
                return 'Null'
        sys._NULL = _NULL()

    # general error
    if not hasattr(sys, '_ERR'):
        class _ERR(object):
            def __repr__(self):
                # for pretty display in pycharm debugger
                return 'Err'
        sys._ERR = _ERR()

    # VOID - the uninitialised variable state - in general this is
    # undetectable and has no place in code - just as part of the
    # building process
    if not hasattr(sys, '_VOID'):
        class _VOID(object):
            def __bool__(self):
                return False
            def __repr__(self):
                # for pretty display in pycharm debugger
                return 'Void'
        sys._VOID = _VOID()

    # not a - e.g. not a number, not a date, etc #NA!, #NUM!, #VALUE!
    # np.log(0)  => -inf, #np.log(-1)  => nan, tbd


    # general exceptions

    if not hasattr(sys, '_ProgrammerError'):
        class ProgrammerError(Exception): pass
        sys._ProgrammerError = ProgrammerError

    if not hasattr(sys, '_NotYetImplemented'):
        class NotYetImplemented(Exception): pass
        sys._NotYetImplemented = NotYetImplemented

    if not hasattr(sys, '_PathNotTested'):
        class PathNotTested(Exception): pass
        sys._PathNotTested = PathNotTested

    if not hasattr(sys, '_UnhappyWomble'):
        class UnhappyWomble(Exception): pass
        sys._UnhappyWomble = UnhappyWomble

    if not hasattr(sys, '_ContextStack'):
        sys._ContextStack = {}



# **********************************************************************************************************************
# context
# **********************************************************************************************************************

def context(*args, **kwargs):
    if args:
        if len(args) > 1: raise ProgrammerError(f'Can only get one context value at a time, but {args} was requested')
        # get context
        return sys._ContextStack.get(args[0], [Missing])[-1]
    else:
        return _setContext(**kwargs)

@_contextmanager
def _setContext(*args, **kwargs):
    # push context
    for k, v in kwargs.items():
        sys._ContextStack.setdefault(k, []).append(v)
    answer = None
    try:
        yield answer
    finally:
        # pop context, deleting if empty
        for k in kwargs.keys():
            sys._ContextStack[k] = sys._ContextStack[k][:-1]
            if len(sys._ContextStack[k]) == 0:
                del sys._ContextStack[k]



# **********************************************************************************************************************
# Scope - copy on write - https://stackoverflow.com/questions/628938/what-is-copy-on-write
# **********************************************************************************************************************

def _targetCount(p):
    return c_long.from_address(p._targetId).value

class _Proxy(object):
    __slots__ = ['_parentProxy', '_k', '_target', '_targetId']

    def __init__(self, parentProxy, k, target):
        super().__setattr__('_parentProxy', parentProxy)
        super().__setattr__('_k', k)
        super().__setattr__('_target', target)
        super().__setattr__('_targetId', id(target))

    def _copyIfNeeded(self, eId):
        _targetId = super().__getattribute__('_targetId')
        if eId == _targetId:
            raise ValueError('Cycle to parent detected - needs a better error message')
        parentProxy = super().__getattribute__('_parentProxy')
        if isinstance(parentProxy, _Proxy):
            parentProxy._copyIfNeeded(eId)
        if _from_address(_targetId).value > 2:  # 1 plus 1 for the proxy
            targetRefCount = _from_address(_targetId).value
            # newTarget = copy.copy(super().__getattribute__('_target'))
            super().__setattr__('_target', copy.copy(super().__getattribute__('_target')))
            newTargetId = id(super().__getattribute__('_target'))
            super().__setattr__('_targetId', newTargetId)
            newTargetRefCount = _from_address(newTargetId).value
            parentProxy._target[super().__getattribute__('_k')] = super().__getattribute__('_target')
            newTargetRefCount2 = _from_address(newTargetId).value
            global _numCopies
            _numCopies += 1
        else:
            global _numNotCopied
            _numNotCopied += 1

    def __delitem__(self, k):  # del _.fred[1]    k = 1, target is the indexable fred
        super().__getattribute__('_copyIfNeeded')(0)
        del super().__getattribute__('_target')[k]

    def __getitem__(self, k):  # _.fred[1]      k = 1, target is the indexable fred
        _target = super().__getattribute__('_target')
        # answer a new proxy every time (rather than answering an already created proxy) so ref count keeps going up
        # if the caller holds on to it just like a normal python object
        return _Proxy(self, k, _target[k])

    def __iter__(self):
        return super().__getattribute__('_target').__iter__()

    def __next__(self):
        return super().__getattribute__('_target').__next__()

    def __setitem__(self, k, newTarget):  # _.fred[1] = x      k = 1, target is the indexable fred
        newTarget = newTarget._target if isinstance(newTarget, _Proxy) else newTarget
        super().__getattribute__('_copyIfNeeded')(id(newTarget))
        super().__getattribute__('_target')[k] = newTarget   # target has not changed just the element the target contains

    def __getattribute__(self, k):
        if context('print'):
            print(k)
        if k in ('_target', '_copyIfNeeded', '_targetId', '_parentProxy', '__len__', '_nRefs', '_setAttr', '_setItem'):
            return super().__getattribute__(k)
        elif k == '_t':
            return super().__getattribute__('_target')._t
        else:
            # _target = super().__getattribute__('_target')
            if isinstance(super().__getattribute__('_target'), list):
                if k in ('clear', 'extend', 'pop', 'remove', 'insert', 'reverse'):
                    raise ProgrammerError(f'list>>{k} is disabled for Scope')
                elif k in ('append', 'sort'):
                    # _target = None
                    super().__getattribute__('_copyIfNeeded')(0)        # could append a parent!!! TODO fix
                    # if a copy was needed then _target has changed so get it again
                    return getattr(super().__getattribute__('_target'), k)
                else:
                    # __contains__, __iter__, __add__, __mul__, __reversed__, copy, count, index
                    return super().__getattribute__('_target').__getattribute__(k)
            if isinstance(super().__getattribute__('_target'), dict):
                if k in ('clear', 'pop', 'popitem', 'update'):
                    raise ProgrammerError(f'dict>>{k} is disabled for Scope')
                elif k in ('setdefault'):
                    raise NotYetImplemented()
                    # _target = None
                    super().__getattribute__('_copyIfNeeded')(0)  # could append a parent!!! TODO fix
                    # if a copy was needed then _target has changed so get it again
                    return getattr(super().__getattribute__('_target'), k)
                else:
                    # __contains__, __iter__, __reversed__, __ror__, fromkeys, get, items, keys, values
                    return super().__getattribute__('_target').__getattribute__(k)
            return _Proxy(self, k, super().__getattribute__('_target').__getattribute__(k))

    def __setattr__(self, k, newElement):    # _.fred.name = x      _target=fred, k=name, newElement=x
        super().__getattribute__('_copyIfNeeded')(newElement._targetId if isinstance(newElement, _Proxy) else id(newElement))
        setattr(super().__getattribute__('_target'), k, newElement)  # target has not changed just the element the target contains

    def __str__(self):
        return super().__getattribute__('_target').__str__()

    def __repr__(self):
        return f"[{super().__getattribute__('_k')}]{{{super().__getattribute__('_target').__repr__()}}}"

    def __len__(self):
        return super().__getattribute__('_target').__len__()

    def __bool__(self):
        _target = super().__getattribute__('_target')
        if hasattr(_target, '__bool__'):
            return _target.__bool__()
        else:
            return _target.__len__() > 0

    def __call__(self, *args, **kwargs):
        return super().__getattribute__('_target')(*args, **kwargs)

    def __add__(self, rhs):
        return super().__getattribute__('_target') + rhs

    def __radd__(self, lhs):
        return lhs + super().__getattribute__('_target')

    def __sub__(self, rhs):
        return super().__getattribute__('_target') - rhs

    def __rsub__(self, lhs):
        return lhs - super().__getattribute__('_target')

    def __mul__(self, rhs):
        return super().__getattribute__('_target') * rhs

    def __rmul__(self, lhs):
        return lhs - super().__getattribute__('_target')

    def __truediv__(self, rhs):
        return super().__getattribute__('_target') / rhs

    # def __rdiv__(self, lhs):
    #     return lhs / super().__getattribute__('_target')

    def __rtruediv__(self, lhs):
        return lhs / super().__getattribute__('_target')

    def __iadd__(self, rhs):          # _.fred.age += rhs       _target=age, k=age
        oldTarget = super().__getattribute__('_target')
        newTarget = oldTarget + rhs
        newtargetId = id(newTarget)
        assert not isinstance(newTarget, _Proxy)  # unlikely but just in case
        # self won't need to check for copies as we have a new target, so start with parent
        _parentProxy = super().__getattribute__('_parentProxy')
        if isinstance(_parentProxy, _Proxy):
            _parentProxy._copyIfNeeded(newtargetId)
        k = super().__getattribute__('_k')
        _parentProxy._setAttr(k, newTarget)
        return newTarget        #__iadd__ must return the new value

    def __imul__(self, rhs):        # self *= rhs
        raise NotYetImplemented()

    def __eq__(self, rhs):          # self == rhs
        return super().__getattribute__('_target') == (rhs._target if isinstance(rhs, _Proxy) else rhs)

    def _nRefs(self):
        return _from_address(super().__getattribute__('_targetId')).value

    def _setAttr(self, k, v):
        setattr(super().__getattribute__('_target'), k, v)

    def _setItem(self, k, v):
        super().__getattribute__('_target')[k] = v


# to decrease any ref count object deletion must be detected thus we need to create an object on access - this is
# the cost of the optimisation in Python

class Scope(object):
    _slots__ = ['_vars']

    def __init__(self):
        super().__setattr__('_vars', {})

    def __getattribute__(self, k):      # _.fred or
        if k == '_target': # _._target
            return super().__getattribute__('_vars')
        if k in ('__class__', '__module__', '_setAttr'):
            return super().__getattribute__(k)
        _vars = super().__getattribute__('_vars')
        if k in _vars: # _.fred
            # answer a new proxy every time so ref count goes up
            return _Proxy(self, k, _vars[k])
        else:
            raise AttributeError(k)

    def __setattr__(self, k, newValue):
        if isinstance(newValue, _Proxy):
            newValue = newValue._target
        super().__getattribute__('_vars')[k] = newValue

    def __delattr__(self, k):
        vars = super().__getattribute__('_vars')
        if k in vars:
            del vars[k]
            return
        raise AttributeError(k)

    def __repr__(self):
        # for pretty display in pycharm debugger
        return f"TBC{{{','.join(super().__getattribute__('_vars'))}}}"

    def _setAttr(self, k, v):
        super().__getattribute__('_vars')[k] = v

    def __dir__(self):
        return list(super().__getattribute__('_vars').keys())



_ensureSingletons()
TBC = sys._TBC
Missing = sys._Missing
Null = sys._NULL
Err = sys._ERR
Void = sys._VOID
ProgrammerError = sys._ProgrammerError
NotYetImplemented = sys._NotYetImplemented
PathNotTested = sys._PathNotTested
UnhappyWomble = sys._UnhappyWomble


if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__ + ' - done')
