import gevent
from toolz import partial
import socket
from corens.ns import *
from corens.tpl import nsMk
from corens.gevt import *

def _net_client_init(ns, *args, **kw):
    nsMkdir(ns, "/net/tcp/out")
    nsMkdir(ns, "/net/udp/out")

def _net_tcp_cli_proto(ns, name, port, fun_read=None, fun_write=None):
    nsMkdir(ns, "/net/tcp/out/{}/{}".format(name, port))


def _net_server_init(ns, *args, **kw):
    nsMkdir(ns, "/net/tcp/in")
    nsMkdir(ns, "/net/udp/in")

def nsNetworkInit(ns, *args, **kw):
    nsMkdir(ns, "/bin/network")
    nsMkdir(ns, "/bin/network/read")
    nsMkdir(ns, "/bin/network/write")
    nsMkdir(ns, "/net")
    nsMkdir(ns, "/net/tcp")
    nsMkdir(ns, "/net/udp")
    #nsMk(ns, network_client)
    #nsMk(ns, network_server)



_lib = {
    "/sbin/network_init": nsNetworkInit
}

_tpl = {
    'network_client': {
        'init': _net_client_init
    },
    'network_server': {
        'init': _net_server_init
    }

}
