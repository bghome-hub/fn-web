from dataclasses import dataclass
from typing import Optional, List
import uuid

@dataclass
class Breakout:
    breaout_id: Optional[int] = None
    guid: Optional[str] = None
    number: Optional[int] = None   
    title: Optional[str] = None
    content: Optional[str] = None
    story_id: Optional[int] = None
    add_date: Optional[str] = None

    def __post_init__(self):
        if self.guid is None:
            self.guid = str(uuid.uuid4())

    def __repr__(self):
        return f"Breakout(id={self.breaout_id}, description={self.title})"
