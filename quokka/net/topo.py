"""
"""
from quokka.net.node import *
from quokka.util.exception import NetException

class Topology(object):

    def __init__(self):
        self.nd = {}
        self.edgeID = 0
        self.ndID = 0
        self.edge = {}
        self.host = []
        self.pool = []
        self.switch = []
        self.MB = []

    def getEdgeID(self):
        self.edgeID = self.edgeID + 1
        return self.edgeID

    def getNodeID(self):
        self.ndID = self.ndID + 1
        return self.ndID

    def addIsolateSwitch(self, switchID):
        self.addNode('switch', switchID)

    def addEdge(self,nd1,nd2,delay):
        #check whether exsit
        edge = Edge(nd1,nd2,delay)
        if self.nd.has_key(nd1):
            for edgeID in self.nd[nd1].edge:
                if edge == self.edge[edgeID]:
                    raise NetException('exist edge')
        if self.nd.has_key(nd2):
            for edgeID in self.nd[nd2].edge:
                if edge == self.edge[edgeID]:
                    raise NetException('exist edge')
        edgeID = self.getEdgeID()
        self.edge[edgeID]=edge
        self.nd[nd1].addEdge(edgeID)
        self.nd[nd2].addEdge(edgeID)
        return edgeID

    def getEdge(self,nd1, nd2):
        if not ( self.nd.has_key(nd1) or self.nd.has_key(nd2)):
            return None
        else:
            edge = Edge(nd1, nd2)
            for edgeID in self.nd[nd1].edge:
                if  edge == self.edge[edgeID]:
                    return edgeID
            return None

    def getNode(self, nd):
        if not self.nd.has_key(nd):
            return None
        else:
            return nd

    def delEdge(self, nd1, nd2):
        edge = Edge(nd1, nd2)
        for edgeID in self.nd[nd1].edge:
            if edge == self.edge[edgeID]:
                try:
                    self.edge.pop(edgeID)
                    self.nd[nd1].edge.remove(edgeID)
                    self.nd[nd2].edge.remove(edgeID)
                except:
                    print "trying to remove unexsit edge " , __name__ 
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
