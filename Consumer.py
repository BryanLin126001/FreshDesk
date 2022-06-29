from ConfigLoaderUtil import ConfigSetting
from datetime import datetime
import Util
import Properties

class Customer:
    configSettingLoader = ConfigSetting()
    behaviourCode = -1
    startTuQueueDatetime = ""
    behaviour = ""
    name = ""
    ticketId = 0

    def __init__(self):
        self.behaviour = self.configSettingLoader.getSingleSettingString("consumer", "behaviour." + str(Util.getRandomNumber(0, 4)))
        self.name = Properties.People.name[Util.getRandomNumber(0, 52)]
        now_dt = Util.getNowWithTimezoneReturnDatetime()
        self.startTuQueueDatetime = now_dt.strftime("%Y-%m-%d %H:%M:%S")
        
    def getBehaviour(self):
        return self.behaviour

    def getName(self):
        return self.name

    def receiveTicket(self, ticketId):
        print(self.name, "got a ticket: ", ticketId)