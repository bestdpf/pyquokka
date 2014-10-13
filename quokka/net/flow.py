from collections import defaultdict as multimap
from quokka.util.exception import FlowException
from quokka.util.ds import *

class Flow(object):

    def __init__(self, src, dst ,size , proc ):
        self.src = src
        self.dst = dst
        self.size = size
        self.proc = proc

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.src == other.src and self.dst == other.dst
        else:
            return False
        

    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __repr__(self):
        return 'flow\t' + self.__str__()

    def __str__(self):
        return 'src %d dst %d size %d req %s' % (self.src, self.dst, self.size, self.proc)

class FlowMap(object):

    def __init__(self):
        #self.table = self.__table__()
        self.table = TwoDMap()
    """
    def __table__(self):
        return multimap(self.__table__)
    """

    def addFlow(self, src, dst, size, proc  ):
        self.table[src][dst] = Flow(src, dst, size, proc)

    def isFlowExist(self, src, dst):
        #return self.table[src][dst] != self.__table__()
        return self.table.has_key(src, dst)    

    def getFlow(self, src, dst):
        if self.isFlowExist(src, dst):
            return self.table[src][dst]
        else:
            return Flow(src, dst) 

    def delFlow(self, src, dst):
        if self.isFlowExist(src, dst): 
            del self.table[src][dst] 
        else:
            raise FlowException('no such flow')
