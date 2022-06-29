import random
from datetime import datetime
from pytz import timezone
from ConfigLoaderUtil import ConfigSetting


def lpad(length, inputStr, padStr):
    padLength = length - len(inputStr)
    return padStr * padLength + inputStr 

def getRandomNumber(startRange, endRange):
    return random.randrange(startRange, endRange)

def getRandomNumberWithoutStartRange(endRange):
    return random.randrange(1, endRange)

def getPauseSecond():
    return getRandomNumber(1,4) / getRandomNumber(4,8)

def getIsoFormatDatetimeWithTimezone():
    configSettingLoader = ConfigSetting()
    tZone = timezone(configSettingLoader.getSingleSettingString("ticket_metadata_detail", "timezone"))
    return datetime.now(tz=tZone).isoformat(' ', 'seconds')
    
def getNowWithTimezoneReturnDatetime():
    configSettingLoader = ConfigSetting()
    tZone = timezone(configSettingLoader.getSingleSettingString("ticket_metadata_detail", "timezone"))
    return datetime.now(tz=tZone)

def getNoteId():
    return getRandomNumber(1000000, 10000000)

def getDatetimeWithspecificDatetimeStr(datetimeStr):
    configSettingLoader = ConfigSetting()
    tZone = timezone(configSettingLoader.getSingleSettingString("ticket_metadata_detail", "timezone"))
    return datetime.astimezone(datetime.strptime(datetimeStr, "%Y-%m-%d %H:%M:%S"), tz=tZone)
