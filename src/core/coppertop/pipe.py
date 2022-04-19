# **********************************************************************************************************************
#
#                             Copyright (c) 2020-2021 David Briant. All rights reserved.
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
# You should have received a copy of the GNU Affero General Public License along with coppertop-bones. If not, see
# <https://www.gnu.org/licenses/>.
#
# **********************************************************************************************************************

import sys
if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)

__all__ = [
    'coppertop', 'nullary', 'unary', 'rau', 'binary', 'ternary', 'unary1', 'binary2', '_', 'sig', 'context',
    'raiseLessPipe', 'typeOf', 'selectDispatcher', 'anon', 'MultiFn', 'Partial'
]


import inspect, types, builtins, datetime
from collections import namedtuple
from coppertop.core import ProgrammerError, NotYetImplemented, Missing, TBC, context
from coppertop._singletons import _Proxy
from bones.kernel.explaining import ErrSite
from bones.core.metatypes import BType, fitsWithin, cacheAndUpdate, BTFn, BTUnion, BTTuple
from bones.core.types import pystr, pyint, pylist, pydict, pytuple, pydate, pydatetime, pyset, pyfloat, pybool, \
    pydict_keys, pydict_items, pydict_values, pyfunc

dict_keys = type({}.keys())
dict_values = type({}.values())
dict_items = type({}.items())
function = type(lambda x:x)

_BonesTByPythonT = {
    int : pyint,
    str : pystr,
    list : pylist,
    dict : pydict,
    tuple : pytuple,
    datetime.date : pydate,
    datetime.datetime : pydatetime,
    set : pyset,
    float : pyfloat,
    bool : pybool,
    dict_keys : pydict_keys,
    dict_items : pydict_items,
    dict_values : pydict_values,
    function : pyfunc,
}

DispatcherQuery = namedtuple('DispatcherQuery', ['d', 'tByT'])

_ = TBC
NO_TYPE = inspect._empty
BETTER_ERRORS = False

_mfByFnname = {}
_sigCache = {}



# the @coppertop decorator
def coppertop(*args, style=Missing, newName=Missing, typeHelper=Missing, supressDispatcherQuery=False):

    def registerFn(fn):
        style_ = unary if style is Missing else style
        module, fnname, priorDef, definedInFunction = _fnContext(fn, 'registerFn', newName)

        # create dispatcher
        if issubclass(style_, _FasterSingleDispatcher):
             d = style_(fnname, module, fn, supressDispatcherQuery, typeHelper)
        else:
            d = _SingleDispatcher(fnname, module, style_, fn, supressDispatcherQuery, typeHelper)

        # add it to the relevant multifn
        if definedInFunction:
            # prevent update of any global multifn
            ds = [d]
            if (mf := _mfByFnname.get(fnname, Missing)) is not Missing:
                ds += [mf.dispatcher]
            if priorDef:
                ds += [priorDef.dispatcher]
            if len(ds) > 1:
                d = _MultiDispatcher(*ds)
            mf = MultiFn()
        else:
            if (mf := _mfByFnname.get(fnname, Missing)) is Missing:
                # create new multifn
                mf = MultiFn()
                _mfByFnname[fnname] = mf
            else:
                # extend the current multifn with d
                d = _MultiDispatcher(mf.dispatcher, d)
        mf.dispatcher = d
        return mf


    if len(args) == 1 and isinstance(args[0], (types.FunctionType, types.MethodType, type)):
        # of form @coppertop so args[0] is the function or class being decorated
        return registerFn(args[0])

    else:
        # of form as @coppertop() or @coppertop(overrideLHS=True) etc
        if len(args): raiseLessPipe(TypeError('Only kwargs allowed'))
        return registerFn



class MultiFn(object):
    __slots__ = ['_dispatcher']

    def __init__(mf):
        mf._dispatcher = Missing
    def __call__(mf, *args, **kwargs):
        return mf.dispatcher.__call__(*args, **kwargs)
    def __rrshift__(mf, arg):  # arg >> func
        if isinstance(arg, MultiFn): arg = arg.dispatcher
        answer = arg >> mf.dispatcher
        return answer
    def __rshift__(mf, arg):  # func >> arg
        if isinstance(arg, MultiFn): arg = arg.dispatcher
        return mf.dispatcher >> arg
    def __repr__(mf):
        return mf.dispatcher.__repr__()
    @property
    def dispatcher(mf):
        return mf._dispatcher
    @dispatcher.setter
    def dispatcher(mf, d):
        mf._dispatcher = d
    @property
    def __doc__(mf):
        return mf._dispatcher.__doc__
    @property
    def _t(mf):
        return mf.dispatcher._t


