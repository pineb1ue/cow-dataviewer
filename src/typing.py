from enum import Enum
from typing import Tuple


class Content(Enum):
    table = "table"
    images = "images"

    @classmethod
    def all(cls) -> Tuple[str]:
        return tuple(map(lambda c: c.value, cls))

    @staticmethod
    def from_str(v: str) -> "Content":
        for content in Content:
            if content.value == v:
                return content
        raise ValueError(f"invalid value: {v}")
