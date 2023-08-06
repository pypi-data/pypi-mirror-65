from dataclasses import dataclass, field
from typing import List


@dataclass
class MediaLike:
    mediaId: str = ""
    userId: str = ""
    createdAt: int = 0


@dataclass
class MediaLikes:
    mediaLikes: List[MediaLike] = field(default_factory=list)

    def add(self, m):
        self.mediaLikes.append(m)


@dataclass
class MediaFavorite:
    mediaId: str = ""
    userId: str = ""
    createdAt: int = 0


@dataclass
class MediaFavorites:
    mediaFavorites: List[MediaFavorite] = field(default_factory=list)

    def add(self, m):
        self.mediaFavorites.append(m)


@dataclass
class Comment:
    mediaId: str = ""
    userId: str = ""
    createdAt: int = 0
    content: str = ""
    thirdId: str = ""


@dataclass
class Comments:
    comments: List[Comment] = field(default_factory=list)

    def add(self, m):
        self.comments.append(m)


@dataclass
class CommentLike:
    mediaId: str = ""
    userId: str = ""
    createdAt: int = 0
    commentId: str = ""


@dataclass
class CommentLikes:
    commentLikes: List[CommentLike] = field(default_factory=list)

    def add(self, m):
        self.commentLikes.append(m)
