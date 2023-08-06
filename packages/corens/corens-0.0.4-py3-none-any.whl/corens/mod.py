import builtins
import os.path
import pkgutil
import importlib
from toolz import partial
from corens.ns import *
from corens.log import *
from corens.tpl import *

def nsImport(ns, m):
    if type(m) == list:
        for _m in m:
            ns = _nsImport(ns, _m)
    elif type(m) == str:
        return nsImport(ns, m)
    else:
        return ns
    return ns

def I(ns, name, fun):
    return nsSet(ns, name, partial(fun, ns))

def _nsImport(ns, module):
    for loader, module_name, is_pkg in pkgutil.walk_packages(importlib.import_module(module).__path__):
        _module = loader.find_module(module_name).load_module(module_name)
        try:
            _lib = getattr(_module, '_lib')
        except AttributeError:
            _lib = None
            pass
        try:
            _tpl = getattr(_module, '_tpl')
        except AttributeError:
            _tpl = None
            pass
        if _lib is not None:
            for k in _lib:
                nsSet(ns, k, partial(_lib[k], ns))
        if _tpl is not None:
            for m in _tpl:
                nsTemplate(ns, m, **_tpl[m])
    return ns

def f(ns, *n):
    out = []
    for _n in n:
        out.append(fN(ns, _n))
    if len(out) == 1:
        return out[0]
    else:
        return (*out,)

def fN(ns, name):
    if name[0] == "/":
        fun = nsGet(ns, name, None)
        if fun is None:
            nsError(ns, "Call for unknown full-path function %(fun)s", fun=name)
            return None
        return fun
    for p in nsGet(ns, "/config/path"):
        fun = nsGet(ns, "{}/{}".format(p, name), None)
        if fun is None:
            continue
        return fun
    nsError(ns, "Call for unknown function %(fun)s", fun=name)
    return None

def F(ns, *funcs):
    for _f in funcs:
        _nf = f(ns, _f)
        if _nf is None:
            continue
        setattr(builtins, os.path.basename(_f), _nf)
    return ns

def lf(ns):
    f = nsGet(ns, "/bin/f")
    return f