class _DispatcherBase(object):

    def __call__(d, *args, **kwargs):  # func(...)
        # if all the args are passed and not a multi dispatcher then we don't need to create a partial
        # would this be overall faster? yes as this is calculated anyway in Partial.__new__
        return d.style(d, False, args, kwargs)

    def __rrshift__(d, arg):  # arg >> func
        if d.style.numLeft == 0:
            raiseLessPipe(SyntaxError(f'arg >> {d.name} - illegal syntax for a {d.style.name}'))
        else:
            args = [TBC] * d.style.numPiped
            return d.style(d, False, args, {}).__rrshift__(arg)

    def __rshift__(d, arg):  # func >> arg
        if d.style.numLeft == 0 and d.style.numRight > 0:
            # only rau can handle this case
            args = [TBC] * d.style.numRight
            return d.style(d, False, args, {}).__rshift__(arg)
        else:
            if hasattr(arg, '__rrshift__'):
                return arg.__rrshift__(d)
            else:
                raiseLessPipe( SyntaxError(f'{d.name} >> arg - illegal syntax for a {d.style.name}'))

    def __repr__(d):
        return d.name

    def _dispatch(d, args, kwargs):
        io = dict(hasValue=False)
        argTypes = tuple(((arg if _isType(arg, io) else _typeOf(arg)) for arg in args))
        sd, tByT = d._selectDispatcher(argTypes)
        if io['hasValue'] or sd.supressDispatcherQuery:
            return _dispatchNoSigCheck(sd, args, kwargs, tByT)
        else:
            return DispatcherQuery(sd, tByT)



class _SingleDispatcher(_DispatcherBase):

    def __init__(sd, name, module, style, fn, supressDispatcherQuery, typeHelper, _t=Missing):
        assert isinstance(name, str), f'name must be a string'
        if not isinstance(module, str): module = str(module)
        assert issubclass(style, (_FasterSingleDispatcher, Partial)), f'{name} - style must be nullary, unary, rmu, binary, unary1 or binary2'
        assert callable(fn), f'{name} - fn must be callable'
        sd.style = style
        sd.name = name
        sd.module = module
        sd.fn = fn
        if _t is Missing:
            sd._sig = Missing
            sd._argNames = Missing
            sd._retType = NO_TYPE
            sd._t_ = Missing
        else:
            sd._sig = _t.argTypes
            sd._argNames = Missing
            sd._retType = _t.retType
            sd._t_ = _t
        sd._numArgsNeeded = Missing
        sd.pass_tByT = False
        sd.supressDispatcherQuery = supressDispatcherQuery          # calls the function rather than returns the dispatch when all args are types
        sd.typeHelper = typeHelper
        sd.tByTByATs = {}
        sd.__doc__ = fn.__doc__ if hasattr(fn, '__doc__') else None

    def _selectDispatcher(sd, argTypes):
        return _checkDispatcherForSD(sd, argTypes)

    @property
    def fullname(sd):
        return sd.module + '.' + sd.name

    @property
    def sig(sd):
        if sd._sig is Missing: sd._determineSignature()
        return sd._sig

    @property
    def retType(sd):
        if sd._sig is Missing: sd._determineSignature()
        return sd._retType

    @property
    def _t(sd):
        if sd._sig is Missing: sd._determineSignature()
        return sd._t_

    def _determineSignature(sd):
        sig = inspect.signature(sd.fn)
        sd._retType = sig.return_annotation
        if sd._retType in _BonesTByPythonT:
            raise TypeError(f'{sd.fullname} - illegal return type {sd._retType}, use {_BonesTByPythonT[sd._retType]} instead')
        argNames = []
        argTypes = []
        for argName, parameter in sig.parameters.items():
            if argName == 'tByT':
                sd.pass_tByT = True
            else:
                if parameter.kind == inspect.Parameter.VAR_POSITIONAL:
                    raiseLessPipe(TypeError(f'{sd.fullname} has *%s' % argName))
                elif parameter.kind == inspect.Parameter.VAR_KEYWORD:
                    pass
                else:
                    if parameter.default == NO_TYPE:
                        argNames += [argName]
                        argTypes += [parameter.annotation]
                    else:
                        pass
        sd._sig = tuple(argTypes)
        sd._argNames = argNames
        sd._numArgsNeeded = len(sd.sig)
        sd._t_ = BTFn(BTTuple(*sd._sig), sd._retType)


