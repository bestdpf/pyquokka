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

    def setPara(self, numLst):
        """
        mbCnt is the number of mb types
        numLst is the list for number of mb for each type
        level is the maximal length of MB chains
        """
        """
        TO DO
        """
        self.pool = self.topo.pool        
        self.mbCnt = Defines.mb_type 
        self.numLst = numLst
        self.level = Defines.max_chain_len
        self.selectNum = numLst

    def run(self):
        self.prepair()
        for i in range(self.level):
            self.vote(i)
            self.select()
        return self.finalSelect()

    def  prepair(self):
        self.score = self.make2dList(len(self.pool), self.mbCnt)
        self.candi = [[]]*self.mbCnt
        

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
        for j in range(self.mbCnt):
            self.candi[j] = self.getNPool(j, self.selectNum[j])

    def finalSelect(self):
        ret = self.make2dList(self.mbCnt, 1)
        for j in range(self.mbCnt):
            ret[j] = self.getNPool(j, self.numLst[j])
        return ret

    def getMBCol(self, mb):
        mbLst = []
        for i in range(len(self.pool)):
            mbLst.append(self.score[i][mb])
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
    
    def setPara(self, candi):
        self.mbCnt = Defines.mb_type 
        self.pool = self.topo.pool
        #TO DO convert pools into mbs
        self.candi = candi

    def run(self):
        self.prepair()
        lst = []
        for i,j in self.flowMap.iteritems():
            for k, flow in j.iteritems():
                path,dis = self.singleMDP(flow, set([]))
                lst.append([flow, path, dis])
        sorted(lst, key = lambda ele: ele[2], reverse = True)
        retLst = []
        for flow,path,dis in lst:
            mask = self.checkCnt()
            retPath, retDis = self.singleMDP(flow, mask)
            #no path in this mask
            if retDis > Defines.INF:
                mask = set([])
                retPath, retDis = self.singleMDP(flow, mask)
            self.incCnt(retPath, flow.proc)
            retLst.append([flow, retPath, retDis])
        return retLst

    def checkCnt(self):
        ret = set([]);
        for i,j in self.cnt.iteritems():
            for k,cnt in j.iteritems():
                if cnt > Defines.general_max:
                    ret.add(k)
        return ret

    def checkOverflow(self):
        mbLst = []
        for i,j in self.cnt.iteritems():
            overflow = False
            for k,cnt in j.iteritems():
                if cnt > Defines.general_max:
                    overflow = True
            mbLst.append(i)

    def checkOverDelay(self, retLst):
        totalCnt = len(retLst)*1.0
        overCnt = 0.0
        for flow, retPath, retDis in retLst:
            dis = retDis
            for i,mbID in enumerate(retPath[1:-1]):
                dis += self.topo.nd[mbID].getMBDelay(self.cnt[flow.proc[i]])
            if retDis > Defines.max_delay:
                overCnt += 1
        return overCnt/totalCnt

    def prepair(self):
        #self.cnt = make2dList(mbCnt, len(self.pool), 0)
        self.cnt = TwoDMap()

    def singleMDP(self, flow, mask = set([])):
        #self.singleTable = make2dList(mbCnt, Defines.mb_max_num, [-1, Defines.INF])
        self.singleTable = TwoDMap()
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
        purePath = path[1:-1]
        for idx, mb in enumerate(proc):
            if not self.cnt.has_key(mb,purePath[idx]):
                self.cnt[mb][purePath[idx]] = 0
            self.cnt[mb][purePath[idx]] += 1



class QuokkaAlg(BaseAlg):

    def __init__(self):
        self.klevel = KLevel()
        self.mdp = MDP()
        self.minReq = [0]*Defines.mb_type

    def setTopo(self, topo):
        self.topo = topo
        self.klevel.setTopo(topo)
        self.mdp.setTopo(topo)

    def setFlowMap(self, flowMap):
        self.flowMap = flowMap
        self.klevel.setFlowMap(flowMap)
        self.mdp.setFlowMap(flowMap)

    def calcMinReq(self):
        for i,j in self.flowMap.table.iteritems():
            for k,flow in j.iteritems():
                for mb in flow.proc:
                    self.minReq[mb] += 1
        for mb in range(Defines.mb_type):
            self.minReq[mb] /= Defines.general_max
            self.minReq[mb] += 1
            if self.minReq[mb] > Defines.mb_max_num:
                raise AlgException('need more mb instances')

    def run(self):
        # calc min request mb number list
        self.calcMinReq()
        while True:
            self.klevel.setPara(self.minReq)
            pla = self.klevel.run()
            self.mdp.setPara(pla)
            retLst = self.mdp.run()
            if self.mdp.checkOverDelay(retLst) > Defines.max_delay_ratio:
                addLst = self.mdp.checkCnt()
                for addItem in addLst:
                    self.minReq[addItem] += Defines.mb_add_step
            else:
                return pla, retLst
