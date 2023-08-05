class JsDict(dict):
    def __init__(self, o=None):
        if o is None:
            o = {}
        self.__dict__["_JsDict__o"] = o

    def clear(self):
        return self.__o.clear()

    def copy(self):
        return self.__o.copy()

    def has_key(self, k):
        return k in self.__o

    def update(self, *args, **kwargs):
        return self.__o.update(*args, **kwargs)

    def keys(self):
        return self.__o.keys()

    def values(self):
        return self.__o.values()

    def items(self):
        return self.__o.items()

    def pop(self, *args):
        return self.__o.pop(*args)

    def __nonzero__(self):
        return bool(self.__o)

    def __setattr__(self, name, val):
        if val is not None:
            if type(val) is dict:
                val = JsDict(val)
            self.__o[name] = val

    def __getattr__(self, name):
        return self.__o.get(name, None)

    def __getitem__(self, name):
        return self.__o.get(name, None)

    def __setitem__(self, name, val):
        if val is not None:
            if type(val) is dict:
                val = JsDict(val)
            self.__o[name] = val

    def __delitem__(self, name):
        del self.__o[name]

    def __repr__(self):
        return repr(self.__o)

    def __cmp__(self, dict_):
        return self.__cmp__(self.__o, dict_)

    def __contains__(self, item):
        return item in self.__o

    def __iter__(self):
        return iter(self.__o)