class _MultiDispatcher(_DispatcherBase):

    def __new__(cls, *dispatchers):
        name = dispatchers[0].name
        style = dispatchers[0].style
        if style == unary1: style = unary
        if style == binary2: style = binary
        ds = []
        for d in dispatchers:
            if isinstance(d, _MultiDispatcher):
                for d in d.dBySig.values():
                    if isinstance(d, _FasterSingleDispatcher):
                        if style == unary:
                            if d.style != unary1: raise TypeError(f'{name}() is unary - can\'t change to {d.style}')
                        elif style == binary:
                            if d.style != binary2: raise TypeError(f'{name}() is binary - can\'t change it to {d.style}')
                        else:
                            raiseLessPipe(ProgrammerError('unhandled _FasterSingleDispatcher subclass'))
                        ds.append(d)
                    elif isinstance(d, _SingleDispatcher):
                        if d.style != style:
                            raiseLessPipe(TypeError(f'Expected {style} got {d.style}'))
                        ds.append(d)
                    else:
                        raiseLessPipe(ValueError("unknown dispatcher type"))
            elif isinstance(d, _FasterSingleDispatcher):
                if style == unary:
                    if d.style != unary1: raise TypeError(f'{name}() is unary - can\'t change to {d.style}')
                elif style == binary:
                    if d.style != binary2: raise TypeError(f'{name}() is binary - can\'t change it to {d.style}')
                else:
                    raiseLessPipe(ProgrammerError('unhandled _FasterSingleDispatcher subclass'))
                ds.append(d)
            elif isinstance(d, _SingleDispatcher):
                if d.name != name: raise ProgrammerError()
                if d.style != style:
                    raiseLessPipe(TypeError(f'{name} - expected {style} got {d.style}'))
                ds.append(d)
            else:
                raiseLessPipe(ProgrammerError("unhandled dispatcher class"))
        dBySig = {}
        for d in ds:
            oldD = dBySig.get(d.sig, Missing)
            if oldD is not Missing and oldD.module != d.module:
                raise SyntaxError(f'Found definition of {_ppFn(name, d.sig)} in "{d.module}" and "{oldD.module}"')
            dBySig[d.sig] = d
        if len(dBySig) == 1:
            # this can occur in a REPL where a function is being redefined
            # SHOULDDO think this through as potentially we could overload functions in the repl accidentally which
            #  would be profoundly confusing
            return d
        md = super().__new__(cls)
        md.name = name
        md.style = style
        md.dBySig = dBySig
        md.dtByTByATs = {}
        md._t_ = Missing
        md._checkMDDef()
        md.__doc__ = None
        return md

    @property
    def _t(md):
        if md._t_ is Missing:
            md._t_ = BTUnion(*(d._t for sig, d in md.dBySig.items()))
        return md._t_

    def _selectDispatcher(md, argTypes):
        return _selectDispatcherFromMD(md, argTypes)

    def _checkMDDef(md):
        overlap = False
        if overlap:
            raiseLessPipe(SyntaxError("The signatures of the provided dispatcher do not uniquely resolve"))


class _FasterSingleDispatcher(_SingleDispatcher):
    # removes a couple of calls compared to _SingleDispatch (faster and easier to step through)
    def __init__(fsd, name, module, fn, supressDispatcherQuery, typeHelper, _t=Missing):
        super().__init__(name, module, fsd.__class__, fn, supressDispatcherQuery, typeHelper, _t)
    def __call__(fsd, *args, **kwargs):  # func(...)
        raiseLessPipe(SyntaxError(f'Illegal syntax {fsd.name}(...)'))
    def __rrshift__(fsd, arg):  # arg >> func
        raiseLessPipe(SyntaxError(f'Illegal syntax arg >> {fsd.name}'))
    def __rshift__(fsd, arg):    # func >> arg
        if hasattr(arg, '__rrshift__'):
            try:
                return arg.__rrshift__(fsd)
            except:
                return NotImplemented
        else:
            raiseLessPipe(SyntaxError(f'{fsd.name} >> arg - illegal syntax for a {fsd.style.name}'))


class unary1(_FasterSingleDispatcher):
    name = 'unary1'
    numPiped = 1
    numLeft = 1
    numRight = 0
    def __call__(u1, *args, **kwargs):  # func(arg)
        arg = args[0]
        io = dict(hasValue=False)
        argTypes = (arg if _isType(arg, io) else _typeOf(arg),)
        d, tByT = _checkDispatcherForU1(u1, argTypes)
        if io['hasValue'] or d.supressDispatcherQuery:
            return _dispatchNoSigCheck(d, args, kwargs, tByT)
        else:
            return DispatcherQuery(d, tByT)
    def __rrshift__(u1, arg):  # arg >> func
        io = dict(hasValue=False)
        argTypes = (arg if _isType(arg, io) else _typeOf(arg),)
        d, tByT = _checkDispatcherForU1(u1, argTypes)
        if io['hasValue'] or d.supressDispatcherQuery:
            return _dispatchNoSigCheck(d, (arg,), {}, tByT)
        else:
            return DispatcherQuery(d, tByT)


class binary2(_FasterSingleDispatcher):
    name = 'binary2'
    numPiped = 2
    numLeft = 1
    numRight = 1
    def __call__(b2, *args, **kwargs):  # func(arg1, arg2)
        arg1, arg2 = args
        if arg1 is TBC or arg2 is TBC: return _PartialBinary2(b2, arg1, arg2)
        io = dict(hasValue=False)
        argTypes = (arg1 if _isType(arg1, io) else _typeOf(arg1), arg2 if _isType(arg2, io) else _typeOf(arg2))
        d, tByT = _checkDispatcherForB2(b2, argTypes)
        if io['hasValue'] or d.supressDispatcherQuery:
            return _dispatchNoSigCheck(d, args, kwargs, tByT)
        else:
            return DispatcherQuery(d, tByT)
    def __rrshift__(b2, arg1):  # arg1 >> func
        return _PartialBinary2(b2, arg1, TBC)
