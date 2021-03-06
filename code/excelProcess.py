# -*- coding: utf-8 -*-

from xlwt import *



class Excel(object):

    def __init__(self):
        self.wbk = 0
        self.sheetIdx = 0
        self.sheetCurrent = 0
        self.firstRowDict = {}
        self.firstRowList = ["LineTime", "LineNumber", "Sfn", "SubFrm", "ENBid", "L3CellId", "CRnti", "Gid", "HRQId",
             "TbNum", "TB0AN", "TB1AN", "ANNPucch", "Ps", "Pni", "ACKvalue",
             "PDLNum", "SDLNum", "M", "AN0", "AN1", "CAflag", "ValidAnum", "Dlposition",
             "DTXflag", "SRn1pucch", "SRflag", "n2pucch", "CQILen", "CQIvalue",
             "RIvalue", "IsValid", "HarqReportCycle", "LogType"]

    def initFirstRow(self):
        n = 0
        for key in self.firstRowList:
            self.firstRowDict[key] = n
            n += 1
        #print(self.firstRowDict)
        for column in range(len(self.firstRowList)):
            self.sheetCurrent.write(0, column, self.firstRowList[column])
        pass

    def writeList2Excel(self, row, dict):
        for key,value in dict.items():
            column = self.firstRowDict.get(key, None)
            #print(key,value,column)
            if None != column:
                self.sheetCurrent.write(row, column, value)
            else:
                continue

    def createNewSheet(self,wbk):
        self.sheetCurrent = wbk.add_sheet("PUCCH Log %d" % self.sheetIdx)
        self.sheetIdx += 1
        self.initFirstRow()

    def saveExcel(self,writeFileName):
        self.wbk.save(writeFileName)

    def createNewExcel(self):
        self.wbk = Workbook(encoding="ascii")
        self.createNewSheet(self.wbk)



