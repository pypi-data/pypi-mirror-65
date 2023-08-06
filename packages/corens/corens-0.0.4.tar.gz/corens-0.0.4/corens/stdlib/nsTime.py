import time

def stamp(ns):
    return time.time()

def ctx_stamp(ns, ctx):
    return time.time()

_lib = {"/bin/stamp":stamp}
_tpl = {
    'time': {
       'read': ctx_stamp
    }
}
