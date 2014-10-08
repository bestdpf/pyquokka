from collections import defaultdict as multimap
from quokka.util.exception import FlowException

class Flow(object):

    def __init__(self, src, dst ,size = 0, proc = []):
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

class FlowMap(object):

    def __init__(self):
        self.table = self.__table__()

    def __table__(self):
        return multimap(self.__table__)

    def addFlow(self, src, dst, size, proc = [] ):
        self.table[src][dst] = Flow(src, dst, size, proc)

    def isFlowExist(self, src, dst):
        return self.table[src][dst] != self.__table__()    

    def getFlow(self, src, dst):
        if self.isFlowExist(src, dst):
            return self.table[src][dst]
        else:
            return [0, []]

    def delFlow(self, src, dst):
        if self.isFlowExist(src, dst): 
            del self.table[src][dst] 
        else:
            raise FlowException('no such flow')
