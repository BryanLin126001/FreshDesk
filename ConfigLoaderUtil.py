import configparser

class ConfigSetting:
    configCfg = configparser.ConfigParser()
    
    
    def __init__(self):
        self.configCfg.read("config.cfg")
    
    def getSingleSettingString(self, section, key):
        return self.configCfg[section][key]

    def getPluralSettingList(self, section, partialKey, settingCount):
        settingList = []
        for i in range(1, settingCount + 1):
            settingList.append(self.configCfg[section][partialKey+'.'+ str(i)])
        return settingList

    def getStartAtDatetime(self):
        return self.getSingleSettingString("ticket_metadata_detail", "start.at")

    def getEndAtDatetime(self):
        return self.getSingleSettingString("ticket_metadata_detail", "end.at")

    def getTimezone(self):
        return self.getSingleSettingString("ticket_metadata_detail", "timezone")

    
class SqlSetting:
    sqlCfg = configparser.ConfigParser()
    
    def __init__(self):
        self.sqlCfg.read("sql.cfg")

    def getSqlStatement(self, key):
        return self.sqlCfg['sqlstatement'][key]
