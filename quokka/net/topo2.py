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
        self.minDis = False
        self.switchDis = self.__table__()

    def __table__(self):
        return multimap(self.__table__)

    def getSwitchDis(self, nd1, nd2):
        if not self.minDis:
            self.calcShortestPath()
            self.minDis = true
        if self.dis[nd1][nd2] != self.__table__():
            return self.switchDis[nd1][nd2]
        else:
            return self.INF

    def getDis(self, nd1, nd2):
        dis1,switchID1 = self.toSwitchDis(nd1)
        dis2,switchID2 = self.toSwitchDis(nd2)
        dis = dis1 + dis2 + self.getSwitchDis(switchID1, switchID2)
        return dis
        

    def toSwitchDis(self, ndID):
        dis = 0
        ID = ndID
        if self.nd[ID].ndType == 'switch':
            return dis, ID
        elif self.nd[ID].ndType == 'MB':
            dis += self.nd[ID].dis
            ID = self.nd[ID].poolID
        # for pool and host
        dis += self.nd[ID].dis
        ID = self.nd[ID].switchID
        return dis, ID
            

    def calcShortestPath(self):
        self.switchDis = self.__table__()
        #Floyd-Warshall Algorithm
        for switchID in self.switch:
            self.switchDis[switchID][switchID] = 0
        for src,j in self.table.iteritems():
            for dst,delay in j.iteritems():
                if self.nd[src].ndType == 'switch' and self.nd[dst].ndType == 'switch':
                    self.switchDis[src][dst] = delay
        for switchID in self.switch:
            for src in self.switch:
                for dst in self.switch:
                    if self.switchDis[src][dst] > self.switchDis[src][switchID] + self.switchDis[switchID][dst]:
                        self.switchDis[src][dst] = self.switchDis[src][switchID] + self.switchDis[switchID][dst]

    def getNodeID(self):
        self.ndID = self.ndID + 1
        return self.ndID

    def addIsolateSwitch(self, switchID):
        switch = Switch(switchID)
        self.nd[switchID] = switch
        self.switch.append(switchID)

    def addEdge(self,nd1,nd2,delay):
        self.table[nd1][nd2] = delay
        self.table[nd2][nd1] = delay
        if self.nd[nd1].ndType == 'pool' or self.nd[nd1].ndType == 'host':
            self.nd[nd1].setSwitch(nd2, delay)
        if self.nd[nd2].ndType == 'pool' or self.nd[nd2].ndType == 'host':
            self.nd[nd2].setSwitch(nd1, delay)
        if self.nd[nd1].ndType == 'MB':
            self.nd[nd1].setPool(nd2, delay)
        if self.nd[nd2].ndType == 'MB':
            self.nd[nd2].setPool(nd1, delay)

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
        host = Host(hostID)
        self.nd[hostID] = host
        self.host.append(hostID) 

    def addIsolatePool(self, poolID):
        pool = Pool(poolID)
        self.nd[poolID] = pool
        self.pool.append(poolID)

    def addIsolateMB(self, MBID):
        mb = MB(MBID)
        self.nd[MBID] = mb
        self.MB.append(MBID)

    def addHost(self, hostID, switchID, delay):
        self.addIsolateHost(hostID)
        self.addEdge(hostID, switchID, delay)

    def addPool(self, poolID, switchID, delay):
        self.addIsolatePool(poolID)
        self.addEdge(poolID, switchID, delay)

    def addMB(self, MBID, poolID):
        self.addIsolateMB(MBID)
        self.addEdge(MBID, poolID, delay=0)

    """
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
    """