class _PartialBinary2(object):
    def __init__(db2, b2, arg1, arg2):
        db2.b2 = b2
        db2.arg1 = arg1
        db2.arg2 = arg2
    def __rshift__(db2, arg2):  # func >> arg2
        return db2._dispatch(arg2)
    def __call__(db2, arg):  # func >> arg2
        return db2._dispatch(arg)
    def _dispatch(db2, arg):
        if db2.arg1 is TBC: arg1 = arg; arg2 = db2.arg2
        if db2.arg2 is TBC: arg1 = db2.arg1; arg2 = arg
        io = dict(hasValue=False)
        argTypes = (arg1 if _isType(arg1, io) else _typeOf(arg1), arg2 if _isType(arg2, io) else _typeOf(arg2))
        d, tByT = _checkDispatcherForDB2(db2, argTypes)
        if io['hasValue'] or d.supressDispatcherQuery:
            return _dispatchNoSigCheck(d, (arg1, arg2), {}, tByT)
        else:
            return DispatcherQuery(d, tByT)


class Partial(object):
    name = 'Partial'
    numPiped = 0
    numLeft = 0
    numRight = 0

    def __new__(cls, dispatcher, isPiping, args, kwargs):
        numArgsGiven = len(args)
        if numArgsGiven < cls.numPiped:
            raiseLessPipe(SyntaxError(f'{dispatcher.name} needs at least {cls.numPiped} arg' + ('s' if (cls.numPiped > 1) else '')))
        if not (iTBC := [i for (i, a) in enumerate(args) if a is TBC]):     # if a is an numpy.ndarray then == makes things weird
            return dispatcher._dispatch(args, kwargs)
        else:
            p = super().__new__(cls)
            p.dispatcher = dispatcher
            p.args = args
            p.kwargs = kwargs
            p.numArgsGiven = numArgsGiven
            p.iTBC = iTBC
            p.isPiping = isPiping   # True if a >> has been encountered
            p._t_ = Missing
            p.tByTByATs = {}
            return p

    def __call__(p, *args, **kwargs):
        if p.isPiping: raiseLessPipe(SyntaxError(f'syntax not of form {_prettyForm(p.__class__)}'))
        if len(args) > len(p.iTBC): raiseLessPipe(SyntaxError(f'{p.dispatcher.name} - too many args - got {len(args)} needed {len(p.iTBC)}'))
        newArgs =  _atPut(p.args, p.iTBC[0:len(args)], args)
        newKwargs = dict(p.kwargs)
        newKwargs.update(kwargs)
        return p.__class__(p.dispatcher, False, newArgs, newKwargs)

    def __rrshift__(p, arg):  # arg >> func
        if p.numLeft == 0:
            # if we are here then the arg does not implement __rshift__ so this is a syntax error
            raiseLessPipe(SyntaxError(f'syntax not of form {_prettyForm(p.__class__)}'))
        else:
            if p.isPiping: raiseLessPipe(SyntaxError(f'For {p.dispatcher.name} - syntax is not of form {_prettyForm(p.__class__)}'))
            if len(p.iTBC) != p.numPiped:
                raiseLessPipe(SyntaxError(f'{p.dispatcher.name} needs {len(p.iTBC)} args but {p.numPiped} will be piped'))
            newArgs = _atPut(p.args, p.iTBC, [arg] + [TBC] * (p.numPiped - 1))
            return p.__class__(p.dispatcher, True, newArgs, p.kwargs)

    def __rshift__(p, arg):  # func >> arg
        if p.numRight == 0:
            return NotImplemented
        else:
            if isinstance(p, rau):
                if isinstance(arg, _SingleDispatcher):
                    if arg.style in (nullary, unary, binary, ternary):
                        raiseLessPipe(TypeError(f'An rau may not consume a nullary, unary, binary, ternary'))
                    if arg.style == rau:
                        raiseLessPipe(NotYetImplemented('could make sense...'))
                if len(p.iTBC) != p.numPiped: raise SyntaxError(f'needs {len(p.iTBC)} args but {p.numPiped} will be piped')
                newArgs = _atPut(p.args, p.iTBC[0:1], [arg])
            elif isinstance(p, binary):
                if not p.isPiping: raiseLessPipe(SyntaxError(f'syntax not of form {_prettyForm(p.__class__)}'))
                if isinstance(arg, MultiFn) and arg.dispatcher.style is rau:
                    raiseLessPipe(NotYetImplemented(
                        f'>> binary >> rau >> x not yet implemented use parentheses >> binary >> (rau >> x)',
                        ErrSite(p.__class__, '>> binary >> rau >> x nyi')
                    ))
                newArgs = _atPut(p.args, p.iTBC[0:1], [arg])
            elif isinstance(p, ternary):
                if not p.isPiping: raiseLessPipe(SyntaxError(f'syntax not of form {_prettyForm(p.__class__)}'))
                if len(p.iTBC) == 2:
                    if isinstance(arg, MultiFn) and arg.dispatcher.style is rau:
                        raiseLessPipe(NotYetImplemented(
                            f'>> ternary >> rau >> x >> y not yet implemented use parentheses >> ternary >> (rau >> x) >> y',
                            ErrSite(p.__class__, '>> ternary >> rau >> x >> y nyi')
                        ))
                    newArgs = _atPut(p.args, p.iTBC[0:2], [arg, TBC])
                elif len(p.iTBC) == 1:
                    if isinstance(arg, MultiFn) and arg.dispatcher.style is rau:
                        raiseLessPipe(NotYetImplemented(
                            f'>> ternary >> x >> rau >> y not yet implemented use parentheses >> ternary >> x >> (rau >> y)',
                        ErrSite(p.__class__, '>> ternary >> x >> rau >> y nyi')
                        ))
                    newArgs = _atPut(p.args, p.iTBC[0:1], [arg])
                else:
                    raiseLessPipe(ProgrammerError())
            else:
                raiseLessPipe(ProgrammerError())
            return p.__class__(p.dispatcher, True, newArgs, p.kwargs)

    def __repr__(p):
        return f"{p.dispatcher.name}({', '.join([repr(arg) for arg in p.args])})"

    @property
    def sig(p):
        sig = p.dispatcher.sig
        return tuple(sig[i] for i in p.iTBC)

    @property
    def retType(p):
        return p.dispatcher._retType

    @property
    def _t(p):
        # OPEN: could check that the number of arguments in the partial doesn't exceed the number of args in the
        # multidispatcher - the available dispatchers for a partial could be filtered from the md on each partial creation?
        # lots of extra work - just filter once on dispatch? actually not a problem as length is handled in the
        # dispatcher selection.
        if p._t_ is Missing:
            try:
                if isinstance(p.dispatcher, _SingleDispatcher):
                    try:
                        argTypes = [p.dispatcher.sig[iTBC] for iTBC in p.iTBC]
                    except IndexError:
                        # number of args error so we know this dispatcher will not be found so throw a TypeError
                        raise TypeError('Needs more description')
                    if len(argTypes) == 1:
                        t = BTFn(argTypes[0], p.dispatcher._retType)
                    else:
                        t = BTFn(BTTuple(*argTypes), p.dispatcher._retType)
                elif isinstance(p.dispatcher, _MultiDispatcher):
                    ts = []
                    for sig, d in p.dispatcher.dBySig.items():
                        try:
                            argTypes = [sig[iTBC] for iTBC in p.iTBC]
                        except IndexError:
                            # number of args error so we know this dispatcher will not be found so ignore
                            break
                        if len(argTypes) == 1:
                            t = BTFn(argTypes[0], d._retType)
                        else:
                            t = BTFn(BTTuple(*argTypes), d._retType)
                        ts.append(t)
                    if len(ts) == 0:
                        raise TypeError('Needs more description')
                    elif len(ts) == 1:
                        t = ts[0]
                    else:
                        t = BTUnion(*ts)
                else:
                    raise ProgrammerError("missing dispatcher type")
            except TypeError as ex:
                raise
            except Exception as ex:
                print(p.dispatcher.sig if isinstance(p.dispatcher, _SingleDispatcher) else p.dispatcher.dBySig.values())
                print(p.iTBC)
                print(p.dispatcher._retType)
                raise TypeError(f'Can\t generate type on partially bound {d.name} - needs more detail in this error message ')
            p._t_ = t
        return p._t_


