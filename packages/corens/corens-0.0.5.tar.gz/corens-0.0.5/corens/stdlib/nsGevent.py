import gevent
from toolz import partial
from gevent.queue import Queue, Empty
from corens.ns import *
from corens.gevt import *


def _queue_init(ns, *args, **kw):
    nsMkdir(ns, "/dev/q")

def _queue_open(ns, ctx, name, **kw):
    q = nsGet(ns, "/dev/q/{}".format(name))
    if q is not None:
        return q
    else:
        q = nsMkdir(ns, "/dev/q/{}".format(name))
        _q = Queue()
        nsSet(ns, "/dev/q/{}/q".format(name), _q)
        nsSet(ns, "/dev/q/{}/put".format(name), partial(_queue_put, ns, ctx, _q))
        nsSet(ns, "/dev/q/{}/get".format(name), partial(_queue_get, ns, ctx, _q))
    return q

def _queue_put(ns, ctx, _queue, data):
    return _queue.put_nowait(data)

def _queue_get(ns, ctx, _queue):
    try:
        return _queue.get_nowait()
    except Empty:
        return None

_lib = {
    '/bin/gevent': nsGevent,
    '/bin/spawn': nsSpawn,
    '/bin/daemon': nsDaemon,
    '/bin/loop': nsLoopUser,
    '/sbin/loop': nsLoopSys,
    '/sbin/killall': nsKillAll,
    '/bin/schedule': nsSchedulerIntervalJob,
    '/bin/scheduleN': nsSchedulerIntervalJob,
    '/bin/scheduleINT': nsSchedulerIntervalJob,
    '/bin/sps': nsSchedulerPS,
    '/bin/ps': nsGeventPS,
}

_tpl = {
    'queue': {
        'open': _queue_open,
        'init': _queue_init
    }
}
