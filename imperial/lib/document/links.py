from dataclasses import dataclass

from imperial.lib.common import HOSTNAME


@dataclass(repr=False)
class Links:
    id: str

    def __post_init__(self):
        self.raw: str = f"{HOSTNAME}/r/{self.id}"
        self.formatted: str = f"{HOSTNAME}/p/{self.id}"

    def __repr__(self):
        return f"<{self.__class__.__name__} raw='/r/{self.id}' formatted='/p/{self.id}'>"
