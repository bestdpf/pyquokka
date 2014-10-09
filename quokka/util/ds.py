from collections import defaultdict as multimap

class TwoDMap(object):

    def __init__(self):
        self.table = self.__table__()

    def __getitem__(self, idx):
        return self.table[idx]

    def __setitem__(self, idx, val):
        self.table[idx] = val

    def has_key(self, idx1, idx2):
        return self.table[idx1] != self.__table__() and \
                self.table[idx1][idx2] != self.__table__()

    def __call__(self, value):
        return self.table.__call__(value)

    def __getattr__(self, attr):
        if hasattr(self.table, attr):
            def wrapper(*args, **kw):
                return getattr(self.table, attr)(*args, **kw)
            return wrapper
        raise AttributeError(attr)

    """
    def __getattr__(self, attr):
        return getattr(self.table, attr)
    """

    def __table__(self):
        return multimap(self.__table__)
