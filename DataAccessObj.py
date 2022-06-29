import sqlite3
from ConfigLoaderUtil import SqlSetting
import Properties
import EmptyClass


class DAO:
    sqlSettingLoader = SqlSetting()
    def __init__(self):
        pass
    
    
    def getConnection(self):
        conn = sqlite3.connect(self.sqlSettingLoader.getSqlStatement("DATABASE.NAME"))
        return conn

    def getCursor(self, conn):
        cur = conn.cursor()
        return cur

    def closeCursor(self, cur):
        cur.close()

    def closeConnection(self, conn):
        conn.close()

class TicketDAO:
    dataObj = DAO()
    #conn = dataObj.getConnection()
    conn = EmptyClass.Empty()
    sqlSettingLoader = SqlSetting()

    def __init__(self, conn):
       self.conn = conn

    def updateTicketBaseOnCustReq(self, valueList):
        cur = self.dataObj.getCursor(self.conn)
        sqlStr = valueList.pop()
        try:
            cur.execute(sqlStr, valueList)
            self.conn.commit()
        finally:
            self.dataObj.closeCursor(cur)
    
    def selectTicketAllData(self, sqlStr):
        cur = self.dataObj.getCursor(self.conn)
        try:
            cur.execute(sqlStr)
            rows = cur.fetchall()
        finally:
            self.dataObj.closeCursor(cur)
        return rows
    
    def closeConnection(self):
        self.dataObj.closeConnection(self.conn)