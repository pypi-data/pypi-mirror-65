import time
import uuid
import os.path
from toolz import partial, dissoc
from corens.ns import *
import vedis
import dill

def nsVset(ns, ctx, key, val):
    v = ctx["image"]
    _dir = os.path.dirname(key)
    _k   = bypes(os.path.basename(key))
    isRedefine = nsGet(ns, "/config/var.redefine", True)
    try:
        nsDir = v.Hash(_dir)
    except KeyError:
        nsDir = v.Hash(_dir)
    if _k not in nsDir.keys() and isRedefine is True:
        nsDir[_k] = dill.dumps(val)
    return ns

def nsVget(ns, ctx, key):
    v = ctx["image"]
    _dir = os.path.dirname(key)
    _k   = bypes(os.path.basename(key))
    try:
        nsDir = v.Hash(_dir)
    except KeyError:
        return None
    if _k not in nsDir.keys():
        return None
    return dill.loads(nsDir[_k])

def nsVinit(ns, *args, **kw):
    dev_path = nsGet(ns, "/config/dev/path", "/dev")
    nsMkdir(ns, "{}/volumes")

def nsVopen(ns, name, path=':mem:', **kw):
    dev_path = kw.get("target", None)
    if dev_path is None:
        dev_path = nsGet(ns, "/config/dev/path", "/dev")
    _path = "{}/volumes/{}".format(dev_path, name)
    if nsGet(ns, "{}/id".format(_path)) is not None:
        return (False, None)
    if path != ':mem:':
        path = os.path.abspath(path)
        if not os.path.exists(path) or not os.path.isfile(path):
            nsVmkfs(ns, name, path, **kw)
    ctx = nsMkdir(ns, _path)
    v = vedis.Vedis(path)
    nsSet(ns, "{}/image".format(_path), v)
    nsSet(ns, "{}/stamp".format(_path), time.time())
    nsSet(ns, "{}/id".format(_path), str(uuid.uuid4()))
    nsSet(ns, "{}/path".format(_path), path)
    nsSet(ns, "{}/set".format(_path), partial(nsVset, ns, ctx))
    nsSet(ns, "{}/get".format(_path), partial(nsVget, ns, ctx))
    return (True, _path)

def nsVmkfs(ns, name, path, *patt):
    path = os.path.abspath(path)
    if os.path.exists(path):
        return False
    v = vedis.Vedis(path)
    hdr = v.Hash("/.volume")
    hdr['id'] = dill.dumps(str(uuid.uuid4()))
    hdr['stamp'] = dill.dumps(time.time())
    hdr['name'] = dill.dumps(name)
    hdr['path'] = dill.dumps(path)
    mapping = v.Set('/.mapping')
    for n in patt:
        mapping.add(bytes(n))
    return True

def nsVdiskmount(ns, *args, **kw):
    fstab = nsGet(ns, "/etc/fstab")
    fs = nsGet(ns, "/etc/fs")
    for f in fstab:
        if fstab[f] != 'disk':
            continue
        path = fstab[f].get('path', None)
        if path is None:
            continue
        res, _path = nsVopen(ns, f, path, **kw)
        if res is not True:
            continue
        v = V(ns, "{}/image".format(_path))
        patt = v.Set('/.mapping')
        for p in patt:
            fs[p] = _path
    return True

def nsVdiskunmount(ns, *args, **kw):
    return True

_lib = {
    '/sbin/mkfs.disk': nsVmkfs,
    '/sbin/mount.disk': nsVopen,
    '/sbin/remount.disk': nsVdiskmount,
}

_tpl = {
    'disk': {
        'init': nsVinit,
        'open': nsVopen,
        'mkfs': nsVmkfs
    },
    '01_diskmount': {
        'target': "/etc/init.d",
        'start': nsVdiskmount,
        'stop': nsVdiskunmount,
    }
}
