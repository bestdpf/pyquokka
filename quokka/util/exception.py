class QuokkaBaseException(Exception):

    def __init__(self, value):
        self.area = ''
        self.value = value
    
    def __str__(self):
        return repr(self.area + ": " + self.value)

class NetException(QuokkaBaseException):

    def __init__(self, value):
        QuokkaBaseException.__init__(self, value)
        self.area = 'net'

class FlowException(QuokkaBaseException):

    def __init__(self, value):
        QuokkaBaseException.__init__(self, value)
        self.area = 'flow'
