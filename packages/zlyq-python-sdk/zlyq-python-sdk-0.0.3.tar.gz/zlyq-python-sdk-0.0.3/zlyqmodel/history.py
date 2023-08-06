from dataclasses import dataclass
from typing import List

@dataclass
class TrackCommon():
    udid               : str = ""     
    userId             : int = 0
    distinctId         : int = 0 
    appId              : int = 0
    platform           : str = ""
    time               : int = 0 
    iosSdkVersions     : str = ""
    androidSdkVersions : str = ""
    screenHeight       : int = 0
    screenWidth        : int = 0
    manufacturer       : str = ""
    network            : int = 0
    os                 : int = 0
    osVersion          : str = ""
    ip                 : str = ""
    country            : str = ""
    province           : str = ""
    city               : str = ""
    carrier            : str = ""
    utmSource          : str = ""
    utmMedia           : str = ""
    utmCampaign        : str = ""
    utmContent         : str = ""
    utmTerm            : str = ""
    appVersion         : str = ""

@dataclass
class EventCommon():
    event        : str = ""
    eventTime    : int = 0
    feedConfigId : str = ""
    requestId    : str = ""
    abtestIds    : str = ""

@dataclass
class TrackInfo():
    common:TrackCommon = None
    properties:List[EventCommon] = None

@dataclass
class TrackRegister(EventCommon):
    methord      : int = 0
    isSuccess    : int = 0
    failReason   : str = ""

@dataclass
class TrackLogin(EventCommon):
    methord      : int = 0
    isSuccess    : int = 0
    failReason   : str = ""

@dataclass
class TrackFinishVideo(EventCommon):
    methord      : int = 0
    contentId    : int = 0
    contentType  : int = 0
    videoTime    : int = 0
    duration     : int = 0
    isFinish     : int = 0

@dataclass
class TrackLike(EventCommon):
    contentId    : int = 0
    contentType  : int = 0

@dataclass
class TrackDisLike(EventCommon):
    contentId    : int = 0
    contentType  : int = 0

@dataclass
class TrackFollow(EventCommon):
    contentId    : int = 0
    contentType  : int = 0
    authorId     : int = 0

@dataclass
class TrackComment(EventCommon):
    contentId    : int = 0
    contentType  : int = 0

@dataclass
class TrackLikeComment(EventCommon):
    contentId    : int = 0
    contentType  : int = 0
    commentId    : int = 0

@dataclass
class TrackDislikeComment(EventCommon):
    contentId    : int = 0
    contentType  : int = 0
    commentId    : int = 0



if __name__ == "__main__":
    trackCommon = TrackCommon()
    print(trackCommon)

    trackRegister = TrackRegister()
    print(trackRegister)

    properties = [trackRegister]
    
    trackInfo = TrackInfo()
    trackInfo.common = trackCommon
    trackInfo.properties = properties
    print(trackInfo)



