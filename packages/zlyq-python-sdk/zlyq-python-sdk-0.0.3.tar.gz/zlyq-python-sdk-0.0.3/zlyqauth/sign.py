import time
import hashlib

def addSign(urlParams, appId, appSecret):
    urlParams['time'] = int(time.time() * 1000)
    urlParams['appId'] = appId

    keys = [key for key in urlParams.keys()]
    keys.sort()

    values = []
    for key in keys:
        values.append(key + '=' + str(urlParams[key]))

    string = "&".join(values)

    salt = appSecret
    signature = hashlib.md5((salt + "&" + string).encode(encoding='UTF-8')).hexdigest()

    return signature, string
