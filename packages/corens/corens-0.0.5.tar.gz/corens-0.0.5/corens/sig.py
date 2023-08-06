import signal
from toolz import partial
from corens.ns import *

def nsSignalAdd(ns, path, *handlers):
    hpath = "{}/handlers".format(path)
    for h in handlers:
        nsGet(ns, hpath).add(h)

def nsSignalAddInit(ns, path, *handlers):
    hpath = "{}/handlers".format(path)
    spath = "{}/signal".format(path)
    _handlers = nsGet(ns, hpath)
    sig = nsGet(ns, spath)
    for h in handlers:
        if h in _handlers:
            continue
        _handlers.add(h)
        signal.signal(sig, h)

def nsSignalInit(ns, *args, **kw):
    nsMkdir(ns, "/sys/signals")
    for s in signal.Signals:
        _p = "/sys/signals/{}".format(s.name)
        nsMkdir(ns, _p)
        nsSet(ns, "/sys/signals/{}/signal".format(s.name), s)
        nsSet(ns, "/sys/signals/{}/n".format(s.name), s.value)
        nsSet(ns, "/sys/signals/{}/handlers".format(s.name), set())
        nsSet(ns, "/sys/signals/{}/add".format(s.name), partial(nsSignalAdd, ns, _p))
        nsSet(ns, "/sys/signals/{}/init".format(s.name), partial(nsSignalAddInit, ns, _p))
    return

def nsSignalSetup(ns, *args, **kw):
    for s in nsLs(ns, "/sys/signals"):
        spath = "/sys/signals/{}".format(s)
        sig = nsGet(ns, "{}/signal".format(spath))
        handlers = nsGet(ns, "{}/handlers".format(spath))
        for h in handlers:
            signal.signal(sig, h)
    return
