import hashlib
import time

def addAppToken(appKey, appSecret):
    timeStr = time.strftime('%Y-%m-%d %H:%M',time.localtime(time.time()))
    string = appKey + appSecret + timeStr
    signature = hashlib.md5(string.encode(encoding='UTF-8')).hexdigest() 

    return signature
