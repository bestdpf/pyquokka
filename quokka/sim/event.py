from quokka.algorithm.alg import *

class Event(object):

    def __init__(self):
        pass

    def run(self):
        self.flowMap = self.getFlowMap()
        self.topo = self.getTopo()
        self.alg = QuokkaAlg()
        pla,mdp = self.alg.run()
        return pla,mdp
       
    def getFlowMap(self):
        pass

    def getTopo(self):
        pass
