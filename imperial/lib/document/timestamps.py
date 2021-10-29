from dataclasses import dataclass, InitVar
from datetime import datetime


@dataclass
class Timestamps:
    creation: InitVar[int]
    expiration: InitVar[int]

    def __post_init__(self, creation: int, expiration: int):
        self.creation: datetime = datetime.fromtimestamp(creation)
        self.expiration: datetime = datetime.fromtimestamp(expiration)
