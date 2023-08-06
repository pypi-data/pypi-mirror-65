from dataclasses import dataclass

@dataclass
class UserInfo:
    thirdId      :       str   = ""
    account      :       str   = ""
    nickname     :       str   = ""
    avatar       :       str   = ""
    gender       :       int   = 0
    birthday     :       int   = 0
    signature    :       str   = ""
    region       :       str   = ""
    extraInfo    :       str   = ""
    createdAt    :       int   = 0
    updatedAt    :       int   = 0
    loginTime    :       int   = 0
    isRobot      :       int   = 0
    status       :       int   = 0
    avatarStorage:       bool  = False
    phone        :       str   = ""
    deviceId     :       str   = ""
    deviceType   :       str   = ""

