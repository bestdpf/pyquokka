class Debug(object):
    enable = True 
    @classmethod
    def debug(cls, *args):
        if cls.enable:
            print args
