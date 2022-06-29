import Properties
from ConfigLoaderUtil import ConfigSetting
from ConfigLoaderUtil import SqlSetting
from DataAccessObj import TicketDAO
from ActivityInfo import Ticket
import time
import Util
import EmptyClass

class CustomerService:
    configSettingLoader = ConfigSetting()
    sqlSettingLoader = SqlSetting()
    ticketDao = EmptyClass.Empty()
    custReq = ""
    ticketId = 0
    #pendingCaseList = []

    def __init__(self, custReq, ticketId, conn):
        self.custReq = custReq
        self.ticketId = ticketId
        self.ticketDao = TicketDAO(conn)

    def processingCustRequest(self):
        if self.custReq == "purchase":
            self.processingPurchase()
        elif self.custReq == "refund":
            self.processingRefund()
        elif self.custReq == "booking":
            self.processingBooking()
        elif self.custReq == "exchange":
            self.processingExchange()
    
    def processingPurchase(self):
        print("Purchase ticket, processing...")
        status = Properties.Status.open
        timeSpentOpen = self.configSettingLoader.getSingleSettingString("ticketinfo", "ticket.time.spent.open")
        group = self.custReq
        sqlStr = self.sqlSettingLoader.getSqlStatement("UPDATE.R_TKT_ACTIVITY.PURCHASETICKET")
        valueList = [status, group, str(timeSpentOpen), self.ticketId, sqlStr]
        self.ticketDao.updateTicketBaseOnCustReq(valueList)
        time.sleep(Util.getPauseSecond())
        if self.isMalfunctionHappens() == True:
            self.noteTicketWhenMalFunctionHappens()
            time.sleep(Util.getPauseSecond())

    def processingRefund(self):
        print("Refund ticket, processing...")
        status = Properties.Status.closed
        issueType = Properties.IssueType.incident
        priority = Properties.Priority.veryUrgent
        group = self.custReq
        sqlStr = self.sqlSettingLoader.getSqlStatement("UPDATE.R_TKT_ACTIVITY.REFUNDTICKET")
        valueList = [status, group, issueType, priority, self.ticketId, sqlStr]
        self.ticketDao.updateTicketBaseOnCustReq(valueList)
        time.sleep(Util.getPauseSecond())

    def processingBooking(self):
        print("Booking ticket, processing...")
        status = Properties.Status.resolved
        priority = Properties.Priority.urgent
        contactedCustomer = False
        group = self.custReq
        sqlStr = self.sqlSettingLoader.getSqlStatement("UPDATE.R_TKT_ACTIVITY.BOOKINGTICKET")
        valueList = [status, group,contactedCustomer, priority, self.ticketId, sqlStr]
        self.ticketDao.updateTicketBaseOnCustReq(valueList)
        time.sleep(Util.getPauseSecond())
        if self.isMalfunctionHappens() == True:
            self.noteTicketWhenMalFunctionHappens()
            time.sleep(Util.getPauseSecond())

    def processingExchange(self):
        print("Exchanging ticket, processing...")
        status = Properties.Status.waitingForThirdParty
        group = self.custReq
        product = Properties.Product.paper
        category = Properties.Category.thirdParty
        sqlStr = self.sqlSettingLoader.getSqlStatement("UPDATE.R_TKT_ACTIVITY.EXCHANGINGTICKET")
        valueList = [status, group, category, product, self.ticketId, sqlStr]
        self.ticketDao.updateTicketBaseOnCustReq(valueList)
        time.sleep(Util.getPauseSecond())
        self.processingPending()
        print("It will cost a little bit of time, please wait...")
        time.sleep(Util.getPauseSecond())
        self.closingPendingCase()
        
    def noteTicketWhenMalFunctionHappens(self):
        print("MalFunction Happens, note ticket id: ", self.ticketId)
        noteId = Util.getNoteId()
        noteType = Properties.NoteType.malfunction
        sqlStr = self.sqlSettingLoader.getSqlStatement("UPDATE.R_TKT_ACTIVITY.NOTETICKETID")
        valueList = [noteId, noteType, self.ticketId, sqlStr]
        self.ticketDao.updateTicketBaseOnCustReq(valueList)
        time.sleep(Util.getPauseSecond())

    def processingPending(self):  
        print("Waiting for checking, pending...")
        status = Properties.Status.penging
        pendingStartDatetime = Util.getNowWithTimezoneReturnDatetime().strftime("%Y-%m-%d %H:%M:%S.%f")
        sqlStr = self.sqlSettingLoader.getSqlStatement("UPDATE.R_TKT_ACTIVITY.PENDINGTICKET")
        valueList = [status, pendingStartDatetime, self.ticketId, sqlStr]
        self.ticketDao.updateTicketBaseOnCustReq(valueList)
        time.sleep(Util.getPauseSecond())

    def closingPendingCase(self):
        print("Closing pending case...")
        status = Properties.Status.open
        pendingEndtime = Util.getNowWithTimezoneReturnDatetime().strftime("%Y-%m-%d %H:%M:%S.%f")
        timeSpentOpen = self.configSettingLoader.getSingleSettingString("ticketinfo", "ticket.time.spent.open")
        sqlStr = self.sqlSettingLoader.getSqlStatement("UPDATE.R_TKT_ACTIVITY.CLOSEPENDINGCASE")
        print("pending case ticket id: ", self.ticketId)
        valueList = [status, pendingEndtime, str(timeSpentOpen), self.ticketId,  sqlStr]
        self.ticketDao.updateTicketBaseOnCustReq(valueList)
        time.sleep(Util.getPauseSecond())

    def isMalfunctionHappens(self):
        if Util.getRandomNumber(1,6) == 1:
            return True
        return False

class ClosedProcedure:
    ticketDao = EmptyClass.Empty()
    sqlSettingLoader = SqlSetting()
    def __init__(self, conn):
        self.ticketDao = TicketDAO(conn)

    def forceToCloseUnsoldTicket(self):
        print("Force to close unsold ticket...")
        sqlStr = self.sqlSettingLoader.getSqlStatement("UPDATE.R_TKT_ACTIVITY.CLOSEUNSOLDTICKET")
        beforeStatus = Properties.Status.waitingForCustomer
        afterStatus = Properties.Status.closed
        valueList = [afterStatus, beforeStatus, sqlStr]
        self.ticketDao.updateTicketBaseOnCustReq(valueList)
        time.sleep(Util.getPauseSecond())