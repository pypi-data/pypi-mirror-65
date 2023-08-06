from corens.ns import *
from corens.tpl import nsMk

def nsVNSinit(ns, *args, **kw):
    nsSet(ns, "/etc/fstab", {})
    nsMk(ns, "disk")
    return ns

def nsVNSRegister(ns, name, **kw):
    fstab = V(ns, "/etc/fstab")
    if name in fstab:
        return False
    if 'type' not in kw:
        return False
    fstab[name] = kw
    return True

def nsVNSget(ns, name):
    fstab = V(ns, "/etc/fstab")
    return fstab.get(name, None)
