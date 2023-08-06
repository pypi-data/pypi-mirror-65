import time
import os
import pretty_errors
from TimeService import TimeServiceClass
from FileService import FileServiceClass

class LogServiceClass(object):
    TimeService = TimeServiceClass()
    FileService = FileServiceClass()

    filePath = "{}{}-Common.log".format("./Log/",TimeService.GetPrintTimeToDay()) 
    tag = ""
    def __init__(self, filePath = None, tag = None):
        if filePath != None:
            self.filePath = filePath
        if tag != None:
            self.tag = tag
        self.FileService.AppendFile(self.filePath, "{}{} {} {}".format("\n", self.TimeService.GetPrintTimeToAll(), self.tag, "- Start \n\n"))
        
    # 打印日志
    def Log(self, content, type=0):
        front = "LogD"
        if type == 0:
            front = "LogD"
        elif type == 1:
            front = "LogW"
        elif type == 2:
            front = "LogE"
        outPrint = "{} {} {}: {}".format(self.TimeService.GetPrintTimeToAll(), self.tag, front, content)
        self.SavePrintToFile(outPrint)
        print(outPrint)

    def LogD(self, *content):
        self.Log(content, 0)

    def LogW(self, *content):
        self.Log(content, 1)

    def LogE(self, *content):
        self.Log(content, 2)

    def SavePrintToFile(self, content):
        if self.filePath:
            self.FileService.AppendFile(self.filePath, content, True)

if __name__ == '__main__':
    LogService = LogServiceClass(tag="ADBServiceClass")
    LogService.Log(15)
    LogService.LogD(16,66)
    LogService.LogW(17)
    LogService.LogE(18)