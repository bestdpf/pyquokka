"""
network element node
"""


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

    def addEdge(self, edgeID):
        self.edge.append(edgeID)

    def clearEdge(self):
        self.edge[:] = []

    def delEdge(self, edgeID):
        self.edge.remove(edgeID)

class Host(Node):

    def __init__(self, hostID):
        Node.__init__(self, ndType='host', ID=hostID)


class Switch(Node):

    def __init__(self, switchID):
        Node.__init__(self, ndType='switch', ID=switchID)


class Pool(Node):

    def __init__(self, poolID):
        Node.__init__(self, ndType='pool', ID=poolID)


class MB(Node):

    def __init__(self, MBID):
        Node.__init__(self, ndType='MB', ID=MBID)
