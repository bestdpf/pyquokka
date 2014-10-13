from quokka.util.funcs import *
from quokka.util.defines import *
from quokka.util.exception import *
from quokka.util.ds import *
from quokka.util.debug import Debug
import math
import random

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
        Debug.debug('k level run')
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
                            if srci != poolID:
                                dis = self.topo.getDis(srci, poolID)
                                self.score[idx][mb] += flow.size*1000.0/math.log(dis)

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
            mask = set([])
            self.candi[j] = self.getNPool(j, self.selectNum[j], mask)
            for item in self.candi[j]:
                mask.add(item)

    def finalSelect(self):
        ret = self.make2dList(self.mbCnt, 1)
        mask = set([])
        for j in range(self.mbCnt):
            ret[j] = self.getNPool(j, self.numLst[j], mask)
            for item in ret[j]:
                mask.add(item)
        Debug.debug('final selected ret', ret)
        return ret

    def getMBCol(self, mb):
        mbLst = []
        for i in range(len(self.pool)):
            mbLst.append(self.score[i][mb])
        return mbLst

    def getNPool(self, mb, n ,mask):
        lst = self.getMBCol(mb)
        obj = []
        for i in range(len(self.pool)):
            obj.append([i, lst[i]])
        obj.sort(key=lambda i: i[1], reverse=True)
        ret = []
        for i,score in obj:
            if self.pool[i] not in mask:
                ret.append(self.pool[i])
        if n > len(ret):
            raise AlgException('pool num is not enough')
        cnt = min(n, len(ret))
        return ret[0:cnt]

