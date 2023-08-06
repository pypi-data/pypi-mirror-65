from clint.textui import puts, indent, colored
from corens.ns import *

def nsHelp(ns, path):
    help = nsGet(ns, path)
    if help is None:
        help = colored.red("Help not found")
    with indent(4, quote=colored.blue(' > ')):
        for h in help.split('\n'):
            puts(h)
    return ns
