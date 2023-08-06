from dataclasses import dataclass
from typing import BinaryIO


@dataclass
class Image:
    image: bytes
    userId: str = ""
    description: str = ""
    source: int = 0
    thirdId: str = ""
    thirdExtra: str = ""
