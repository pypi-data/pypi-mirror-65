import re
import sys
import atexit
from corens.ns import *
from corens.tpl import *
from corens.mod import f
from corens.hylang import nsHyEval, nsHyPipeline

def matchInitName(name):
    r = re.match(r'(\d+)\_([a-zA-Z]+)', name)
    if r is None:
        return False
    if r.span()[0] == 0 and r.span()[1] == len(name):
        return True
    return False

def nsInitExecuteFun(ns, path, action, *args, **kw):
    patt = r"^{}(.*)*".format(action)
    actions = nsLs(ns, path)
    for a in actions:
        if re.match(patt, a) is not None:
            actions[a](*args, **kw)

def nsInitExecuteHy(ns, path, action, *args, **kw):
    patt = r"^{}Hy(.*)*".format(action)
    actions = nsLs(ns, path)
    for a in actions:
        if re.match(patt, a) is not None:
            nsHyEval(ns, actions[a])

def nsInitExecutePipe(ns, path, action, *args, **kw):
    patt = r"^{}Pipe(.*)*".format(action)
    actions = nsLs(ns, path)
    for a in actions:
        if re.match(patt, a) is not None:
            nsHyPipeline(ns, actions[a])


def nsInitExecute(ns, action, *args, **kw):
    initd = nsLs(ns, "/etc/init.d")
    _cmds = list(initd.keys())
    _cmds.sort()
    if re.match(r"^stop(.*)*", action) is not None:
        _cmds.reverse()
    for i in _cmds:
        path = "/etc/init.d/{}".format(i)
        nsInitExecuteFun(ns, path, action, *args, **kw)
        nsInitExecuteHy(ns, path, action, *args, **kw)
        nsInitExecutePipe(ns, path, action, *args, **kw)



def nsInit(ns, *args, **kw):
    tpls = nsLs(ns, "/templates")
    for i in tpls:
        if matchInitName(i) is True:
            nsMk(ns, i, *args, **kw)
    nsInitExecute(ns, "start", *args, **kw)
    atexit.register(nsStop, ns)
    return True

def nsStop(ns):
    nsInitExecute(ns, "stop", *(), **{})
    return True

def nsInitMk(ns, name, start, stop, **kw):
    if name in nsLs(ns, "/etc/init.d"):
        return
    path = "/etc/init.d/{}".format(name)
    nsMkdir(ns, path)


def nsDummyMain(ns, *args, **kw):
    return ns
