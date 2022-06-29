import json
import queue
import time
import Util
import InitialUtil
import Properties
from ConfigLoaderUtil import ConfigSetting
from ConfigLoaderUtil import SqlSetting
from ActivityInfo import Ticket
from Consumer import Customer
from datetime import datetime
from pytz import timezone
from DataAccessObj import TicketDAO
from DataAccessObj import DAO
from ProcessRequest import CustomerService
from ProcessRequest import ClosedProcedure

class Freshdesk:
    configSettingLoader = ConfigSetting()
    sqlSettingLoader = SqlSetting()
    dao = DAO()
    conn = dao.getConnection()
    ticketGen = Ticket()
    ticketDao = TicketDAO(conn)
    increaseRange = 0
    ticketQuantity = 0
    outputFile = ""
    ptr = 0
    ticketRegisterList = []
    ticketSoldList = []
    activitiesDataList = []
    pendingCaseList = []
    employeeId = Properties.Employee.employeeId_1
    posId = Properties.Counter.pos_1
    tZone = timezone(configSettingLoader.getSingleSettingString("ticket_metadata_detail", "timezone"))
    today = datetime.now(tz=tZone).strftime("%d %b, %Y")
    
    ticketDetailInfoDict = ticketGen.getDefaultTicketDetailInfo(today, employeeId, posId)

    def __init__(self, ticketQuantity, outputFile):
        print("Initial Data...")
        dataInitialer = InitialUtil.InitialData()
        dataInitialer.InitialAllData()
        InitialUtil.FileClean().deleteOutputFile(outputFile)
        print("Initial Ticket Info...")
        self.ticketQuantity = ticketQuantity
        self.outputFile = outputFile
        self.setTicketGenerateRange()
        
    def greeting(self, cust, ticketId):
        print("Hello, ", cust.name, "welcome to Freshdesk.")
        greetingDatetime = Util.getNowWithTimezoneReturnDatetime().strftime("%Y-%m-%d %H:%M:%S")
        startQueueDatetime = cust.startTuQueueDatetime
        sqlStr = self.sqlSettingLoader.getSqlStatement("UPDATE.R_TKT_ACTIVITY.GREETINGTIMEANDSTARTQUEUETIME")
        valueList = [startQueueDatetime, greetingDatetime, ticketId, sqlStr]
        self.ticketDao.updateTicketBaseOnCustReq(valueList)
        
    def setTicketGenerateRange(self):
        self.increaseRange = self.configSettingLoader.getSingleSettingString("ticketinfo", "ticket.increase.random.range")
        self.ticketGenerateRange = self.ticketQuantity * int(self.increaseRange)

    def nextCustomer(self, cust):
        return cust.getCustomerBehaviour()

    def putTicketIntoActivitiesDataList(self, ticket):
        self.activitiesDataList.append(ticket)
    
    def isTicketIdExists(self, ticketId):
        return ticketId in self.ticketRegisterList

    def addTicketIdToRegisterList(self, ticketId):
        self.ticketRegisterList.append(ticketId)

    def getTicketId(self):
        ticketId = 0
        while True:
            ticketId = Util.getRandomNumberWithoutStartRange(self.ticketGenerateRange)
            if self.isTicketIdExists(ticketId) == False:
                self.addTicketIdToRegisterList(ticketId)
                break
        return ticketId
    
    def copyTicketDefaultDict(self):
        return self.ticketDetailInfoDict.copy()

    def setTicketId(self, ticketId, ticketValueList):
        ticketValueList.insert(0, ticketId)
        return ticketValueList
    
    def setTicketCreateDatetime(self, createDatetime, ticketValueList):
        ticketValueList.append(createDatetime)
        return ticketValueList
    
    def createTickets(self):
        i = 1
        createTicketDatetime = Util.getNowWithTimezoneReturnDatetime().strftime("%Y-%m-%d %H:%M:%S")
        sqlStr = self.sqlSettingLoader.getSqlStatement("INSERT.R_TKT_ACTIVITY.DEFAULTTICKETSINFO")
        while i <= self.ticketQuantity:
            ticketId = self.getTicketId()
            ticketDict = self.copyTicketDefaultDict()
            ticketValueList = list(ticketDict.values())
            ticketValueList = self.setTicketId(ticketId, ticketValueList)
            ticketValueList = self.setTicketCreateDatetime(createTicketDatetime, ticketValueList)
            ticketValueList.append(sqlStr)
            self.ticketDao.updateTicketBaseOnCustReq(ticketValueList)
            i += 1

    def soldTicket(self, ticketId):
        soldDatetime = Util.getNowWithTimezoneReturnDatetime()
        soldDatetimeStr = soldDatetime.strftime("%Y-%m-%d %H:%M:%S")
        self.ticketSoldList.append(ticketId)
        sqlStr = self.sqlSettingLoader.getSqlStatement("UPDATE.R_TKT_ACTIVITY.SOLDDATETIME")
        valueList = [soldDatetimeStr, ticketId, sqlStr]
        self.ticketDao.updateTicketBaseOnCustReq(valueList)
        self.ptr += 1
        
    def isTicketSoldOut(self):
        if len(self.ticketSoldList) == self.ticketQuantity:
            return True
        return False

    def serviceCustomer(self, cust):
        behaviour = cust.getBehaviour()
        ticketId = self.ticketRegisterList[self.ptr]
        print("guest no:", self.ptr, "please go to the counter")
        self.greeting(cust, ticketId)
        name = cust.getName()
        print(name, " is coming for ", behaviour, "waiting for servicing ")
        cs = CustomerService(behaviour, ticketId, self.conn)
        cs.processingCustRequest()
        time.sleep(Util.getPauseSecond())
        cust.receiveTicket(ticketId)
        self.soldTicket(ticketId)

    def goingToClosed(self):
        closedProcedure = ClosedProcedure(self.conn)
        closedProcedure.forceToCloseUnsoldTicket()

    def getAllTicketsActivitiesWithoutNote(self):
        sqlStr = self.sqlSettingLoader.getSqlStatement("SELECT.R_TKT_ACTIVITY.ALLDATAWITHOUTNOTE")
        allDataList = self.ticketDao.selectTicketAllData(sqlStr)
        return allDataList

    def getAllTicketsActivitiesWithNote(self):
        sqlStr = self.sqlSettingLoader.getSqlStatement("SELECT.R_TKT_ACTIVITY.ALLDATAWITHNOTE")
        allDataList = self.ticketDao.selectTicketAllData(sqlStr)
        return allDataList

    def generateTicketActivitiesDataList(self):
        dataListWithoutNote = self.getAllTicketsActivitiesWithoutNote()
        dataListWithNote = self.getAllTicketsActivitiesWithNote()
        self.generateTicketList(dataListWithoutNote, self.ticketGen.getTicketDetailInfo)
        self.generateTicketList(dataListWithNote, self.ticketGen.getTicketNoteDict)

    def generateTicketList(self, dataList, func):
        for row in dataList:
            rowList = list(row)
            ticketId = rowList.pop(0)
            detailDict = func(rowList)
            ticketDict = self.ticketGen.getTicket(ticketId, self.employeeId, detailDict)
            self.activitiesDataList.append(ticketDict)

    def sortOutActivities(self):
        metadataDetailDict = self.ticketGen.getTicketMetadataDetailDict(self.ticketQuantity)
        return self.ticketGen.getTicketActivitiesDict(metadataDetailDict, self.activitiesDataList)
        
    def outputWholeTicketActivitiestoJsonFile(self, wholeTicketActivitiesDict):
        self.dao.closeConnection(self.conn)
        with open(self.outputFile, 'w') as f:
            json.dump(wholeTicketActivitiesDict, f)