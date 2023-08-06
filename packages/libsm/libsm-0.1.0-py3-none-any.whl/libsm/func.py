from . import value


def single(f):
    def wrap(*args):
        ret = f(*args)
        return value.Value(ret)
    return wrap
