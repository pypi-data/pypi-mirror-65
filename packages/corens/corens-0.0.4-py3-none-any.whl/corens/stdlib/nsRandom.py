import numpy as np

def randint(ns, start=0, end=100, n=1):
    return np.random.randint(start, end, n)

_lib = {
    '/bin/random': randint
}
