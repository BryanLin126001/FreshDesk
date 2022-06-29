class Status:
    open = "Open"
    closed = "Closed"
    resolved = "Resolved"
    waitingForCustomer = "Waiting for Customer"
    waitingForThirdParty = "Waiting for Third Party"
    penging = "Pending"

class IssueType:
    incident = "Incident"
    normal = "Normal"

class Priority:
    normal = 3
    urgent = 4
    veryUrgent = 5

class Source:
    freshdesk = 3
    thirdParty = 4

class Product:
    mobile = "mobile"
    paper = "paper"

class Category:
    phone = "Phone"
    thirdParty = "Third Party"

class PerformerType:
    user = "user"

class NoteType:
    malfunction = 4

class Employee:
    employeeId_1 = 149018

    def getEmployeeList(self):
        employeeList = []
        employeeList.append(self.employeeId_1)

class Counter:
    pos_1 = 145423

    def getPosList(self):
        posList = []
        posList.append(self.pos_1)

class People:
    name = ['Andy'
    , 'Brooks'
    , 'Carter'
    , 'Dalton'
    , 'Elliston'
    , 'Finch'
    , 'Gerrell'
    , 'Hayden'
    , 'Ian'
    , 'Jay'
    , 'Kevin'
    , 'Lucas'
    , 'Mars'
    , 'Neo'
    , 'Oliver'
    , 'Peter'
    , 'Quinn'
    , 'Ryan'
    , 'Stvevn'
    , 'Tim'
    , 'Umar'
    , 'Vander'
    , 'Wayne'
    , 'Xanto'
    , 'Yves'
    , 'Zac'
    , 'Ada'
    , 'Bela'
    , 'Celine'
    , 'Doris'
    , 'Ella'
    , 'Fifi'
    , 'Gina'
    , 'Helen'
    , 'Ivy'
    , 'Judy'
    , 'Kay'
    , 'Lara'
    , 'May'
    , 'Nata'
    , 'Orea'
    , 'Peggy'
    , 'Qing'
    , 'Ren'
    , 'Sandra'
    , 'Tani'
    , 'Uri'
    , 'Valli'
    , 'Wendy'
    , 'Xena'
    , 'Yani'
    , 'Zali']