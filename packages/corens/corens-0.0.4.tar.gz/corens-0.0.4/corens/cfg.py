from fs.opener import open_fs
from fs.errors import CreateFailed
from corens.ns import *
from corens.cfg_grammar import nsCfgGrammar
from corens.version import *

def nsDefaults(ns):
    nsSet(ns, "/config/var.redefine", True)
    nsSet(ns, "/config/cmd.run", False)
    nsSet(ns, "/config/path", ["/home", "/bin", "/sbin"])
    nsSet(ns, "/config/dev.path", "/dev")
    nsSet(ns, "/config/cfg.path", ['osfs://.','osfs://tests'])
    nsSet(ns, "/config/cfg.fs", [])
    nsSet(ns, "/config/cfg.files", [])
    nsSet(ns, "/config/library", ["corens.stdlib"])
    nsSet(ns, "/config/user.library", [])
    nsSet(ns, "/config/cmd.path", "/usr/local/bin")
    nsSet(ns, "/config/cmd.kw", {})
    nsSet(ns, "/config/answer", 42)
    nsMkdir(ns, "/etc/corens")
    nsSet(ns, "/etc/corens/version", VERSION)
    nsSet(ns, "/etc/corens/release", RELEASE)
    nsSet(ns, "/etc/corens/url", URL)
    nsSet(ns, "/etc/corens/author", AUTHOR)
    nsSet(ns, "/etc/corens/author.email", AUTHOR_EMAIL)
    nsSet(ns, "/etc/corens/license", LICENSE)
    nsSet(ns, "/etc/version", "0.0")
    nsSet(ns, "/etc/release", "0.0.0")
    nsSet(ns, "/etc/author", "Unknown")
    nsSet(ns, "/etc/author.email", "Unknown@Example.com")
    nsSet(ns, "/etc/license", "GPL3")
    nsSet(ns, "/etc/url", "http://www.example.com")
    nsSet(ns, "/etc/shell.prompt", " #  ")
    for c in nsGet(ns, "/config/cfg.path"):
        try:
            nsGet(ns, "/config/cfg.fs").append(open_fs(c))
        except CreateFailed:
            continue
    ns = nsCfgGrammar(ns)
    return ns
