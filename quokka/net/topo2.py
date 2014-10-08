"""
"""
from quokka.net.node import *
from quokka.util.exception import NetException
from collections import defaultdict as multimap

class Topology(object):

    def __init__(self):
        self.nd = {}
        self.table = self.__table__()
        self.ndID = 0
        self.host = []
        self.pool = []
        self.switch = []
        self.MB = []
        self.INF = 1000000000

    def __table__(self):
        return multimap(self.__table__)

    def getNodeID(self):
        self.ndID = self.ndID + 1
        return self.ndID

    def addIsolateSwitch(self, switchID):
        self.addNode('switch', switchID)

    def addEdge(self,nd1,nd2,delay):
        self.table[nd1][nd2] = delay
        self.table[nd2][nd1] = delay

    def isEdgeExist(self, nd1, nd2):
        return self.table[nd1][nd2] != self.__table__()        

    def getEdge(self,nd1, nd2):
        if self.isEdgeExist(nd1, nd2):
            return self.table[nd1][nd2]
        else:
            return self.INF 

    def getNode(self, nd):
        if not self.nd.has_key(nd):
            return None
        else:
            return nd

    def delEdge(self, nd1, nd2):
        if self.isEdgeExist(nd1 , nd2):
            del self.table[nd1][nd2]
            del self.table[nd2][nd1]
        else:
            raise NetException('no such edge')

    def addSwitch(self, switchID, dstSwitchID, delay):
        self.addIsolateSwitch(switchID)
        self.addEdge(switchID, dstSwitchID, delay)

    def addIsolateHost(self, hostID):
        self.addNode('host', hostID)

    def addIsolatePool(self, poolID):
        self.addNode('pool', poolID)

    def addIsolateMB(self, MBID):
        self.addNode('MB', MBID)

    def addHost(self, hostID, switchID, delay):
        self.addIsolateHost(hostID)
        self.addEdge(hostID, switchID, delay)

    def addPool(self, poolID, switchID, delay):
        self.addIsolatePool(poolID)
        self.addEdge(poolID, switchID, delay)

    def addMB(self, MBID, poolID):
        self.addIsolateMB(MBID)
        self.addEdge(MBID, poolID, delay=0)

    def addNode(self, ndType, ndID):
        if ndType not in ['switch', 'host', 'pool', 'MB']:
            raise NetException('invided node type')
        nd = Node(ndType, ndID)
        self.nd[ndID] = nd
        if ndType == 'switch':
            self.switch.append(ndID)
        elif ndType == 'host':
            self.host.append(ndID)
        elif ndType == 'pool':
            self.pool.append(ndID)
        elif ndType == 'MB':
            self.MB.append(ndID)
        else:
            raise NetException('invided node type')
