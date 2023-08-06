import sys
import re
import clint
import os.path
from corens.ns import *
from corens.help import *
from corens.mod import f

def nsArgs(ns, args=sys.argv[1:]):
    if len(sys.argv) == 0 or sys.argv[0] == '':
        name = 'corens'
    else:
        name = os.path.basename(sys.argv[0])
    path = "/etc/args"
    nsSet(ns, "/etc/argv", [])
    nsSet(ns, "/etc/name", name)
    argv = nsGet(ns, "/etc/argv")
    _args = nsGet(ns, path)
    args = clint.arguments.Args(args, True)
    _path = "{}/default".format(path)
    nsMkdir(ns, path)
    nsMkdir(ns, _path)
    nsMkdir(ns, '/etc/flags')
    isFlag = False
    prev = None
    while True:
        a = args.pop(0)
        if a is None or isinstance(a, str) is not True:
            break
        if len(a) == 0:
            continue
        if re.match(r'--help', a) is not None:
            if prev is None:
                hpath = "/help/cmd/default"
            else:
                hpath = "/help/cmd/{}".format(prev)
            nsHelp(ns, hpath)
            raise SystemExit
        if re.match(r'\+(.*)', a) is not None and isFlag is False:
            nsSet(ns, "/etc/flags/{}".format(a[1:]), True)
            continue
        if re.match(r'\-(\w+)', a) is not None and isFlag is False:
            nsSet(ns, "/etc/flags/{}".format(a[1:]), False)
            continue
        if re.match(r'--(.*)', a) is not None and isFlag is False:
            isFlag = True
            prev = a[2:]
            continue
        if re.match(r'--(.*)', a) is not None and isFlag is True:
            nsSet(ns, "{}/{}".format(_path, prev), True)
            isFlag = True
            prev = a[2:]
            continue
        if re.match(r'--(.*)', a) is None and isFlag is True:
            nsSet(ns, "{}/{}".format(_path, prev), a)
            isFlag = False
            continue
        if re.match(r'--(.*)', a) is None and isFlag is False:
            prev = a
            argv.append(a)
            _path = "{}/{}".format(path, a)
            nsMkdir(ns, _path)
            continue


    nsSet(ns, "/etc/name", nsGet(ns, "/etc/args/default/appname", name))
    nsSet(ns, "/etc/daemonize", nsGet(ns, "/etc/flags/daemonize", False))
    nsSet(ns, "/etc/console", nsGet(ns, "/etc/flags/console", True))
    nsSet(ns, "/etc/log", nsGet(ns, "/etc/flags/log", True))

    return ns

def nsCmd(ns, *args, **kw):
    argv = nsGet(ns, "/etc/argv", [])
    root = nsGet(ns, "/config/cmd.path")
    kw.update(nsGet(ns, "/config/cmd.kw"))
    out = None
    is_cmd_run = nsGet(ns, "/config/cmd.run")
    if is_cmd_run is True:
        return ns
    for k in argv:
        _args = tuple([out,] + list(args))
        try:
            out = f(ns, "{}/{}".format(root, k))(*_args, **kw)
            nsSet(ns, "/config/cmd.run", True)
        except TypeError:
            nsGlobalError(ns, "Command {}/{} not found".format(root, k))
            continue
    return ns
