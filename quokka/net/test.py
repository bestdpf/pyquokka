from quokka.net.topo2 import *
from unittest import TestCase
import unittest
from quokka.net.flow import *

class TestTopo(TestCase):

    def testTopo(self):
        topo = Topology()
        topo.addIsolateSwitch(0)
        topo.addSwitch(1, 0, 20)
        topo.addHost(2, 1, 10)
        topo.addPool(3, 0, 10)
        self.assertTrue(topo.nd.has_key(0))
        self.assertTrue(topo.nd.has_key(1))
        self.assertTrue(topo.isEdgeExist(0, 1))
        topo.delEdge(0, 1)
        self.assertFalse(topo.isEdgeExist(0, 1))
        topo.addEdge(0, 1, 30)
        topo.addEdge(0, 1, 20)

    def testEdge(self):
        edge1 = Edge(1, 2, 10)
        edge2 = Edge(2, 1, 5)
        self.assertTrue(edge1 == edge2)

    def testFlowMap(self):
        flowMap = FlowMap()
        flowMap.addFlow(0, 1, 100)
        self.assertTrue(flowMap.getFlow(0, 1) == 100)
        flowMap.delFlow(0, 1)
        self.assertFalse(flowMap.isFlowExist(0, 1))
        flowMap.delFlow(0, 1)

if __name__ == '__main__':
    unittest.main()
