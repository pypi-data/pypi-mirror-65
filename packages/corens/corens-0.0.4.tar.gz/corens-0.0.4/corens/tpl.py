import re
from collections.abc import Callable
from toolz import partial
from corens.ns import *

def nsTemplate(ns, name, **kw):
    path = "/templates/{}".format(name)
    ctx = nsMkdir(ns, path)
    for k in kw:
        _path =  "{}/{}".format(path, k)
        nsSet(ns, _path, kw[k])
    return ns

def nsMk(ns, name, *args, **kw):
    _t = nsGet(ns, "/templates/{}".format(name))
    dev_path = kw.get("target", None)
    if dev_path is None:
        dev_path = nsGet(ns, "/templates/{}/target".format(name), None)
    if dev_path is None:
        dev_path = nsGet(ns, "/config/dev/path", "/dev")
    _path = "{}/{}".format(dev_path, name)
    ctx = nsMkdir(ns, _path)
    for i in _t:
        if re.match(r'__(.*)', i) is not None:
            continue
        _i = "{}/{}".format(_path, i)
        if isinstance(_t[i], Callable) is True:
            nsSet(ns, _i, partial(_t[i], ns, ctx))
        else:
            nsSet(ns, _i, _t[i])
    _init = nsGet(ns, "{}/{}/init".format(dev_path, name), None)
    if _init is not None and isinstance(_init, Callable) is True:
        ns = _init(*args, **kw)
    return ns