class nullary(Partial):
    name = 'nullary'
    numPiped = 0
    numLeft = 0
    numRight = 0

class unary(Partial):
    name = 'unary'
    numPiped = 1
    numLeft = 1
    numRight = 0

class rau(Partial):
    name = 'rau'
    numPiped = 1
    numLeft = 0
    numRight = 1

class binary(Partial):
    name = 'binary'
    numPiped = 2
    numLeft = 1
    numRight = 1

class ternary(Partial):
    name = 'ternary'
    numPiped = 3
    numLeft = 1
    numRight = 2



def _checkDispatcherForU1(u1, argTypes):
    sig = u1.sig
    doesFit, tByT = _fitsSignature(argTypes, sig)
    if not doesFit and sig[0] != NO_TYPE:
        raiseLessPipe(TypeError(f"Can't find {u1.name}{str(argTypes)}"))
    return u1, tByT

def _checkDispatcherForB2(b2, argTypes):
    sig = b2.sig
    doesFit, tByT = _fitsSignature(argTypes, b2.sig)
    if not doesFit:
        match = True
        distances = Missing
        for tArg, tSig in zip(argTypes, sig):
            if tSig is NO_TYPE:
                pass
            else:
                doesFit, tByT, distances = cacheAndUpdate(fitsWithin(tArg, tSig), tByT, distances)
                if not doesFit:
                    match = False
                    break
        if not match:
            raiseLessPipe(TypeError(f"Can't find {b2.name}{str(argTypes)}"))
    return b2, tByT

def _checkDispatcherForDB2(db2, argTypes):
    sig = db2.b2.sig
    tByT = {}
    match = True
    distances = Missing
    for tArg, tSig in zip(argTypes, sig):
        if tSig is NO_TYPE:
            pass
        else:
            doesFit, tByT, distances = cacheAndUpdate(fitsWithin(tArg, tSig), tByT, distances)
            if not doesFit:
                match = False
                break
    if not match:
        raiseLessPipe(TypeError(f"Can't find {db2.b2.name}{str(argTypes)}"))
    return db2.b2, tByT

