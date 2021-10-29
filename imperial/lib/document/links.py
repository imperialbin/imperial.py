from dataclasses import dataclass, InitVar, field

from imperial.lib.common import HOSTNAME


@dataclass
class Links:
    id: InitVar[str]
    raw: str = field(init=False)
    formatted: str = field(init=False)

    def __post_init__(self, id: str):
        self.raw = f"{HOSTNAME}/r/{id}"
        self.formatted = f"{HOSTNAME}/p/{id}"
