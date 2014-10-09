from quokka.util.funcs import *
from quokka.util.defines import *
from quokka.util.exception import *
from quokka.util.ds import *

class BaseAlg(object):
    def __init__(self):
        pass

    def setFlowMap(self, flowMap):
        self.flowMap = flowMap

    def setTopo(self, topo):
        self.topo = topo

    def run(self):
       pass

class KLevel(BaseAlg):

    def __init__(self):
        pass

    def setPara(self, mbCnt, numLst, level):
        """
        mbCnt is the number of mb types
        numLst is the list for number of mb for each type
        level is the maximal length of MB chains
        """
        """
        TO DO
        """
        self.pool = self.topo.pool        
        self.mbCnt = mbCnt
        self.numLst = numLst
        self.level = level
        self.selectNum = numLst

    def run(self):
        self.prepair()
        for i in range(self.level):
            self.vote(i)
            self.select()
        return self.finalSelect()

    def  prepair(self):
        self.score = self.make2dList(len(self.pool), self.mbCnt)
        self.candi = [0]*self.mbCnt
        

    def make2dList(self, row, col):
        lst = []
        for i in xrange(row):
            lst += [[0.0]*col]
        return lst

    def vote(self, k):
        for i,j in self.flowMap.table.iteritems():
            for l,flow in j.iteritems():
                if(len(flow.proc)>k):
                    mb = flow.proc[k]
                    if k == 0:
                        src = [flow.src]
                    else:
                        src = self.candi[flow.proc[k-1]]
                    for idx,poolID in enumerate(self.pool):
                        for srci in src:
                            self.score[idx][mb] += flow.size*1000.0/self.topo.getDis(srci, poolID)

    def select(self):
        """
        for j in range(mbCnt):
            maxVal = 0
            maxIdx = -1
            for i range(len(self.pool)):
                if maxVal < self.score[i][j]:
                    maxVal = self.score[i][j]
                    maxIdx = i
            self.candi[j] = self.pool[i]
        """
        for j in range(mbCnt):
            self.candi[j] = self.getNPool(j, self.selectNum[j])

    def finalSelect(self):
        ret = self.make2dList(self.mbCnt, 1)
        for j in range(mbCnt):
            ret[j] = self.getNPool(j, self.num[j])
        return ret

    def getMBCol(self, mb):
        mbLst = []
        for i in range(len(self.pool)):
            mbList.append(self.score[i][mb])
        return mbLst

    def getNPool(self, mb, n):
        lst = self.getMBCol(mb)
        ret = []
        for i in range(len(self.pool)):
            ret.append(i)
        sorted(ret, key=lambda i: lst[i], reverse=True)
        for idx,val in enumerate(ret):
            ret[idx] = self.pool[val]
        cnt = max(n, len(self.pool))
        return ret[0:cnt]

class MDP(BaseAlg):

    def __init__(self):
        pass
    
    def setPara(self, mbCnt, candi):
        self.mbCnt = mbCnt
        self.pool = self.topo.pool
        #TO DO convert pools into mbs
        self.candi = candi

    def run(self):
        pass

    def prepair(self):
        #self.cnt = make2dList(mbCnt, len(self.pool), 0)
        self.cnt = TwoDMap()

    def singleMDP(self, flow, mask = set([])):
        #self.singleTable = make2dList(mbCnt, Defines.mb_max_num, [-1, Defines.INF])
        self.singleTable = TWoDMap()
        proc = flow.proc
        if len(proc) <= 0:
            return [flow.src, flow.dst], self.topo.getDis(flow.src, flow.dst)
        for idx,mb in enumerate(proc):
            if idx == 0:
                for idx2,candi in enumerate(self.candi[mb]):
                    if candi in mask:
                        continue
                    self.singleTable[mb][candi] = [flow.src, self.topo.getDis(flow.src, candi)]
            else:
                for idx2,candi in enumerate(self.candi[mb]):
                    if candi in mask:
                        continue
                    premb = proc[idx-1]
                    for idx3, pre in enumerate(self.candi[premb]):
                        if pre in mask:
                        continue
                        if self.singleTable[mb][candi][1] > self.singleTable[premb][pre][1] + self.topo.getDis(candi, pre):
                            self.singleTable[mb][candi] = [pre , self.singleTable[premb][pre][1] + self.topo.getDis(candi, pre)]
        lastmb = proc[-1]
        finalDis = Defines.INF
        finalmbidx = -1
        finalmb = 0
        for idx, candi in enumerate(self.candi[lastmb]):
            if candi in mask:
                continue
            if finalDis > self.singleTable[lastmb][candi] + self.topo.getDis(candi, flow.dst):
                finalDis = self.singleTable[lastmb][candi] + self.topo.getDis(candi , flow.dst)
                #finalmbidx = idx
                finalmb = candi
        path = []
        #stidx = finalmbidx
        st = finalmb
        path.append(flow.dst)
        for i in range(len(proc)):
            mbidx = len(proc) - i - 1
            mb = proc[mbidx]
            path.append(st)
            st = self.singleTable[mb][st][0]
        return path.reverse(), finalDis

    def incCnt(self, path, proc):
        if len(path) == len(proc) + 2:
            raise AlgException('path\' length is wrong')
        purePath = [1:-1]
        for idx, mb in enumerate(proc):
            if not self.cnt.has_key(mb,purePath[idx]):
                self.cnt[mb][purePath[idx]] = 0
            self.cnt[mb][purePath[idx]] += 1



class QuokkaAlg(BaseAlg):

    def __init__(self):
        self.klevel = KLevel()
        self.mdp = MDP()

    def setTopo(self, topo):
        self.topo = topo
        self.klevel.setTopo(topo)
        self.mdp.setTopo(topo)

    def setFlowMap(self, flowMap):
        self.flowMap = flowMap
        self.klevel.setFlowMap(flowMap)
        self.mdp.setFlowMap(flowMap)

    def run(self):
       pass 