def _checkDispatcherForSD(sd, argTypes):
    tByT = sd.tByTByATs.get(argTypes, Missing)
    if tByT is Missing:
        match = False
        if len(argTypes) >= len(sd.sig):            # caller is likely passing optional arguments
            match = True
            argDistances = []
            tByT = {}
            for tArg, tSig in zip(argTypes[0:len(sd.sig)], sd.sig):
                if tSig is NO_TYPE:
                    pass
                else:
                    doesFit, tByT, argDistance = cacheAndUpdate(fitsWithin(tArg, tSig), tByT, 0)
                    if not doesFit:
                        match = False
                        break
                    argDistances.append(argDistance)
            distance = sum(argDistances)
        if not match:
            with context(showFullType=True):
                lines = [
                    f'Can\'t find {_ppFn(sd.name, argTypes)} in:',
                    f'  {_ppFn(sd.name, sd.sig, sd._argNames)} in {sd.module}'
                ]
                print('\n'.join(lines), file=sys.stderr)
                raiseLessPipe(TypeError('\n'.join(lines)))
        sd.tByTByATs[argTypes] = tByT
    return sd, tByT

def _selectDispatcherFromMD(md, argTypes):
    d, tByT = md.dtByTByATs.get(argTypes, (Missing, {}))
    if d is Missing:
        matches = []
        fallbacks = []
        # search though each bound function ignoring discrepancies where the declared type is NO_TYPE
        for sig, d in md.dBySig.items():
            distance = 10000
            if len(argTypes) == len(sig):
                fallback = False
                match = True
                argDistances = []
                tByT = {}
                for tArg, tSig in zip(argTypes, sig):
                    if tSig is NO_TYPE:
                        fallback = True
                        argDistances.append(0.5)
                    else:
                        doesFit, tByT, argDistance = cacheAndUpdate(fitsWithin(tArg, tSig, False), tByT, 0)
                        if not doesFit:
                            match = False
                            break
                        argDistances.append(argDistance)
                if match:
                    distance = sum(argDistances)
                    if fallback:
                        fallbacks.append((d, tByT, distance, argDistances))
                    else:
                        matches.append((d, tByT, distance, argDistances))
            if distance == 0:
                break
        if distance == 0:
            d, tByT, distance, argDistances = matches[-1]
        elif len(matches) == 0 and len(fallbacks) == 0:
            raiseLessPipe(_cantFindMatchError(md, argTypes))
        elif len(matches) == 1:
            d, tByT, distance, argDistances = matches[0]
        elif len(matches) == 0 and len(fallbacks) == 1:
            d, tByT, distance, argDistances = fallbacks[0]
        elif len(matches) > 0:
            matches.sort(key=lambda x: x[2])
            # MUSTDO warn of potential conflicts that have not been explicitly noted
            if matches[0][2] != matches[1][2]:
                d, tByT, distance, argDistances = matches[0]
            else:
                # too many at same distance so report the situation nicely
                caller = f'{md.name}({",".join([repr(e) for e in argTypes])})'
                print(f'{caller} fitsWithin:', file=sys.stderr)
                for d, tByT, distance, argDistances in matches:
                    callee = f'{d.name}({",".join([repr(argT) for argT in d.sig])}) (argDistances: {argDistances}) defined in {d.module}'
                    print(f'  {callee}', file=sys.stderr)
                raiseLessPipe(TypeError(f'Found {len(matches)} matches and {len(fallbacks)} fallbacks for {caller}'))
        elif len(fallbacks) > 0:
            fallbacks.sort(key=lambda x: x[2])
            # MUSTDO warn of potential conflicts that have not been explicitly noted
            if fallbacks[0][2] != fallbacks[1][2]:
                d, tByT, distance, argDistances = fallbacks[0]
            else:
                # too many at same distance so report the situation nicely
                caller = f'{md.name}({",".join([repr(e) for e in argTypes])})'
                print(f'{caller} fitsWithin:', file=sys.stderr)
                for d, tByT, distance, argDistances in matches:
                    callee = f'{d.name}({",".join([repr(argT) for argT in d.sig])}) (argDistances: {argDistances}) defined in {d.module}'
                    print(f'  {callee}', file=sys.stderr)
                raiseLessPipe(TypeError(f'Found {len(matches)} matches and {len(fallbacks)} fallbacks for {caller}'))
        else:
            raise ProgrammerError('Can\'t get here')
        md.dtByTByATs[argTypes] = d, tByT
    return d, tByT

def _fitsSignature(a, b):
    if len(a) != len(b): return False
    doesFit, tByT = _sigCache.get((a, b), (Missing, {}))
    if doesFit is Missing:
        distances = Missing
        for i, aT in enumerate(a):
            doesFit, tByT, distances = cacheAndUpdate(fitsWithin(aT, b[i]), tByT, distances)
            if not doesFit:
                break
        _sigCache[(a, b)] = doesFit, tByT
    return doesFit, tByT


