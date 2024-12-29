from dataclasses import dataclass
from typing import Optional, List
from pydantic import BaseModel, Field
import uuid

class Breakout(BaseModel):
    breakout_id: Optional[int] = None
    guid: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    number: Optional[int] = None   
    title: Optional[str] = None
    content: Optional[str] = None
    story_id: Optional[int] = None
    add_date: Optional[str] = None

    def __repr__(self):
        return f"Breakout(id={self.title})"
