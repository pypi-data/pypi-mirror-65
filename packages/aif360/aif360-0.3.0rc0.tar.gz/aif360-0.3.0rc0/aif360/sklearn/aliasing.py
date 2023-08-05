from functools import wraps
import sys


def aka(*names):
    def wrapper(func):
        func.__aliases__ = set(names)
        @wraps(func)
        def identity(*args, **kwargs):
            return func(*args, **kwargs)
        return identity
    return wrapper

def handle_aliases(name):
    mod = sys.modules[name]
    for k, v in vars(mod).copy().items():
        for a in getattr(v, '__aliases__', ()):
            wrapped = wraps(v)(lambda *args, **kwargs: v(*args, **kwargs))
            wrapped.__doc__ = "Alias of :func:`{}`.".format(k)
            setattr(mod, a, wrapped)
