### 中量引擎服务端SDK (Python)

##### 安装方法
```
pip install zlyq-python-sdk
```

##### 中量引擎官方文档
```
https://wiki.zplatform.cn/
```

##### SDK说明
本SDK封装了向中量引擎服务同步用户数据、媒资数据及用户历史交互数据的方法

##### 接口调用示例
同步用户信息
```
from zlyqsync.client import SyncClient
from zlyqmodel.user import UserInfo

# 同步用户数据
userClient = SyncClient("f1edf8b4ff55610c129dc1626e6dd71f", "7de548e902debd7ca6aac1f5c6ec802e", 402918291821943819, "http://testappapi.zplatform.cn")

userInfo = UserInfo()
userInfo.thirdId = '51982'
userInfo.udid = "ABC"
userInfo.nickname = "test name"
userInfo.gender = 1
userInfo.account = "xiaoming"
userInfo.avatar = "http://www.baidu.com"
userInfo.phone = "10000000000"

print(userClient.userInfoSynchronize(userInfo))
```

同步用户历史交互信息
```
from zlyqsync.client import SyncClient
from zlyqmodel.history import TrackInfo, TrackCommon, TrackLike, TrackFinishVideo

trackClient = SyncClient("f1edf8b4ff55610c129dc1626e6dd71f", "7de548e902debd7ca6aac1f5c6ec802e", 402918291821943819, "http://testtrackapi.zplatform.cn")

trackCommon = TrackCommon()
trackCommon.udid = "AKDHA-KAJFO-KA81K-9HQ1L"
trackCommon.userId = 404910192718291827
trackCommon.distinctId = 409181916271928172 
trackCommon.appId = 402918291821943819 
trackCommon.platform =  
trackCommon.time = 1585239477000 
trackCommon.screenHeight = 670 
trackCommon.screenWidth = 375   
trackCommon.manufacturer = "huawei"
trackCommon.network = 4
trackCommon.os = 2        
trackCommon.osVersion = 11.2.4         
trackCommon.ip = 212.29.35.12    
trackCommon.country = "中国"           
trackCommon.province = "北京"    
trackCommon.city = "北京"   
trackCommon.carrier = 电信
trackLike = TrackLike()
trackLike.event = "like"
trackLike.contentId = 401929181919011928
trackLike.contentType = 1
trackFinishVideo = TrackFinishVideo()
trackFinishVideo.event = "finishVideo"
trackFinishVideo.contentId = 40192918191901
trackFinishVideo.contentType = 1
trackFinishVideo.videoTime = 15
trackFinishVideo.duration = 10
trackFinishVideo.isFinish = 0

properties = [trackLike, trackFinishVideo]

trackInfo = TrackInfo()
trackInfo.common = trackCommon
trackInfo.properties = properties

print(trackClient.historySynchronize(trackInfo))
```
