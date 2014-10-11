from quokka.net.topo2 import *
from unittest import TestCase
import unittest
from quokka.net.flow import *
from quokka.util.defines import Defines

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

    def testFatTree(self):
        fat = FatTree(4, 5)
        fat.addEndNode(0.5)
        fat.calcShortestPath()
        for sw1 in fat.switch:
            for sw2 in fat.switch:
                Debug.debug(fat.getSwitchDis(sw1, sw2))
                #self.assertTrue(fat.getSwitchDis(sw1, sw2) != Defines.INF)

    def testEdge(self):
        edge1 = Edge(1, 2, 10)
        edge2 = Edge(2, 1, 5)
        self.assertTrue(edge1 == edge2)

    def testFlowMap(self):
        flowMap = FlowMap()
        flowMap.addFlow(0, 1, 100, [])
        self.assertTrue(flowMap.getFlow(0, 1).size == 100)
        flowMap.delFlow(0, 1)
        self.assertFalse(flowMap.isFlowExist(0, 1))
        flowMap.addFlow(0, 1, 100, [])
        flowMap.addFlow(1, 2, 100, [])
        for i,j in flowMap.table.iteritems():
            for k,l in j.iteritems():
                print 'flow[%d][%d] = [%d]' % (i,k,l.size)

    def testMatrix(self):
        mat = [[1,2],[3,4]]
        print mat[0][:]

    def testLst(self):
        lst = [2,1,3]
        lst2 = [3,2,1]
        lst2.sort(key= lambda i: lst[i-1])
        print lst2

if __name__ == '__main__':
    unittest.main()
