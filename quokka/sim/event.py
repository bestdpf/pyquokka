from quokka.algorithm.alg import *
from quokka.net.topo2 import *
from quokka.net.flow import *
from random import *
from quokka.util.debug import *
from quokka.algorithm.algFF import FFAlg 
from quokka.algorithm.algFLB import FLBAlg
class Event(object):

    def __init__(self):
        self.rule = [[0,1,2,3,4], [0, 1, 2], [0, 3, 4], [0, 1, 4], [0, 2, 3]]

    def run(self):
        self.topo = self.getTopo()
        self.topo.addEndNode(Defines.hostRatio)
        Debug.debug('pool', self.topo.pool)
        self.flowMap = self.getFlowMap()
        self.alg = QuokkaAlg()
        self.alg.setFlowMap(self.flowMap)
        self.alg.setTopo(self.topo)
        pla,mdp = self.alg.run()
        return pla,mdp
  
    def runFF(self):
        self.topo = self.getTopo()
        self.topo.addEndNode(Defines.hostRatio)
        Debug.debug('pool', self.topo.pool)
        self.flowMap = self.getFlowMap()
        self.alg = FFAlg()
        self.alg.setFlowMap(self.flowMap)
        self.alg.setTopo(self.topo)
        numLst = [4, 4, 4, 4, 4]
        self.alg.setPara(numLst)
        mdp = self.alg.run()
        return mdp
 
    def runFLB(self):
        self.topo = self.getTopo()
        self.topo.addEndNode(Defines.hostRatio)
        Debug.debug('pool', self.topo.pool)
        self.flowMap = self.getFlowMap()
        self.alg = FLBAlg()
        self.alg.setFlowMap(self.flowMap)
        self.alg.setTopo(self.topo)
        numLst = [4, 4, 4, 4, 4]
        self.alg.setPara(numLst)
        mdp = self.alg.run()
        return mdp
       
    def getFlowMap(self):
        flowMap = FlowMap()
        for i in range(0, Defines.flow_num):
            src = self.getRandHost()
            seed()
            ifOut = random()
            if ifOut < Defines.outFlowRatio:
                dst = self.getRandOutNode()
            else:
                dst = self.getRandHost()
            if flowMap.isFlowExist(src, dst):
                continue
            else:
                ruleID = randint(0,4)
                rule = self.rule[ruleID]
                flowMap.addFlow(src, dst, size = 1,proc = rule)
        return flowMap

    def getRandHost(self):
        seed()
        idx = randint(0, len(self.topo.host)-1)
        return self.topo.host[idx]

    def getRandOutNode(self):
        seed()
        idx = randint(0, len(self.topo.core)- 1)
        return self.topo.core[idx]

    def getRandFlowSize(self):
        seed()
        p = random()
        if p < shortSmallRatio:
            size = 50
        elif p <shortLargeRatio:
            size = 1000
        elif p < longSmallRatio:
            size = 1
        else:
            size = 10
        return size

    def readTopo(self):
        pass

    def getTopo(self):
        # FatTree, k = 16, delay = 5
        return  FatTree(16, Defines.fattree_delay)
