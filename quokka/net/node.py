"""
network element node
"""
from quokka.util.defines import *
from random import *
from quokka.util.exception import *

class Edge(object):

    def __init__(self, nd1, nd2, delay = 0):
        self.nd1 = nd1
        self.nd2 = nd2
        self.delay = delay

    def __eq__(self,other):
        if isinstance(other, self.__class__):
            return ( self.nd1 == other.nd1 and self.nd2 == other.nd2) \
                    or (self.nd1 == other.nd2 and self.nd2 == other.nd1)
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

class Node(object):

    def __init__(self, ndType, ID):
        self.ndType = ndType
        self.online = True
        self.ID = ID
        self.edge = []
    """
    def addEdge(self, edgeID):
        self.edge.append(edgeID)

    def clearEdge(self):
        self.edge[:] = []

    def delEdge(self, edgeID):
        self.edge.remove(edgeID)
    """

class Host(Node):

    def __init__(self, hostID):
        Node.__init__(self, ndType='host', ID=hostID)

    def setSwitch(self, switchID, dis):
        self.switchID = switchID
        self.dis = dis

class Switch(Node):

    def __init__(self, switchID):
        Node.__init__(self, ndType='switch', ID=switchID)


class Pool(Node):

    def __init__(self, poolID):
        Node.__init__(self, ndType='pool', ID=poolID)
        self.mb = []

    def setSwitch(self, switchID, dis):
        self.switchID = switchID
        self.dis = dis

    def getMBDelay(self, mb_type, flowNum):
        if mb_type == 0:
            mb = Proxy(0)
        elif mb_type == 1:
            mb = IDS(0)
        elif mb_type == 2:
            mb = FireWall(0)
        elif mb_type == 3:
            mb = NAT(0)
        elif mb_type == 4:
            mb = GateWay(0)
        else:
            raise NetException('error mb type number, should be in [0,5)')
        return mb.delay(flowNum)

    """
    def clearMB(self):
        self.mb = []

    def installMB(self, MBID):
        self.mb.append(MBID)
    """

class MB(Node):

    def __init__(self, MBID):
        Node.__init__(self, ndType='MB', ID=MBID)

    def setName(self, name):
        self.name = name

    def delay(self, flowNum):
        return Defines.general_base_delay

    def setPool(self, poolID, dis = 0):
        self.poolID = poolID
        self.dis = dis

class Proxy(MB):

    def __init__(self, MBID):
        MB.__init__(self, MBID)
        self.setName('proxy')

    def delay(self, flowNum):
        seed()
        seq = randint(0,flowNum)
        time = Defines.proxy_base_delay*(seq/Defines.general_speed + 1)    
        return time

class GateWay(MB):
    def __init__(self, MBID):
        MB.__init__(self, MBID)
        self.setName('gateway')

    def delay(self, flowNum):
        seed()
        seq = randint(0, flowNum)
        time = Defines.gateway_base_delay*(seq/Defines.gateway_speed + 1)
        return time

class IDS(MB):
    def __init__(self, MBID):
        MB.__init__(self, MBID)
        self.setName('ids')

    def delay(self, flowNum):
        seed()  
        seq = randint(0, flowNum)
        time = Defines.ids_base_delay*(seq/Defines.ids_speed + 1)
        return time

class FireWall(MB):
    def __init__(self, MBID):
        MB.__init__(self, MBID)
        self.setName('firewall')

    def delay(self, flowNum):
        seed()
        seq = randint(0, flowNum)
        time = Defines.firewall_base_delay*(seq/Defines.firewall_speed + 1)

class NAT(MB):
    def __init__(self, MBID):
        MB.__init__(self, MBID)
        self.setName('nat')

    def delay(self, flowNum):
        seed()
        seq = randint(0, flowNum)
        time = Defines.nat_base_delay*(seq/Defines.nat_speed + 1)
        return time


