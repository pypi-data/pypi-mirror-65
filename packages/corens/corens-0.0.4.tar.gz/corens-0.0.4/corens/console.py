
import gevent
from clint.textui import indent, puts, colored
from corens.ns import nsGet


def nsConsole(ns,  msg, **kw):
    _msg = msg % kw
    q = nsGet(ns, "/sys/console")
    q.put_nowait(_msg)
    return _msg

def nsConsoleProcess(ns, entries=1):
    q = nsGet(ns, "/sys/console")
    c = 0
    while True:
        if q.qsize() > 0:
            msg = q.get_nowait()
            c += 1
        else:
            break
        with indent(4, quote=colored.green("|")):
            puts(msg)
        if c >= entries:
            break
        gevent.sleep(0.1)

def nsConsoleSize(ns):
    q = nsGet(ns, "/sys/console")
    return q.qsize()
