from quokka.algorithm.alg import *
from quokka.net.topo2 import *
from quokka.net.flow import *
from random import *
from quokka.util.debug import *
from quokka.algorithm.algFF import FFAlg 
from quokka.algorithm.algFLB import FLBAlg
class Event(object):

    def __init__(self, algName = 'quokka', topoName = 'fattree'):
        self.algName = algName
        self.topoName = topoName
        self.rule = [[0,1,2,3,4], [0, 1, 2], [0, 3, 4], [0, 1, 4], [0, 2, 3]]


    def run(self):
        if self.algName == 'quokka':
            return self.runQuokka()
        elif self.algName == 'flb':
            return self.runFLB()
        elif self.algName == 'ff':
            return self.runFF()
        else:
            return None,None

    def runQuokka(self):
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
        numLst = [ 5, 5, 5, 5, 5]
        self.alg.setPara(numLst)
        mdp = self.alg.run()
        return None,mdp
 
    def runFLB(self):
        self.topo = self.getTopo()
        self.topo.addEndNode(Defines.hostRatio)
        Debug.debug('pool', self.topo.pool)
        self.flowMap = self.getFlowMap()
        self.alg = FLBAlg()
        self.alg.setFlowMap(self.flowMap)
        self.alg.setTopo(self.topo)
        numLst = [5, 5, 5, 5, 5]
        self.alg.setPara(numLst)
        mdp = self.alg.run()
        return None, mdp
       
    def getFlowMap(self):
        return self.getDCFlowMap()
        """
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
        """

    def getDCFlowMap(self):
        flowMap = FlowMap()
        for i in range(0,DCDefines.flow_num):
            src = self.getRandHost()
            seed()
            ifOut = random()
            if ifOut < DCDefines.dcOutFlowRatio:
                dst = self.getRandOutNode()
            else:
                dst = self.getRandHost()
            if flowMap.isFlowExist(src, dst):
                continue
            else:
                ruleID = randint(0,4)
                rule = self.rule[ruleID]
                flowMap.addFlow(src, dst, size = 1, proc = rule, lat = self.getRandFlowLatency())
        return flowMap

    def getRandHost(self):
        seed()
        idx = randint(0, len(self.topo.host)-1)
        return self.topo.host[idx]
   
    """ 
    def getRandOutNode(self):
        "use for fatTree"
        seed()
        idx = randint(0, len(self.topo.core)- 1)
        return self.topo.core[idx]
    """
    
    def getRandOutNode(self):
        seed()
        idx = randint(0, len(self.topo.switch) -1)
        return self.topo.switch[idx]        
    
    def getRandFlowSize(self):
        """
        To Do p should be [0,100], not [0,1]
        and do not forget Defines.
        """
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

    def getRandomDis(self, n):
        seed()
        p = random()
        return p*n


    def getRandFlowLatency(self):
        seed()
        p = random()
        if p < DCDefines.dcRealTimeRatio:
            lat = DCDefines.dcRealTimeLatency
        elif p < DCDefines.dcSoftRealTimeRatio:
            lat = DCDefines.dcSoftRealTimeLatency
        else:
            lat = DCDefines.dcNoneRealTimeLatency
        return lat

    def readTopoGML(self, filePath, ndCnt, rand = False):
        topo = Topology()
        for sw in range(ndCnt):
            topo.addIsolateSwitch(sw)
        edgeCnt = 0
        f = open(filePath, 'r')
        for idx1, line in enumerate(f):
            for idx2,val in enumerate(line.split()):
                val = float(val)
                if val != 0:
                    if rand:
                        val = self.getRandomDis(Defines.random_max_delay)
                    Debug.debug('edge from %d to %d %d' % (idx1, idx2, val))
                    topo.addEdge(idx1, idx2, val)#Defines.topo_delay)
                    edgeCnt += 1
        f.close()
        Debug.debug('edge cnt %d in %s' %( edgeCnt, filePath))
        return topo

    def getTopo(self):
        # FatTree, k = 16, delay = 5
        if self.topoName == 'fattree':
            return FatTree(16,Defines.fattree_delay)
        elif self.topoName == 'cernet':
            return self.readTopoGML('Cernet.txt',41,True)
        elif self.topoName == 'carnet':
            return self.readTopoGML('Carnet.txt',44,True)
        elif self.topName == 'as2914':
            return self.readTopoGML('as2914.txt',70)
        else:
            return None
        #return  FatTree(16, Defines.fattree_delay)
        #return self.readTopoGML('Cernet.txt', 41, True)
        #return self.readTopoGML('Carnet.txt', 44, True)#return self.readTopoGML('as2914.txt', 70)
        #return self.readTopoGML('as2914.txt', 70)