def _dispatchNoSigCheck(d, args, kwargs, tByT):
    _retType = d._retType
    if d.pass_tByT:
        if d.typeHelper:
            tByT = d.typeHelper(*args, tByT=tByT, **kwargs)
        answer = d.fn(*args, tByT=tByT, **kwargs)
    else:
        if BETTER_ERRORS:
            answer = _callWithBetterErrors(d, args, kwargs)
        else:
            answer = d.fn(*args, **kwargs)
    if _retType == NO_TYPE or isinstance(answer, DispatcherQuery):
        return answer
    else:
        doesFit, tByT, distances = cacheAndUpdate(fitsWithin(_typeOf(answer), _retType), tByT)
        if doesFit:
            return answer
        else:
            raiseLessPipe(TypeError(f'{d.fullname} returned a {str(_typeOf(answer))} should have have returned a {d._retType} {tByT}'))


# better error messages
# instead of the Python one:
#       TypeError: createBag() missing 1 required positional argument: 'otherHandSizesById'
#
# TypeError: createBag() does match createBag(handId:any, hand:any, otherHandSizesById:any) -> cluedo_bag
# even better say we can't find a match for two arguments

def _callWithBetterErrors(d, args, kwargs):
    try:
        return d.fn(*args, **kwargs)
    except TypeError as ex:
        if ex.args and ' required positional argument'in ex.args[0]:
            print(_sig(d), file=sys.stderr)
            print(ex.args[0], file=sys.stderr)
        raiseLessPipe(ex, True)


        argTs = [_ppType(argT) for argT in args]
        retT = _ppType(x._retType)
        return f'({",".join(argTs)})->{retT} <{x.style.name}>  :   in {x.fullname}'



def _cantFindMatchError(md, argTypes):
    with context(showFullType=True):
        print(f'Can find zero matches for {_ppFn(md.name, argTypes)}', file=sys.stderr)
        for sig, d in md.dBySig.items():
            print(f'  {_ppFn(d.name, sig)} defined in {d.fullname}', file=sys.stderr)
        return TypeError(f"Can find zero matches for {_ppFn(md.name, argTypes)}")


def _ppFn(name, argTypes, argNames=Missing):
    if argNames is Missing:
        return f'{name}({", ".join([_ppType(t) for t in argTypes])})'
    else:
        return f'{name}({", ".join([f"{n}:{_ppType(t)}" for t, n in zip(argTypes, argNames)])})'

def _ppType(t):
    if t is NO_TYPE:
        return "any"
    elif type(t) is type:
        return t.__name__
    else:
        return repr(t)

def _atPut(xs:pylist, os:pylist, ys:pylist) -> pylist:
    xs = list(xs)       # immutable
    for fromI, toI in enumerate(os):
        xs[toI] = ys[fromI]
    return xs

def _prettyForm(style):
    if issubclass(style, nullary):
        return f'{style.name}()'
    else:
        return \
            (f'x >> {style.name}' if style.numLeft > 0 else f'{style.name}') + \
            (' >> y' if style.numRight == 1 else '') + \
            (' >> y >> z' if style.numRight == 2 else '')

def _isType(x, out):
    if isinstance(x, (type, BType)): #, _PartialBinary2, _DispatcherBase, Partial)):
        return True
    else:
        out['hasValue'] = True
        return False

def _typeOf(x):
    if hasattr(x, '_t'):
        return x._t
    else:
        t = builtins.type(x)
        if t is _Proxy:
            t = builtins.type(x._target)
        return _BonesTByPythonT.get(t, t)

def _fnContext(fn, callerFnName, newName=Missing):
    fnname = fn.__name__ if newName is Missing else newName
    # go up the stack to the frame where @coppertop is used to find any prior definition (e.g. import) of the function
    frame = inspect.currentframe()  # do not use `frameInfos = inspect.stack(0)` as it is much much slower
    # discard the frames for registerFn and coppertop
    if frame.f_code.co_name == '_fnContext':
        frame = frame.f_back
    if frame.f_code.co_name == callerFnName:
        frame = frame.f_back
    if frame.f_code.co_name == 'coppertop':  # depending on how coppertop was called this may or may not exist
        frame = frame.f_back
    if frame.f_code.co_name == '__ror__':  # e.g. (lambda...) | (T1^T2)
        frame = frame.f_back
    priorDef = frame.f_locals.get(fnname, Missing)
    if priorDef is Missing:
        priorDef = frame.f_globals.get(fnname, Missing)
    # fi_debug = inspect.getframeinfo(frame, context=0)
    module = frame.f_globals.get('__name__', Missing)
    globals__package__ = frame.f_globals.get('__package__', Missing)
    definedInFunction = frame.f_code.co_name != '<module>'
    return module, fnname, priorDef, definedInFunction



# public functions


