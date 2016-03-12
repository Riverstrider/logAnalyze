#-*- coding:utf-8 –*-

from Tkinter import *
from tkFileDialog import *
from threading import *
from time import *
from tkMessageBox import *

import fileProcess,excelProcess

class Application(Frame):

    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.grid(row = 0, column=0)
        self.createWidgets()
        self.filenameRead = 0
        self.filenameWrite = 0

    def selectFileButton(self):
        self.filenameRead = askopenfilename()
        selectFileEntry = Entry(self)
        selectFileEntry.grid(row = 1, column = 2)
        selectFileEntry.delete(0,END)
        selectFileEntry.insert(0,self.filenameRead)

    def saveFileButton(self):
        self.filenameWrite = asksaveasfilename(defaultextension = 'xls')
        saveFileEntry = Entry(self)
        saveFileEntry.grid(row = 3, column = 2)
        saveFileEntry.delete(0,END)
        saveFileEntry.insert(0,self.filenameWrite)

    def beginButton(self):
        log = fileProcess.Log(self.filenameRead,self.filenameWrite)
        log.linesProcess()
        #t1 = Thread(target=log.linesProcess)
        #t1.start()
        beginLabel = Label(self, text='complete!')
        beginLabel.grid(row=5, column=2)


    def createWidgets(self):
        Label(self).grid(row = 0, column=0)
        Label(self,text='          ').grid(row = 1, column = 1)
        Button(self,text='选择Log文件',command = self.selectFileButton).grid(row = 1, column = 0)

        Label(self).grid(row = 2, column = 0)
        Label(self,text='          ').grid(row = 3, column = 1)
        Button(self,text='选择存放地址',command = self.saveFileButton).grid(row = 3, column = 0)

        Label(self).grid(row = 4, column = 0)
        Label(self,text='          ').grid(row = 5, column = 1)
        Button(self,text='开始处理',command = self.beginButton).grid(row = 5, column = 0)

app = Application()
app.master.title("PUCCH Log解析工具v1.5 -lile20160225")
app.master.geometry('400x200')
app.mainloop()
