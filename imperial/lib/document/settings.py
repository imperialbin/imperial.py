from dataclasses import dataclass, field
from typing import List


@dataclass
class Settings:
    language: str
    encrypted: bool
    password: str  # defaults to ""
    public: bool
    image_embed: bool
    instant_delete: bool
    editors: List[str] = field(default_factory=list)
