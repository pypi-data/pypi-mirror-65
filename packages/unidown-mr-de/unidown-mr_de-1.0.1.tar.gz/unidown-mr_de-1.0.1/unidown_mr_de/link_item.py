from __future__ import annotations

from datetime import datetime

from unidown.plugin import LinkItem

from unidown_mr_de.tools import sizeof_fmt


class MrLinkItem(LinkItem):
    """
    Own link item with additional size and type information.
    """
    def __init__(self, name: str, time: datetime, type: str, size: int):
        super().__init__(name, time)
        self.type: str = type
        self.size: int = size

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"({self._name}, {self._time} - {self.type}, {sizeof_fmt(self.size)})"
