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

class FLBAlg(BaseAlg):

    def __init__(self):
        pass
        self.seq = 0 
    def setPara(self, numLst):
        self.mbCnt = Defines.mb_type 
        self.pool = self.topo.pool
        self.numLst = numLst
        #TO DO convert pools into mbs
        self.generateCandi()

    def generateCandi(self):
        poolLen = len(self.pool)
        self.candi = [0]*self.mbCnt
        mask = set([])
        random.seed()
        Debug.debug('numLst', self.numLst)
        for mb, cnt in enumerate(self.numLst):
            self.candi[mb] = []
            for i in range(cnt):
                while True:
                    idx = random.randint(0, poolLen -1 )
                    if idx not in mask:
                        mask.add(idx)
                        self.candi[mb].append(self.pool[idx])
                        break

    def run(self):
        Debug.debug('FLBAlg run')
        self.prepair()
        lst = []
        for i,j in self.flowMap.table.iteritems():
            for k, flow in j.iteritems():
                path,dis = self.randPath(flow)
                lst.append([flow, path, dis])
                self.incCnt(path, flow.proc)
        self.checkOverDelay(lst)
        self.checkOverflow()
        return lst

    def randPath(self, flow):
        path = []
        path.append(flow.src)
        random.seed()
        for mb in flow.proc:
            lstLen = len(self.candi[mb])
            idx = random.randint(0, lstLen-1)
            path.append(self.candi[mb][idx])
        path.append(flow.dst)
        dis = 0
        for idx, nd in enumerate(path[0:-1]):
            dis += self.topo.getDis(path[idx], path[idx+1])
        return path,dis

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
        f = open('flbflownum' + str(self.seq), 'w')
        mbLst = []
        for i,j in self.cnt.iteritems():
            overflow = False
            for k,cnt in j.iteritems():
                Debug.debug('type %d pool %d cnt %d' %(i, k, cnt))
                f.write('%d %d %d\n' % (i, k, cnt))
                if cnt > Defines.general_busy*2:
                    overflow = True
            if overflow:
                Debug.debug('mb type %d overflow' % i)
                mbLst.append(i)
        f.close()
        return mbLst

    def getCandi(self):
        cnt = 0
        for lst in self.candi:
            cnt += len(lst)
        f = open('flbcnt'+ str(self.seq), 'w')
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
        f = open('flbdelay'+str(self.seq), 'w')
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

