import Util
from ConfigLoaderUtil import ConfigSetting
from datetime import datetime
from pytz import timezone


class DataValidate:
    configSettingLoader = ConfigSetting()
    
    def __init__(self):
        pass

    def ValidateSysArgs(self, argsList):
        numParam = argsList[1]
        ticketQuantity = argsList[2]
        outputParam = argsList[3]
        outPutFile = argsList[4]
        isTicketNumParamOk = self.ValidateNumberParameter(numParam)
        isTicketGenerateQuantityOk = self.ValidateTicketGenerateQuantity(ticketQuantity)
        isOutputFileParamOk = self.ValidateOutputParameter(outputParam)
        idOutputFileOk = self.ValidateOutputFile(outPutFile)
        if isTicketNumParamOk == True and isTicketGenerateQuantityOk == True and isOutputFileParamOk == True and idOutputFileOk == True:
            return True
        else:
            return False
    
    def ValidateTimeFrames(self):
        startAtStr = self.configSettingLoader.getStartAtDatetime()
        endAtStr = self.configSettingLoader.getEndAtDatetime()
        tZone = timezone(self.configSettingLoader.getTimezone())
        start_dt = Util.getDatetimeWithspecificDatetimeStr(startAtStr)
        end_dt = Util.getDatetimeWithspecificDatetimeStr(endAtStr)
        now_dt = datetime.now(tz=tZone)
        if (now_dt - start_dt).total_seconds() > 0 and (end_dt - now_dt).total_seconds() > 0:
            return True
        else:
            return False
    
    def isGoingToClosed(self):
        tZone = timezone(self.configSettingLoader.getTimezone())
        endAtStr = self.configSettingLoader.getEndAtDatetime()
        now_dt = datetime.now(tz=tZone)
        end_dt = Util.getDatetimeWithspecificDatetimeStr(endAtStr)
        if (end_dt - now_dt).total_seconds() <= 0:
            return True
        else:
            return False
    
    def ValidateSysArgsLengh(self, argsList):
        if len(argsList) == 5:
            return True
        else:
            return False
        
    def ValidateNumberParameter(self, numParam):
        if numParam == "-n":
            return True
        else:
            return False

    def ValidateTicketGenerateQuantity(self, ticketQuantity):
        try:
            int(ticketQuantity)
            return True
        except:
            print("Ticket quantity must be a number!")
            return False
    
    def ValidateOutputParameter(self, outputParam):
        if outputParam == "-o":
            return True
        else:
            return False

    def ValidateOutputFile(self, outputFile):
        try:
            fileNameList = outputFile.split(".")
            if fileNameList[1] == "json":
                return True
            else:
                return False
        except:
            print("Illegal file name. File name must be '*.json'")
            return False
