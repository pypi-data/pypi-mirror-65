from dataclasses import dataclass, field
from typing import List


@dataclass
class ArticleSyncInfo:
    title: str = ""
    userId: str = ""
    content: str = ""
    h5content: str = ""
    os: int = 0
    deviceId: str = ""
    ip: str = ""
    longitude: float = 0
    latitude: float = 0
    source: int = 0
    thirdId: str = ""
    thirdExtra: str = ""
    createdAt: int = 0
    mediaType: int = 2


@dataclass
class ArticleSyncInfos:
    articles: List[ArticleSyncInfo] = field(default_factory=list)

    def add(self, a):
        self.articles.append(a)


@dataclass
class ArticleUploadInfo:
    coverIds: List[str]
    galleryIds: List[str]
    title: str
    content: str
    os: int
    source: int
    mediaType: int
    h5content: str
    userId: str = ""
    thirdId: str = ""
    thirdExtra: str = ""
