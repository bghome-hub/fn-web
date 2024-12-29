from dataclasses import dataclass
from typing import Optional, List
from pydantic import BaseModel, Field

import uuid

class Quote(BaseModel):
    quote_id: Optional[int] = None
    guid: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    number: Optional[int] = None   
    description: Optional[str] = None
    content: Optional[str] = None
    speaker: Optional[str] = None
    story_id: Optional[int] = None
    add_date: Optional[str] = None

    def __repr__(self):
        return f"Quote(id={self.quote_id}, description={self.description})"
