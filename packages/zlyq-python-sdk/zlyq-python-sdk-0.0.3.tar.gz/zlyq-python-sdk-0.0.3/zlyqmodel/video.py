from dataclasses import dataclass, field
from typing import List


@dataclass
class VideoSyncInfo:
    title: str = ""
    userId: str = ""
    content: str = ""
    uploadType: int = ""
    orgFileName: str = ""
    os: int = 0
    deviceId: str = ""
    ip: str = ""
    longitude: float = 0
    latitude: float = 0
    audioId: int = 0
    source: int = 0
    thirdId: str = ""
    thirdExtra: str = ""
    createdAt: int = 0


@dataclass
class VideoSyncInfos:
    videos: List[VideoSyncInfo] = field(default_factory=list)

    def add(self, v):
        self.videos.append(v)

@dataclass
class VideoUploadInfo:
    video: bytes
    image: bytes
    title: str = ""
    userId: str = ""
    content: str = ""
    orgFileName: str = ""
    os: int = 0
    source: int = 0
    thirdId: str = ""
    thirdExtra: str = ""
