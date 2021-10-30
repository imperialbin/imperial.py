from dataclasses import dataclass
from typing import Union

from imperial.lib.common import camel_dict_to_snake
from imperial.lib.document.links import Links
from imperial.lib.document.settings import Settings
from imperial.lib.document.timestamps import Timestamps


@dataclass
class Document:
    id: str
    content: str
    creator: str
    views: int
    links: Union[Links, dict]
    timestamps: Union[Timestamps, dict]
    settings: Union[Settings, dict]

    def __post_init__(self):
        if not isinstance(self.links, Links):
            self.links = Links(self.id)
        if isinstance(self.timestamps, dict):
            self.timestamps = Timestamps(**self.timestamps)
        if isinstance(self.settings, dict):
            self.settings = Settings(**camel_dict_to_snake(self.settings))
