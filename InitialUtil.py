from DataAccessObj import DAO
from ConfigLoaderUtil import SqlSetting
from ConfigLoaderUtil import ConfigSetting
from datetime import datetime
from pytz import timezone
import os
import Util


class InitialData:
    sqlSettingLoader = SqlSetting()
    configSettingLoader = ConfigSetting()
    dataObj = DAO()
    
    def __init__(self):
        pass
    
    def InitialAllData(self):
        conn = self.dataObj.getConnection()
        try:
            self.initialTableRTktActivity(conn)
            self.initialTableRTktMetadata(conn)

        finally:
            self.dataObj.closeConnection(conn)

    def initialTableRTktActivity(self, conn):
        if self.isTableExist(conn, "R_TKT_ACTIVITY") == True:
            sqlStr = self.sqlSettingLoader.getSqlStatement("DELETE.R_TKT_ACTIVITY.DELETEALLDATA")
            self.clearTableData(conn, sqlStr)
        else:
            sqlStr = self.sqlSettingLoader.getSqlStatement("CREATE.TABLE.R_TKT_ACTIVITY")
            self.createTable(conn, sqlStr)
    
    def initialTableRTktMetadata(self, conn):
        if self.isTableExist(conn, "R_TKT_METADATA") == True:
            sqlStr = self.sqlSettingLoader.getSqlStatement("DELETE.R_TKT_METADATA.DELETEALLDATA")
            self.clearTableData(conn, sqlStr)
        else:
            sqlStr = self.sqlSettingLoader.getSqlStatement("CREATE.TABLE.R_TKT_METADATA")
            self.createTable(conn, sqlStr)
        sqlStr = self.sqlSettingLoader.getSqlStatement("INSERT.R_TKT_METADATA.DATETIMEINFO")
        self.setTimeForMetadata(conn, sqlStr)

    def createTable(self, conn, sqlStr):
        cur = self.dataObj.getCursor(conn)
        try:
            cur.execute(sqlStr)
        finally:
            self.dataObj.closeCursor(cur)

    def clearTableData(self, conn, sqlStr):
        cur = self.dataObj.getCursor(conn)
        try:
            cur.execute(sqlStr)
            conn.commit()
        finally:
            self.dataObj.closeCursor(cur)
    
    def isTableExist(self, conn, name):
        cur = self.dataObj.getCursor(conn)
        try:
            cur.execute(self.sqlSettingLoader.getSqlStatement("SELECT.SQLITE_MASTER.ISTABLEEXIST"), {"name": name})
            countTuple = cur.fetchone()
            count, = countTuple
            result = False
            if count == 1:
                result = True
        finally:
            self.dataObj.closeCursor(cur)
        return result
    
    def setTimeForMetadata(self, conn, sqlStr):
        startAtStr = self.configSettingLoader.getSingleSettingString("ticket_metadata_detail", "start.at")
        endAtStr = self.configSettingLoader.getSingleSettingString("ticket_metadata_detail", "end.at")
        start_dt = Util.getDatetimeWithspecificDatetimeStr(startAtStr)
        end_dt = Util.getDatetimeWithspecificDatetimeStr(endAtStr)
        cur = self.dataObj.getCursor(conn)
        try:
            cur.execute(sqlStr, (start_dt.strftime("%Y-%m-%d %H:%M:%S"), end_dt.strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()
        finally:
            self.dataObj.closeCursor(cur)

class FileClean:
    def __init__(self):
        pass
    
    @staticmethod
    def deleteOutputFile(fileStr):
        if os.path.exists(fileStr):
            os.remove(fileStr)
