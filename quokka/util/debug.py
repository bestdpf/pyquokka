class Debug(object):
    enable = True
    @classmethod
    def debug(cls, val):
        if cls.enable:
            print val
