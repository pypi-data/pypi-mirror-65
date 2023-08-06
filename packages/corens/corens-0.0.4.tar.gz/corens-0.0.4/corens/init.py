import re
import sys
from corens.ns import *
from corens.tpl import *
from corens.mod import f

def matchInitName(name):
    r = re.match(r'(\d+)\_([a-zA-Z]+)', name)
    if r is None:
        return False
    if r.span()[0] == 0 and r.span()[1] == len(name):
        return True
    return False

def nsInit(ns, *args, **kw):
    tpls = nsLs(ns, "/templates")
    for i in tpls:
        if matchInitName(i) is True:
            nsMk(ns, i, *args, **kw)
    initd = nsLs(ns, "/etc/init.d")
    _cmds = list(initd.keys())
    _cmds.sort()
    for i in _cmds:
        f(ns, "/etc/init.d/{}/start".format(i))(*args, **kw)
    return True

def nsDummyMain(ns, *args, **kw):
    return ns
