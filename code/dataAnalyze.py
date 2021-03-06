# -*- coding: utf-8 -*-

from tkMessageBox import *

class Data(object):

    def __init__(self):
        pass

    def sortData(self, data):
        dataTemp = data[:]
        dataNum = len(dataTemp)
        dataIdxList = range(dataNum)
        for i in dataIdxList:
            for j in range(i+1, dataNum):
                if dataTemp[j] > dataTemp[i]:
                    dataTemp[i], dataTemp[j] = dataTemp[j], dataTemp[i]
                    dataIdxList[i], dataIdxList[j] = dataIdxList[j], dataIdxList[i]
        return dataTemp, dataIdxList

    def processReportCycle(self, reportCycle):
        ReportCycleSum = 0
        ReportCycleCnt = 0
        ReportCycleMax = reportCycle[0]
        for ReportCycleEach in reportCycle:
            ReportCycleSum = ReportCycleSum + ReportCycleEach
            ReportCycleCnt += 1
            if (ReportCycleEach > ReportCycleMax):
                ReportCycleMax = ReportCycleEach
        if (0 != ReportCycleCnt):
            return float(ReportCycleSum) / ReportCycleCnt, ReportCycleMax
        else:
            return 0, 0

    def processTB0(self, cell, tb0):
        cellset = set(cell)
        celllist = list(cellset)
        cellNum = len(cellset)
        NACKratio,ACKratio,DTXratio,DTXNACKratio,AnyRatio,elseRatio = [],[],[],[],[],[]
        for cellIdx in cellset:
            ANnum,NACKNum,ACKNum,DTXNum,DTXNACKNum,AnyNum,elseNum= 0,0,0,0,0,0,0
            for i in range(len(tb0)):
                if cell[i] == cellIdx:
                    ANnum += 1
                    if 0 == tb0[i]:
                        NACKNum += 1
                    elif 1 == tb0[i]:
                        ACKNum += 1
                    elif 2 == tb0[i]:
                        DTXNum += 1
                    elif 3 == tb0[i]:
                        DTXNACKNum += 1
                    elif 8 == tb0[i]:
                        AnyNum += 1
                    else:
                        elseNum += 1
            if 0 != ANnum:
                NACKratio.append(float(NACKNum)/ANnum)
                ACKratio.append(float(ANnum)/ANnum)
                DTXratio.append(float(DTXNum)/ANnum)
                DTXNACKratio.append(float(DTXNACKNum)/ANnum)
                AnyRatio.append(float(AnyNum)/ANnum)
                elseRatio.append(float(elseNum)/ANnum)
            else:
                NACKratio.append(0)
                ACKratio.append(0)
                DTXratio.append(0)
                DTXNACKratio.append(0)
                AnyRatio.append(0)
                elseRatio.append(0)
        sortedData, sortedDataIdx = self.sortData(DTXratio)
        #cellsorted = []
        feedbackRatio = []
        for idx in sortedDataIdx:
            #cellsorted.append(celllist[idx])
            feedbackRatio.append(NACKratio[idx])
            feedbackRatio.append(ACKratio[idx])
            feedbackRatio.append(DTXratio[idx])
            feedbackRatio.append(DTXNACKratio[idx])
            feedbackRatio.append(AnyRatio[idx])
            feedbackRatio.append(elseRatio[idx])
            feedbackRatio.append(celllist[idx])
        return feedbackRatio

    def processDTX(self, crnti, ps, pni, dtxflag):
        crntiset = set(crnti)
        crntilist = list(crntiset)
        anNum = len(crnti)
        dtxRatio, psLowRatio, pniHighRatio = [], [], []
        for crntiIdx in crntiset:
            crntiANum, dtxNum, psLowNum, pniHighNum = 0, 0, 0, 0
            for i in range(anNum):
                if crntiIdx == crnti[i]:
                    crntiANum += 1
                    if 1 == dtxflag[i]:
                        dtxNum += 1
                        if -480 > ps[i]:
                            psLowNum += 1
                        if -420 < pni[i]:
                            pniHighNum += 1
            if 0 != crntiANum:
                dtxRatio.append(float(dtxNum)/crntiANum)
            else:
                dtxRatio.append(0)
            if 0 != dtxNum:
                psLowRatio.append(float(psLowNum)/dtxNum)
                pniHighRatio.append(float(pniHighNum)/dtxNum)
            else:
                psLowRatio.append(0)
                pniHighRatio.append(0)
        sortedData, sortedDataIdx = self.sortData(dtxRatio)
        crntiSorted,dtxRatioSorted,psLowRatioSorted,pniHighRatioSorted =[],[],[],[]
        for idx in sortedDataIdx:
            crntiSorted.append(crntilist[idx])
            dtxRatioSorted.append(dtxRatio[idx])
            psLowRatioSorted.append(psLowRatio[idx])
            pniHighRatioSorted.append(pniHighRatio[idx])
        return crntiSorted, dtxRatioSorted, psLowRatioSorted, pniHighRatioSorted

    def processDTXShow(self,crntiSorted, dtxRatio, psLowRatio, pniHighRatio):
        dtxShowList = []
        ueNum = len(crntiSorted)
        if ueNum <= 5:
            dtxShowList.extend(crntiSorted)
            dtxShowList.extend([0]*(5-ueNum))
            dtxShowList.extend(dtxRatio)
            dtxShowList.extend([0]*(5-ueNum))
            dtxShowList.extend(psLowRatio)
            dtxShowList.extend([0]*(5-ueNum))
            dtxShowList.extend(pniHighRatio)
            dtxShowList.extend([0]*(5-ueNum))
        else:
            dtxShowList.extend(crntiSorted[0:5])
            dtxShowList.extend(dtxRatio[0:5])
            dtxShowList.extend(psLowRatio[0:5])
            dtxShowList.extend(pniHighRatio[0:5])
        if (0 == psLowRatio[0] and 0 == pniHighRatio[0]):
            suggestion = ['无DTX，UE反馈正常']
        elif (psLowRatio[0] > pniHighRatio[0]):
            suggestion = ['比对UElog，确认UE没发原因']
        elif (pniHighRatio[0] >= psLowRatio[0]):
            suggestion = ['噪声功率过大，排查环境干扰']
        else:
            suggestion = ['异常情况']
        return dtxShowList + suggestion

    def processTB0Show(self, feedbackRatio):
        tb0ShowList = []
        cellNum = len(feedbackRatio)/7
        if cellNum <= 2:
            tb0ShowList.extend(feedbackRatio)
            tb0ShowList.extend([0]*(14-cellNum*7))
        else:
            tb0ShowList.extend(feedbackRatio[0:14])
        return tb0ShowList

    def resultShow(self, cycleShowList, dtxShowList, tb0ShowList, cqiShowList):
        #tupleAll = tuple(range(58))
        tuple0 = tuple(cycleShowList)
        tuple1 = tuple(dtxShowList)
        tuple2 = tuple(tb0ShowList)
        tuple3 = tuple(cqiShowList)
        tupleall = tuple0 + tuple1 + tuple2 + tuple3
        #print(tupleall)
        showinfo("分析结果", "PUCCH平均上报时间为: %-4.2fms\r\
PUCCH最大上报时间为: %-4.2fms\r\r\
UE级DTX分析:\rLog中DTX最多的5个UE为:\r\
CRNTI        = %-7.0f %-7.0f %-7.0f %-7.0f %-7.0f\r\
DTX占比      = %-8.2f %-8.2f %-8.2f %-8.2f %-8.2f\r\
DTX产生原因：\r\
PsLow占比   = %-8.2f %-8.2f %-8.2f %-8.2f %-8.2f\r\
PniHigh占比 = %-8.2f %-8.2f %-8.2f %-8.2f %-8.2f\r\
下一步定位建议：%s\r\r\
小区级AN分析:\r\
NACK   ACK    DTX    歧义值   any态   其他    L3CellId\r\
%-8.2f %-8.2f %-8.2f %-8.2f %-8.2f %-8.2f %-8.0f\r\
%-8.2f %-8.2f %-8.2f %-8.2f %-8.2f %-8.2f %-8.0f\r\r\
UE级CQI分析:\r\
CRNTI        = %-7.0f %-7.0f %-7.0f %-7.0f %-7.0f\r\
CQI失效占比= %-8.2f %-8.2f %-8.2f %-8.2f %-8.2f\r\
CQI失效原因：\r\
PsLow占比   = %-8.2f %-8.2f %-8.2f %-8.2f %-8.2f\r\
PniHigh占比 = %-8.2f %-8.2f %-8.2f %-8.2f %-8.2f\r\
下一步定位建议：%s\r "% tupleall)





