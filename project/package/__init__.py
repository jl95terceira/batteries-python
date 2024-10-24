import os.path as os_path
import typing

from . import os, sys

def is_module(path:str):

    if os_path.isfile(path) and path.endswith('.py'): return True

    if not os_path.isdir(path): return False
    
    init_path = os_path.join(path, '__init__.py')
    return os_path.exists(init_path) and \
           os_path.isfile(init_path)

class Enumerator[T]:

    def __init__(self):

        self._managed:list[T] = list()
    
    def E(self, x):

        """
        DEPRECATED - use as callable
        """
        return self(x)
    
    def __call__(self, x):

        self._managed.append(x)
        return x

    def __iter__(self):

        return self._managed.__iter__()

class ChainedCallables:

    def __init__(self, *ff:typing.Callable):

        self._ff = ff

    def __call__(self, *aa, **kaa):

        for f in self._ff: f(*aa, **kaa)

class Raiser:

    def __init__(self, ex:Exception):       self._ex = ex
    def __call__(self)              : raise self._ex

class XorResult():

    def __init__(self, b):        self._b = b
    def __bool__(self)   : return self._b

XOR_TRUE          = XorResult(True)
XOR_FALSE_ALL     = XorResult(False)
XOR_FALSE_NOT_ANY = XorResult(False)

def xor[T](predicate:typing.Callable[[T],bool], *aa:T):

    return XOR_FALSE_ALL     if     all(map(predicate, aa)) else \
           XOR_FALSE_NOT_ANY if not any(map(predicate, aa)) else \
           XOR_TRUE

def xor_None(*aa):

    return xor(lambda a: a is not None, *aa)
