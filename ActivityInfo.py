from ConfigLoaderUtil import ConfigSetting
from datetime import datetime
from pytz import timezone 
import Util
import Properties
from datetime import date

class Ticket:
    configSettingLoader = ConfigSetting()
    def __init__(self):
        pass
    
    def getTicketActivitiesDict(self, ticketMetadataDetailDict, activitiesDataList):
        ticketActivitiesKeyList = self.getKeyList("ticket_activities", "key", 2)
        ticketActivitieslDict = self.getFormedDict(ticketActivitiesKeyList)
        ticketActivitieslDict[ticketActivitiesKeyList[0]] = ticketMetadataDetailDict
        ticketActivitieslDict[ticketActivitiesKeyList[1]] = activitiesDataList
        return ticketActivitieslDict

    def getTicketMetadataDetailDict(self, activitiesCount):
        ticketMetadataKeyList = self.getKeyList("ticket_metadata_detail", "key", 3)
        ticketMetadataDetailDict = self.getFormedDict(ticketMetadataKeyList)
        startAtStr = self.configSettingLoader.getSingleSettingString("ticket_metadata_detail", "start.at")
        endAtStr = self.configSettingLoader.getSingleSettingString("ticket_metadata_detail", "end.at")
        ticketMetadataDetailDict[ticketMetadataKeyList[0]] = Util.getDatetimeWithspecificDatetimeStr(startAtStr).strftime("%d-%m-%Y %H:%M:%S %z")
        ticketMetadataDetailDict[ticketMetadataKeyList[1]] = Util.getDatetimeWithspecificDatetimeStr(endAtStr).strftime("%d-%m-%Y %H:%M:%S %z")
        ticketMetadataDetailDict[ticketMetadataKeyList[2]] = activitiesCount
        return ticketMetadataDetailDict

    
    def getTicket(self, ticketId, employeeId, ticketDetailDict):
        ticketKeyList = self.getKeyList("ticket_header", "key", 5)
        ticketDict = self.getFormedDict(ticketKeyList)
        ticketDict[ticketKeyList[0]] = Util.getNowWithTimezoneReturnDatetime().strftime("%d-%m-%Y %H:%M:%S %z")
        ticketDict[ticketKeyList[1]] = ticketId
        ticketDict[ticketKeyList[2]] = self.configSettingLoader.getSingleSettingString("performertype", "performertype.1")
        ticketDict[ticketKeyList[3]] = employeeId
        ticketDict[ticketKeyList[4]] = ticketDetailDict
        return ticketDict

    def getTicketDetailInfo(self, ticketDetailInfofromCust):
        ticketDetailKeyList = self.getKeyList("ticket_body", "key", 12)
        ticketDetailDict = self.getFormedDict(ticketDetailKeyList)
        for i in range(12):
            ticketDetailDict[ticketDetailKeyList[i]] = ticketDetailInfofromCust[i]
        key = self.configSettingLoader.getSingleSettingString("ticket_body", "key.4")
        ticketDetailDict[key] = self.convertContactedCustomerValue(ticketDetailDict[key])
        return ticketDetailDict

    def convertContactedCustomerValue(self, value):
        if value == 1:
            return True
        return False
    
    def getTicketNoteDict(self, noteList):
        noteKeyList = self.getKeyList("notetype", "note.key", 2)
        noteContectDict = self.getFormedDict(noteKeyList)
        for i in range(2):
            noteContectDict[noteKeyList[i]] = noteList[i]
        noteDict = {"note" : noteContectDict}
        return noteDict

    def getFormedDict(self, keyList):
        formedDict = {}
        for value in keyList:
            formedDict[value] = ""
        return formedDict

    def getKeyList(self,section, partialKeyName, settingCount):
        keyList = self.configSettingLoader.getPluralSettingList(section, partialKeyName, settingCount)
        return keyList

    def getDefaultTicketDetailInfo(self, dateStr, employeeId, posId):
        ticketDetailKeyList = self.getKeyList("ticket_body", "key", 12)
        ticketDefalutDetailDict = self.getFormedDict(ticketDetailKeyList)
        ticketDefalutDetailDict["shipping_address"] = self.notApplicable()
        ticketDefalutDetailDict["shipment_date"] = dateStr
        ticketDefalutDetailDict["category"] = self.getDefaultCategory()
        ticketDefalutDetailDict["contacted_customer"] = self.getDefaultContactedCustomer()
        ticketDefalutDetailDict["issue_type"] = self.getDefaultIssueType()
        ticketDefalutDetailDict["source"] = self.getDefaultSource()
        ticketDefalutDetailDict["status"] = Properties.Status.waitingForCustomer
        ticketDefalutDetailDict["priority"] = self.getDefaultPriority()
        ticketDefalutDetailDict["group"] = self.notApplicable()
        ticketDefalutDetailDict["agent_id"] = employeeId
        ticketDefalutDetailDict["requester"] = posId
        ticketDefalutDetailDict["product"] = self.getDefaultProduct()
        return ticketDefalutDetailDict

    def notApplicable(self):
        return "N/A"

    def getDefaultCategory(self):
        return Properties.Category.phone

    def getDefaultContactedCustomer(self):
        return True
    
    def getDefaultIssueType(self):
        return Properties.IssueType.normal

    def getDefaultSource(self):
        return Properties.Source.freshdesk

    def getDefaultStatus(self):
        return Properties.Status.open

    def getDefaultPriority(self):
        return Properties.Priority.normal
        
    def getDefaultProduct(self):
        return Properties.Product.mobile

    def updateTicketDetailInfoBySpecificKey(self, dictInfo, key, value):
        dictInfo[key] = value 
        return dictInfo