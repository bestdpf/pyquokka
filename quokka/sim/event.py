from quokka.algorithm.alg import *
from quokka.net.topo2 import *

class Event(object):

    def __init__(self):
        pass

    def run(self):
        self.topo = self.getTopo()
        self.flowMap = self.getFlowMap()
        self.alg = QuokkaAlg()
        pla,mdp = self.alg.run()
        return pla,mdp
       
    def getFlowMap(self):
        pass

    def getTopo(self):
        # FatTree, k = 16, delay = 5
        return  FatTree(16, 5)
