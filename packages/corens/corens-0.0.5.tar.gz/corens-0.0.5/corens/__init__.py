from gevent import monkey
if monkey.patch_all() is not True:
    print("Gevent monkey patching was not succesful")
import sys
from toolz import partial
from corens.ns import NS as _NS
from corens.ns import nsGet
from corens.mod import F as _F
from corens.mod import f as _f
from corens.mod import lf as lf
from corens.mod import p as p



from corens.cfg import nsDefaults

def NS(*args, **kw):
    from corens.mod import nsImport
    ns = _NS()
    ns = nsDefaults(ns)
    ns = nsImport(ns, nsGet(ns, "/config/library"))
    cargs = kw.get('args', sys.argv[1:])
    _f(ns, "/bin/args")(cargs)
    _f(ns, "/sbin/signalinit")(*args, **kw)
    _f(ns, "/sbin/envinit")(*args, **kw)
    for c in nsGet(ns, "/config/cfg.files"):
        _f(ns, "/bin/Cfg")(c)
    ns = nsImport(ns, nsGet(ns, "/config/user.library"))
    _f(ns, "/bin/gevent")(*args, **kw)
    _f(ns, "/sbin/network_init")(*args, **kw)
    _f(ns, "/sbin/vnsinit")(*args, **kw)
    _f(ns, "/sbin/hyinit")(*args, **kw)
    _f(ns, "/sbin/hy.startup")(*args, **kw)
    _f(ns, "/sbin/signalsetup")(*args, **kw)
    _f(ns, "/sbin/envsetup")()
    _f(ns, "/sbin/init")(*args, **kw)
    _f(ns, "/bin/cmd")(*args, **kw)
    if nsGet(ns, "/config/cmd.run") is False:
            _f(ns, "/bin/main")(*args, **kw)
    return (ns, partial(_f, ns), partial(_F, ns))
