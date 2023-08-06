import gevent
import sys
import time
from apscheduler.schedulers.gevent import GeventScheduler
from toolz import partial
from corens.ns import *
from corens.mod import f, lf
from corens.tpl import nsMk

def nsGInput(ns):
    prompt = nsGet(ns, "/etc/shell.prompt")
    sys.stdout.write(prompt)
    sys.stdout.flush()
    gevent.select.select([sys.stdin], [], [])
    return sys.stdin.readline().strip()

def nsGeventTick(ns):
    f = lf(ns)
    V = f("V")
    V("/dev/time", time.time())

def nsSchedulerIntervalJob(ns, seconds, name, fun, *args, **kw):
    if len(args) > 0 and args[0] is ns:
        _fun = fun
    else:
        _fun = partial(fun, ns)
    scheduler = nsGet(ns, "/sys/scheduler")
    return scheduler.add_job(_fun, 'interval', seconds=seconds, name=name, args=args, kwargs=kw, max_instances=1, replace_existing=True)

def nsSchedulerPS(ns):
    return nsGet(ns, "/sys/scheduler").get_jobs()

def nsGeventPS(ns):
    return nsGet(ns, "/sys/greenlets")[1:] +  nsGet(ns, "/sys/greenlets.user")

def nsGevent(ns, *args, **kw):
    nsMkdir(ns, "/proc")
    nsSet(ns, "/dev/time", time.time())
    nsSet(ns, "/sys/greenlets", [])
    nsSet(ns, "/sys/greenlets.user", [])
    nsSet(ns, "/sys/greenlets.kill", False)
    nsSet(ns, "/sys/scheduler", GeventScheduler())
    s = nsGet(ns, "/sys/scheduler")
    nsSchedulerIntervalJob(ns, 60, "/dev/time", nsGeventTick)
    #s.add_job(partial(nsGeventTick, ns), 'interval', seconds=60)
    g = s.start()
    ns = nsProcAlloc(ns, "scheduler", g, scheduler=s)
    glist = nsGet(ns, "/sys/greenlets")
    glist.append(g)
    nsMk(ns, "queue")
    f(ns, "/dev/queue/open")("shell")
    return ns

def nsProcAlloc(ns, name, g, **kw):
    path = "/proc/{}".format(name)
    nsMkdir(ns, path)
    for k in kw:
        nsSet(ns, "{}/{}".format(path, k), kw[k])
    nsSet(ns, "{}/proc".format(path), g)
    nsSet(ns, "{}/stamp".format(path), time.time())
    return ns

def nsSpawn(ns, name, fun, *args, **kw):
    if len(args) > 0 and args[0] is ns:
        _fun = fun
    else:
        _fun = partial(fun, ns)
    g = gevent.Greenlet.spawn(_fun, *args, **kw)
    g.name = name
    nsProcAlloc(ns, name, g)
    glist = nsGet(ns, "/sys/greenlets.user")
    glist.append(g)
    g.start()
    return ns

def nsDaemon(ns, name, fun, *args, **kw):
    if len(args) > 0 and args[0] is ns:
        _fun = fun
    else:
        _fun = partial(fun, ns)
    g = gevent.Greenlet.spawn(_fun, *args, **kw)
    g.name = name
    nsProcAlloc(ns, name, g)
    glist = nsGet(ns, "/sys/greenlets")
    glist.append(g)
    g.start()
    return ns

def _ns_greenlet_loop(ns, *path):
    glist = []
    for p in path:
        glist += nsGet(ns, p)
    try:
        gevent.joinall(glist)
    except KeyboardInterrupt:
        nsKillAll(ns)
        pass

def nsLoopUser(ns):
    return _ns_greenlet_loop(ns, "/sys/greenlets.user")

def nsLoopSys(ns):
    return _ns_greenlet_loop(ns, "/sys/greenlets", "/sys/greenlets.user")


def nsKillAll(ns):
    if nsGet(ns, "/sys/greenlets.kill") is True:
        return ns
    nsGet(ns, "/sys/scheduler").shutdown(wait=False)
    gevent.killall(nsGet(ns, "/sys/greenlets")[1:])
    gevent.killall(nsGet(ns, "/sys/greenlets.user"))
    nsSet(ns, "/sys/greenlets.kill", True)
    return ns
