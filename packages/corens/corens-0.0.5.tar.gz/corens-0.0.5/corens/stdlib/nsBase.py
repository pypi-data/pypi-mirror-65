from corens.ns import *
from corens.mod import I, nsImport, f
from corens.tpl import nsTemplate, nsMk
from corens.cfg_grammar import nsCfgFSLoad
from corens.cfg_grammar import nsCfgLoad
from corens.log import *
from corens.arrghs import *
from corens.help import *
from corens.console import *
from corens.version import nsVersion, nsRelease
from corens.vns import *
from corens.init import *
from corens.mod import p
from corens.hylang import nsHYInit, nsHyEval, nsHyPipeline, nsHyStartup
from corens.env import nsEnvInit, nsEnvSetup, nsEnvRemovePid
from corens.sig import nsSignalInit, nsSignalSetup
from corens.txt import nsTxt


def n(ns):
    return ns

_lib = {
    '/bin/mkdir': nsMkdir,
    '/bin/memory': nsMemory,
    '/bin/get': nsGet,
    '/bin/set': nsSet,
    '/bin/ls': nsLs,
    '/bin/ns': n,
    '/bin/V': V,
    '/bin/I': I,
    '/bin/f': f,
    '/bin/p': p,
    '/bin/text': nsTxt,
    '/bin/txt': nsTxt,
    '/bin/hy': nsHyEval,
    '/bin/h|': nsHyPipeline,
    '/sbin/hy.startup': nsHyStartup,
    '/bin/import': nsImport,
    '/bin/T': nsTemplate,
    '/bin/Mk': nsMk,
    '/bin/C': nsCfgLoad,
    '/bin/Cfg': nsCfgFSLoad,
    '/bin/debug': nsDebug,
    '/bin/info': nsInfo,
    '/bin/warning': nsWarning,
    '/bin/error': nsError,
    '/bin/critical': nsCritical,
    '/bin/panic': nsPanic,
    '/bin/logsize': nsLogSize,
    '/sbin/logprocessor': nsLogProcess,
    '/bin/args': nsArgs,
    '/bin/cmd': nsCmd,
    '/bin/help': nsHelp,
    '/bin/console': nsConsole,
    '/sbin/consoleprocessor': nsConsoleProcess,
    '/sbin/corens_version': nsVersion,
    '/sbin/corens_release': nsRelease,
    '/sbin/vnsinit': nsVNSinit,
    '/sbin/hyinit': nsHYInit,
    '/sbin/envinit': nsEnvInit,
    '/sbin/envsetup': nsEnvSetup,
    '/sbin/init': nsInit,
    '/sbin/stop': nsStop,
    '/bin/main': nsDummyMain,
    '/sbin/signalinit': nsSignalInit,
    '/sbin/signalsetup': nsSignalSetup,
    '/bin/atexit/removepid': nsEnvRemovePid,
}
