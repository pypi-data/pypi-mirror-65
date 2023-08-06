from corens.mod import lf as lf

def testMain(ns, *args, **kw):
    f = lf(ns)
    V = f("V")
    V("/home/a", 42)
    return ns


_lib = {
    '/bin/main': testMain
}
