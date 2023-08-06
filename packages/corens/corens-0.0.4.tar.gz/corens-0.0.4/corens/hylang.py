import fnmatch
from corens.ns import nsMkdir, nsSet, nsGet, nsGlobalError, nsLs
from hy import read_str, eval

def nsImportPfun(ns, env, *vpath):
    for p in vpath:
        env.update(nsLs(ns, p))
    return env


def nsHYmkenv(ns, **kw):
    env = globals()
    env["nsGet"] = nsGet
    env["nsSet"] = nsSet
    env["f"] = nsGet(ns, "/bin/f")
    env["stamp"] = nsGet(ns, "/bin/stamp")
    env["ns"] = ns
    return env

def nsHYInit(ns, *args, **kw):
    env = nsHYmkenv(ns, **kw)
    nsMkdir(ns, "/pbin")
    nsMkdir(ns, "/psbin")
    nsMkdir(ns, "/etc/hy.startup")
    nsSet(ns, "/sys/hylang.enabled", False)
    nsHyEval(ns, '(nsSet ns "/sys/hylang.enabled" True)')
    nsHyEval(ns, '(nsSet ns "/sys/hylang.enabled.stamp" ((f "stamp")))')
    nsGet(ns, "/dev/queue/open")("hy")


def nsHyEval(ns, expression):
    env = nsHYmkenv(ns)
    env = nsImportPfun(ns, env, "/psbin", "/pbin")
    try:
        _expr = read_str(str(expression))
        _res = eval(_expr, env)
    except Exception as e:
        nsGlobalError(ns, "{}".format(e))
        return None
    return _res

def nsHyPipeline(ns, expression):
    _exp = u"""(->
    {})""".format(expression)
    return nsHyEval(ns, _exp)

def nsHyStartup(ns, *args, **kw):
    d = nsLs(ns, "/etc/hy.startup")
    for k in d:
        if fnmatch.fnmatch(k, "*.hy") is True:
            nsHyEval(ns, d[k])
            continue
        if fnmatch.fnmatch(k, "*.hpipeline") is True:
            nsHyPipeline(ns, d[k])
            continue