class MDP(BaseAlg):

    def __init__(self):
        pass
        self.seq = 0 
    def setPara(self, candi):
        self.mbCnt = Defines.mb_type 
        self.pool = self.topo.pool
        #TO DO convert pools into mbs
        self.candi = candi

    def run(self):
        Debug.debug('mdp run')
        self.prepair()
        lst = []
        for i,j in self.flowMap.table.iteritems():
            for k, flow in j.iteritems():
                path,dis = self.singleMDP(flow, set([]))
                lst.append([flow, path, dis])
        lst.sort(key = lambda ele: ele[2], reverse = True)
        retLst = []
        for flow,path,dis in lst:
            mask,tp = self.checkMask()
            retPath, retDis = self.singleMDP(flow, mask)
            #no path in this mask
            while retDis >= Defines.INF:
                Debug.debug('!!!!!!!!!!!!!!!!!!!cannot found path in mask!!!!!!!!!!!')
                tPath, tDis = self.singleMDP(flow, set([]))
                minIdx = -1
                minVal = Defines.INF
                for mb in tPath[1:-1]:
                    if mb in mask:
                        if minVal > self.cnt[tp[mb]][mb]:
                            minVal = self.cnt[tp[mb]][mb]
                            minIdx = mb
                mask.remove(minIdx)
                retPath, retDis = self.singleMDP(flow, mask)
            self.incCnt(retPath, flow.proc)
            retLst.append([flow, retPath, retDis])
        return retLst
    """
    def checkMaskType(self):
        ret = set([])
        for i,j in self.cnt.iteritems():
            for k,cnt in j.iteritems():
                if cnt > Defines.general_max:
                    ret.add(i)
        Debug.debug('check mb', ret)
        return ret
    """

    def checkMask(self):
        ret = set([])
        tp = {}
        for i,j in self.cnt.iteritems():
            total = 0
            for k, cnt in j.iteritems():
                total += cnt
            avg = total/len(self.candi[i])
            for k,cnt in j.iteritems():
                if cnt < avg:
                    continue
                random.seed()
                p = random.random()
                if avg < cnt or (cnt-Defines.general_busy)*1.5/(Defines.general_max-Defines.general_busy) > p:
                    ret.add(k)
                    tp[k] = i
        return ret,tp

    def checkOverflow(self):
        mbLst = []
        for i,j in self.cnt.iteritems():
            overflow = False
            for k,cnt in j.iteritems():
                Debug.debug('type %d pool %d cnt %d' %(i, k, cnt))
                if cnt > Defines.general_busy*2:
                    overflow = True
            if overflow:
                Debug.debug('mb type %d overflow' % i)
                mbLst.append(i)
        return mbLst

    def getCandi(self):
        cnt = 0
        for lst in self.candi:
            cnt += len(lst)
        f = open('cnt'+ str(self.seq), 'w')
        f.write('%d' % cnt)
        f.close()
        return cnt
            
    def checkOverflowByDelay(self, retLst):
        self.checkOverflow()
        totalCnt = [0.0]*Defines.mb_type 
        overCnt = [0.0]*Defines.mb_type
        for flow, retPath, retDis in retLst:
            dis = retDis
            for i,mbID in enumerate(retPath[1:-1]):
                dis += self.topo.nd[mbID].getMBDelay(flow.proc[i], self.cnt[flow.proc[i]][mbID])
            for mb in flow.proc:
                totalCnt[mb] +=1
            if dis > Defines.max_delay:
                for mb in flow.proc:
                    overCnt[mb] += 1
        mbNum = [0]* Defines.mb_type
        for idx, lst in enumerate(self.candi):
            mbNum[idx] = len(lst)
        mbLst = []
        for i in range(Defines.mb_type):
            if overCnt[i]/totalCnt[i] > Defines.max_delay_ratio and totalCnt[i] > Defines.general_busy*mbNum[i] :
                mbLst.append(i)   
        return mbLst 


    def checkOverDelay(self, retLst):
        self.seq += 1
        self.getCandi()
        f = open('delay'+str(self.seq), 'w')
        totalCnt = len(retLst)*1.0
        overCnt = 0.0
        for flow, retPath, retDis in retLst:
            dis = retDis
            for i,mbID in enumerate(retPath[1:-1]):
                dis += self.topo.nd[mbID].getMBDelay(flow.proc[i], self.cnt[flow.proc[i]][mbID])
            f.write('%d %d %d\n' % ( flow.src, flow.dst, dis))
            if dis > Defines.max_delay:
                overCnt += 1
        Debug.debug('over delay ratio:',overCnt/totalCnt)
        f.close()
        return overCnt/totalCnt

    def prepair(self):
        #self.cnt = make2dList(mbCnt, len(self.pool), 0)
        self.cnt = TwoDMap()

    def singleMDP(self, flow, mask = set([])):
        #self.singleTable = make2dList(mbCnt, Defines.mb_max_num, [-1, Defines.INF])
        #mask = set([])
        Debug.debug('mdp set', mask)
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
                    self.singleTable[mb][candi] = [-1 , Defines.INF]
                    for idx3, pre in enumerate(self.candi[premb]):
                        if pre in mask:
                            continue
                        if self.singleTable[mb][candi][1] > self.singleTable[premb][pre][1] + self.topo.getDis(candi, pre):
                            self.singleTable[mb][candi] = [pre , self.singleTable[premb][pre][1] + self.topo.getDis(candi, pre)]
        lastmb = proc[-1]
        finalDis = Defines.INF
        finalmbidx = -1
        finalmb = -1
        for idx, candi in enumerate(self.candi[lastmb]):
            if candi in mask:
                continue
            if not self.singleTable.has_key(lastmb, candi):
                continue
            if finalDis > self.singleTable[lastmb][candi][1] + self.topo.getDis(candi, flow.dst):
                finalDis = self.singleTable[lastmb][candi][1] + self.topo.getDis(candi , flow.dst)
                #finalmbidx = idx
                finalmb = candi
        path = []
        #stidx = finalmbidx
        if finalmb == -1:
            return [], Defines.INF
        st = finalmb
        path.append(flow.dst)
        path.append(st)
        for i in range(len(proc)):
            mbidx = len(proc) - i - 1
            mb = proc[mbidx]
            st = self.singleTable[mb][st][0]
            path.append(st)
        path.reverse()
        return path, finalDis

    def incCnt(self, path, proc):
        if len(path) != len(proc) + 2:
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
                    self.minReq[mb] += flow.size 
        for mb in range(Defines.mb_type):
            Debug.debug('raw req', self.minReq[mb])
            self.minReq[mb] /= Defines.general_max
            self.minReq[mb] += 1
            if self.minReq[mb] > Defines.mb_max_num:
                raise AlgException('need more mb instances')

    def run(self):
        # calc min request mb number list
        self.calcMinReq()
        while True:
            Debug.debug('min req', self.minReq)
            self.klevel.setPara(self.minReq)
            pla = self.klevel.run()
            self.mdp.setPara(pla)
            retLst = self.mdp.run()
            if self.mdp.checkOverDelay(retLst) > Defines.max_delay_ratio:
                addLst = self.mdp.checkOverflowByDelay(retLst)
                for addItem in addLst:
                    self.minReq[addItem] += Defines.mb_add_step
            else:
                return pla, retLst
