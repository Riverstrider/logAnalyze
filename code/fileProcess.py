#-*- coding:utf-8 –*-

from Tkinter import *
from tkMessageBox import *
from threading import *

import excelProcess,dataAnalyze

class Log(object):

    def __init__(self, filenameRead, filenameWrite):
        self.filenameRead = filenameRead
        self.filenameWrite = filenameWrite
        self.sfn = 0
        self.subSfn = 0
        self.flag = 0

    def findStr(self, line, *str):
        result = True
        for strIdx in str:
            result = result and (-1 != line.find(strIdx))
        return result

    def strLineRecombine(self, str0, str1, strLine):
        posStr0 = strLine.find(str0)
        posStr1 = strLine.find(str1)
        strLineNew = strLine[0:posStr0] + strLine[posStr1:]
        return strLineNew

    def sfnProcess(self,line):
        eachlineStart = re.split('[ ,]',line)
        SfnSubFrm = int(eachlineStart[6],16)
        self.subSfn = SfnSubFrm % 16
        self.sfn = SfnSubFrm / 16

    def anTDDProcess(self, wbk, row, line):
        anDict = {}
        idx = 5
        anDict['LineTime'] = line[0]
        anDict['LineNumber'] = line[1]
        anDict['Sfn'] = self.sfn
        anDict['SubFrm'] = self.subSfn
        anDict['CRnti'] = int(line[idx][2:6], 16)
        anDict['ANNPucch'] = int(line[idx][6:10], 16)
        anDict['Ps'] = int(line[idx + 3][2:6], 16) - 65536
        anDict['Pni'] = int(line[idx + 3][6:10], 16) - 65536
        anDict['PDLNum'] = int(line[idx + 6][2:4], 16)
        anDict['M'] = int(line[idx + 6][4:6], 16)
        anDict['AN0'] = int(line[idx + 6][6:8], 16)
        anDict['AN1'] = int(line[idx + 6][8:10], 16)
        anDict['Dlposition'] = int(line[idx + 9][2:6], 16)
        anDict['DTXflag'] = int(line[idx + 9][8:10], 16)
        anDict['LogType'] = 'TDDAn'
        #print(line)
        wbk.writeList2Excel(row, anDict)
        return anDict['CRnti'],anDict['Ps'],anDict['Pni'],anDict['DTXflag']

    def anFDDProcess(self, wbk, row, line):
        anDict = {}
        idx = 5
        anDict['LineTime'] = line[0]
        anDict['LineNumber'] = line[1]
        anDict['Sfn'] = self.sfn
        anDict['SubFrm'] = self.subSfn
        anDict['CRnti'] = int(line[idx][2:6], 16)
        anDict['ANNPucch'] = int(line[idx][6:10], 16)
        anDict['Ps'] = int(line[idx + 3][2:6], 16) - 65536
        anDict['Pni'] = int(line[idx + 3][6:10], 16) - 65536
        anDict['PDLNum'] = int(line[idx + 6][2:4], 16)
        anDict['SDLNum'] = int(line[idx + 6][4:6], 16)
        anDict['AN0'] = int(line[idx + 6][6:8], 16)
        anDict['AN1'] = int(line[idx + 6][8:10], 16)
        anDict['CAflag'] = int(line[idx + 9][2:4], 16)
        anDict['ValidAnum'] = int(line[idx + 9][4:6], 16)
        anDict['DTXflag'] = int(line[idx + 9][8:10], 16)
        anDict['LogType'] = 'FDDAn'
        #print(line)
        wbk.writeList2Excel(row, anDict)
        return anDict['CRnti'],anDict['Ps'],anDict['Pni'],anDict['DTXflag']

    def anTDDCAANProcess(self, wbk, row, line):
        anDict = {}
        idx = 7
        anDict['LineTime'] = line[0]
        anDict['LineNumber'] = line[1]
        anDict['Sfn'] = self.sfn
        anDict['SubFrm'] = self.subSfn
        anDict['CRnti'] = int(line[idx][2:6], 16)
        anDict['ANNPucch'] = int(line[idx][6:10], 16)
        anDict['Ps'] = int(line[idx + 3][2:6], 16) - 65536
        anDict['Pni'] = int(line[idx + 3][6:10], 16) - 65536
        anDict['PDLNum'] = int(line[idx + 6][2:4], 16)
        anDict['SDLNum'] = int(line[idx + 6][4:6], 16)
        anDict['AN0'] = int(line[idx + 6][6:8], 16)
        anDict['AN1'] = int(line[idx + 6][8:10], 16)
        anDict['M'] = int(line[idx + 9][2:4], 16)
        anDict['ValidAnum'] = int(line[idx + 9][4:6], 16)
        anDict['DTXflag'] = int(line[idx + 9][8:10], 16)
        anDict['LogType'] = 'TDDCA'
        #print(line)
        wbk.writeList2Excel(row, anDict)
        return anDict['CRnti'],anDict['Ps'],anDict['Pni'],anDict['DTXflag']

    def anFmt3ANProcess(self, wbk, row, line):
        anDict = {}
        #print(line)
        idx = 6
        anDict['LineTime'] = line[0]
        anDict['LineNumber'] = line[1]
        anDict['Sfn'] = self.sfn
        anDict['SubFrm'] = self.subSfn
        anDict['CRnti'] = int(line[idx][2:6], 16)
        anDict['ANNPucch'] = int(line[idx][6:10], 16)
        anDict['Ps'] = int(line[idx + 3][2:6], 16) - 65536
        anDict['Pni'] = int(line[idx + 3][6:10], 16) - 65536
        anDict['ACKvalue'] = line[idx + 6][2:10]
        anDict['CAflag'] = int(line[idx + 9][2:4], 16)
        anDict['ValidAnum'] = int(line[idx + 9][4:6], 16)
        anDict['SRflag'] = int(line[idx + 9][6:8], 16)
        anDict['DTXflag'] = int(line[idx + 9][8:10], 16)
        anDict['LogType'] = 'Fmt3'
        wbk.writeList2Excel(row, anDict)
        return anDict['CRnti'],anDict['Ps'],anDict['Pni'],anDict['DTXflag']

    def srProcess(self, wbk, row, line):
        anDict = {}
        #print(line)
        idx = 6
        anDict['LineTime'] = line[0]
        anDict['LineNumber'] = line[1]
        anDict['Sfn'] = self.sfn
        anDict['SubFrm'] = self.subSfn
        anDict['CRnti'] = int(line[idx][2:6], 16)
        anDict['Gid'] = int(line[idx][6:10], 16)
        anDict['Ps'] = int(line[idx + 3][2:6], 16) - 65536
        anDict['Pni'] = int(line[idx + 3][6:10], 16) - 65536
        anDict['SRn1pucch'] = int(line[idx + 6][:-1])
        anDict['SRflag'] = int(line[idx + 9][:-1])
        anDict['LogType'] = 'SR'
        wbk.writeList2Excel(row, anDict)

    def cqiProcess(self, wbk, row, line):
        anDict = {}
        #print(line)
        idx = 5
        anDict['LineTime'] = line[0]
        anDict['LineNumber'] = line[1]
        anDict['Sfn'] = self.sfn
        anDict['SubFrm'] = self.subSfn
        anDict['Gid'] = int(line[idx][2:6], 16)
        anDict['n2pucch'] = int(line[idx][6:10], 16)
        anDict['CQILen'] = int(line[idx + 3][4:6], 16)
        anDict['CQIvalue'] = int(line[idx + 6][2], 16)
        anDict['RIvalue'] = int(line[idx + 9][6:8], 16)
        anDict['IsValid'] = int(line[idx + 9][8:10], 16)
        anDict['LogType'] = 'CQI'
        wbk.writeList2Excel(row, anDict)

    def cqiPsPniProcess(self, wbk, row, line):
        anDict = {}
        #print(line)
        idx = 6
        anDict['LineTime'] = line[0]
        anDict['LineNumber'] = line[1]
        anDict['Sfn'] = self.sfn
        anDict['SubFrm'] = self.subSfn
        anDict['CRnti'] = int(line[idx][2:6], 16)
        anDict['Gid'] = int(line[idx][6:10], 16)
        anDict['Ps'] = int(line[idx + 3][2:6], 16) -65536
        anDict['Pni'] = int(line[idx + 3][6:10], 16) -65536
        if line[3] == 'CQIANInfo:':
            anDict['n2pucch'] = int(line[idx + 9][:-1]) / 65536
            anDict['IsValid'] = (int(line[idx + 9][:-1]) / 256) % 256
            anDict['DTXflag'] = int(line[idx + 12])
        else:
            anDict['n2pucch'] = int(line[idx + 9][2:6], 16)
            anDict['IsValid'] = int(line[idx + 9][8:10], 16)
        anDict['LogType'] = 'CQIPsPni'
        wbk.writeList2Excel(row, anDict)
        return anDict['CRnti'], anDict['Ps'], anDict['Pni'], anDict['IsValid']

    def tb0tb1Process(self, wbk, row, line):
        anDict = {}
        #print(line)
        idx = 5
        anDict['LineTime'] = line[0]
        anDict['LineNumber'] = line[1]
        anDict['Sfn'] = self.sfn
        anDict['SubFrm'] = self.subSfn
        anDict['ENBid'] = int(line[idx][:-1])
        anDict['L3CellId'] = int(line[idx + 3][:-1])
        anDict['CRnti'] = int(line[idx + 6][2:6], 16)
        anDict['Gid'] = int(line[idx + 6][6:10], 16)
        anDict['HRQId'] = int(line[idx + 9][2:4], 16)
        anDict['TbNum'] = int(line[idx + 9][4:6], 16)
        anDict['TB0AN'] = int(line[idx + 9][6:8], 16)
        anDict['TB1AN'] = int(line[idx + 9][8:10], 16)
        anDict['LogType'] = 'TB0TB1'
        wbk.writeList2Excel(row, anDict)
        return anDict['L3CellId'], anDict['TB0AN']

    def reportCycleProcess(self, wbk, row, line):
        anDict = {}
        #print(line)
        anDict['LineTime'] = line[0]
        anDict['LineNumber'] = line[2]
        anDict['Sfn'] = int(line[14], 16) / 16
        anDict['SubFrm'] = int(line[14], 16) % 16
        anDict['HarqReportCycle'] = int(line[11])
        anDict['LogType'] = 'ReportCycle'
        wbk.writeList2Excel(row, anDict)
        return anDict['HarqReportCycle']

    def linesProcess(self):
        data = dataAnalyze.Data()
        file = open(self.filenameRead,'r')
        lines = file.readlines()
        row = 0
        start = 0
        self.flag = 0
        reportCycle, cellId, tb0, crnti, ps, pni, dtxflag = [],[],[],[],[],[],[]
        cqiCrntiList, cqiPsList, cqiPniList, cqiIsvalidList = [], [], [], []
        wbk = excelProcess.Excel()
        wbk.createNewExcel()
        for eachline in lines:
            if row > 59999:
                row %= 60000
                wbk.createNewSheet(wbk.wbk)
            if self.findStr(eachline,"CellInfo:wSfnSubFrm","Pri:INF"):
                eachline = self.strLineRecombine("Module:", "CellInfo:wSfnSubFrm", eachline)
                self.sfnProcess(eachline)
                start = 1
            if self.findStr(eachline,"PUCCH Report End","Pri:INF"):
                start = 0
            if 1 == start:
                if self.findStr(eachline,"TDDANInfo:","Pri:INF"):
                    row += 1
                    eachline = self.strLineRecombine("Module:", "Pri:INF", eachline)
                    eachlineTDDANInfo = eachline.split()
                    CRNTI, Ps, Pni, DTXflag = self.anTDDProcess(wbk, row, eachlineTDDANInfo)
                    crnti.append(CRNTI)
                    ps.append(Ps)
                    pni.append(Pni)
                    dtxflag.append(DTXflag)

                if self.findStr(eachline,"FDDANInfo:","Pri:INF"):
                    row += 1
                    eachline = self.strLineRecombine("Module:", "Pri:INF", eachline)
                    eachlineFDDANInfo = eachline.split()
                    CRNTI, Ps, Pni, DTXflag = self.anFDDProcess(wbk, row, eachlineFDDANInfo)
                    crnti.append(CRNTI)
                    ps.append(Ps)
                    pni.append(Pni)
                    dtxflag.append(DTXflag)

                if self.findStr(eachline,"TDD CA ANInfo","Pri:INF"):
                    row += 1
                    eachline = self.strLineRecombine("Module:", "Pri:INF", eachline)
                    eachlineTDDCAANInfo = eachline.split()
                    CRNTI, Ps, Pni, DTXflag = self.anTDDCAANProcess(wbk, row, eachlineTDDCAANInfo)
                    crnti.append(CRNTI)
                    ps.append(Ps)
                    pni.append(Pni)
                    dtxflag.append(DTXflag)

                if self.findStr(eachline,"FDDANInfo Fmt3:","Pri:INF") or \
                self.findStr(eachline,"TDDANInfo Fmt3:","Pri:INF"):
                    row += 1
                    eachline = self.strLineRecombine("Module:", "Pri:INF", eachline)
                    eachlineFmt3ANInfo = eachline.split()
                    CRNTI, Ps, Pni, DTXflag = self.anFmt3ANProcess(wbk, row, eachlineFmt3ANInfo)
                    crnti.append(CRNTI)
                    ps.append(Ps)
                    pni.append(Pni)
                    dtxflag.append(DTXflag)

                if self.findStr(eachline,"SRInfo","Pri:INF") or \
                self.findStr(eachline,"SRANInfo","Pri:INF"):
                    row += 1
                    eachline = self.strLineRecombine("Module:", "Pri:INF", eachline)
                    eachlineSRInfo = eachline.split()
                    self.srProcess(wbk, row, eachlineSRInfo)

                if self.findStr(eachline,"dCqiPmiValue","Pri:INF"):
                    row += 1
                    eachline = self.strLineRecombine("Module:", "Pri:INF", eachline)
                    eachlineCQIInfo = eachline.split()
                    self.cqiProcess(wbk, row, eachlineCQIInfo)

                if self.findStr(eachline,"dwCACQIFlag","Pri:INF"):
                    row += 1
                    eachline = self.strLineRecombine("Module:", "Pri:INF", eachline)
                    eachlineCQPsPniIInfo = eachline.split()
                    cqiCrnti, cqiPs, cqiPni, cqiIsvalid = self.cqiPsPniProcess(wbk, row, eachlineCQPsPniIInfo)
                    cqiCrntiList.append(cqiCrnti)
                    cqiPsList.append(cqiPs)
                    cqiPniList.append(cqiPni)
                    if cqiIsvalid == 1:
                        cqiIsvalid = 0
                    elif cqiIsvalid == 0:
                        cqiIsvalid = 1
                    cqiIsvalidList.append(cqiIsvalid)

                if self.findStr(eachline,"ENBId","Pri:INF"):
                    row += 1
                    eachline = self.strLineRecombine("Module:", "Pri:INF", eachline)
                    eachlineTB0TB1Info = eachline.split()
                    L3CellId, TB0 = self.tb0tb1Process(wbk, row, eachlineTB0TB1Info)
                    cellId.append(L3CellId)
                    tb0.append(TB0)

                if self.findStr(eachline,"CycleCnt:","Pri:INF"):
                    row += 1
                    eachline = self.strLineRecombine("Module:", "Pri:INF", eachline)
                    eachlineHarqReportCycle = re.split('[ ,]', eachline)
                    cycle = self.reportCycleProcess(wbk, row, eachlineHarqReportCycle)
                    reportCycle.append(cycle)

        avgCycle, maxCycle = data.processReportCycle(reportCycle)
        crntiSorted, dtxRatio, psLowRatio, pniHighRatio = data.processDTX(crnti, ps, pni, dtxflag)
        feedbackRatio = data.processTB0(cellId, tb0)
        cqicrntiSorted, cqidtxRatio, cqipsLowRatio, cqipniHighRatio = \
            data.processDTX(cqiCrntiList, cqiPsList, cqiPniList, cqiIsvalidList)

        cycleShowList = [float(avgCycle)/1e6, float(maxCycle)/1e6]
        dtxShowList = data.processDTXShow(crntiSorted, dtxRatio, psLowRatio, pniHighRatio)
        tb0ShowList = data.processTB0Show(feedbackRatio)
        cqiShowList = data.processDTXShow(cqicrntiSorted, cqidtxRatio, cqipsLowRatio, cqipniHighRatio)
        wbk.saveExcel(self.filenameWrite)
        self.flag = 1
        print(self.flag)
        data.resultShow(cycleShowList, dtxShowList, tb0ShowList, cqiShowList)