def selectDispatcher(mfOrD, argTypes):
    # a little faster than going through the call or pipe interface
    d = mfOrD.dispatcher if isinstance(mfOrD, MultiFn) else mfOrD
    if isinstance(d, unary1):
        u1, tByT = _checkDispatcherForU1(d, argTypes)
        return u1, tByT
    elif isinstance(d, binary2):
        b2, tByT = _checkDispatcherForB2(d, argTypes)
        return b2, tByT
    elif isinstance(d, _SingleDispatcher):
        sd, tByT = _checkDispatcherForSD(d, argTypes)
        return sd, tByT
    elif isinstance(d, _MultiDispatcher):
        sd, tByT = _selectDispatcherFromMD(d, argTypes)
        return sd, tByT
    elif isinstance(d, Partial):
        p = mfOrD
        io = dict(hasValue=False)
        fullArgTypes = list(((arg if _isType(arg, io) else _typeOf(arg)) for arg in p.args)) # list so can replace elements
        for i, iTBC in enumerate(p.iTBC):
            fullArgTypes[iTBC] = argTypes[i]
        fullArgTypes = tuple(fullArgTypes)   # needs to be a tuple so can put in dict
        if isinstance(d.dispatcher, _SingleDispatcher):
            sd, tByT = _checkDispatcherForSD(d.dispatcher, fullArgTypes)
            return sd, tByT
        elif isinstance(d.dispatcher, _MultiDispatcher):
            sd, tByT = _selectDispatcherFromMD(d.dispatcher, fullArgTypes)
            return sd, tByT
        else:
            raise ProgrammerError("Unhandled Partial Case")
    else:
        raise ProgrammerError("Unhandled Case")


def anon(*args):
    if len(args) == 1:
        name, _t, fn = '<lambda>', Missing, args[0]
    elif len(args) == 2:
        name, _t, fn = '<lambda>', args[0], args[1]
    elif len(args) == 3:
        name, _t, fn = args[0], args[1], args[2]
    else:
        raise TypeError('Wrong number of args passed to anon')
    module, fnname, priorDef, definedInFunction = _fnContext(fn, 'anon', name)
    return _SingleDispatcher(fnname, module, unary, fn, False, Missing, _t)



typeOf = coppertop(style=unary1, newName='typeOf')(_typeOf)


def _sig(x):
    if isinstance(x, _MultiDispatcher):
        answer = []
        for sig, d in x.dBySig.items():
            argTs = [_ppType(argT) for argT in sig]
            retT = _ppType(d._retType)
            style = str(d.style.name)
            fullname = str(d.fullname)
            answer.append(f'({",".join(argTs)})->{retT} <{d.style.name}>  :   in {d.fullname}')
        return answer
    else:
        argTs = [_ppType(argT) for argT in x.sig]
        retT = _ppType(x._retType)
        return f'({",".join(argTs)})->{retT} <{x.style.name}>  :   in {x.fullname}'

sig = coppertop(style=unary1, newName='sig')(_sig)


def raiseLessPipe(ex, includeMe=True):
    tb = None
    frame = inspect.currentframe()  # do not use `frameInfos = inspect.stack(0)` as it is much much slower
    # discard the frames for add_traceback
    if not includeMe:
        if frame.f_code.co_name == 'raiseLessPipe':
            frame = frame.f_back
    hasPydev = False
    while True:
        try:
            # frame = sys._getframe(depth)
            frame = frame.f_back
            if not frame: break
        except ValueError as e:
            break
        fullname = frame.f_globals['__name__'] + '.' + frame.f_code.co_name
        ignore = ['IPython', 'ipykernel', 'pydevd', 'coppertop.pipe', '_pydev_imps._pydev_execfile', 'tornado', \
                  'runpy', 'asyncio', 'traitlets']
        # print(fullname)
        if not [fullname for i in ignore if fullname.startswith(i)]:
            # print(fullname)
            tb = types.TracebackType(tb, frame, frame.f_lasti, frame.f_lineno)
        if fullname == '__main__.<module>': break

    while True:
        # frame = sys._getframe(depth)
        frame = frame.f_back
        if not frame: break
        fullname = frame.f_globals['__name__'] + '.' + frame.f_code.co_name
        if fullname.startswith("pydevd"):
            hasPydev = True
    if hasPydev:
        raise ex.with_traceback(tb)
    else:
        raise ex from ex.with_traceback(tb)


def _init():
    # easiest way to keep namespace relatively clean
    from bones.core.metatypes import weaken

    from datetime import date, datetime
    from bones.core.types import pystr, pyint, pyfloat, pydate, pydatetime, num, index, count, offset, null, pybool, \
        pylist, pydict, pytuple

    # weaken - i.e. T1 coerces to any of (T2, T3, ...)  - first is default for a Holder
    weaken(pyint, (offset, index, num, count))
    # weaken(int, (offset, index, num, count, float, pyfloat, pyint))
    weaken(pyfloat, (num,))
    # weaken(float, (num, pyfloat))
    # weaken(str, (pystr,))
    # weaken(date, (pydate,))
    # weaken(datetime, (pydatetime,))
    # weaken(bool, (pybool,))
    # weaken(list, (pylist,))
    # weaken(dict, (pydict,))
    # weaken(tuple, (pytuple,))
    weaken(type(None), (null,))

_init()
