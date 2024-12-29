from dataclasses import dataclass, field
from typing import Optional, List
from pydantic import BaseModel, Field

from .breakout import Breakout
from .quote import Quote

import uuid

class Story(BaseModel):
    guid: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    headline: Optional[str] = None
    subheadline: Optional[str] = None
    journalist_name: Optional[str] = None
    journalist_bio: Optional[str] = None
    journalist_email: Optional[str] = None
    journalist_photo: Optional[str] = None
    publication: Optional[str] = None
    publication_date: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None
    keywords: Optional[str] = None
    photo_url: Optional[str] = None
    story_id: Optional[int] = None
    user_input: Optional[str] = None
    prompt: Optional[str] = None
    add_date: Optional[str] = None
    quotes: List[Quote] = Field(default_factory=list) 
    breakouts: List[Breakout] = Field(default_factory=list)

    def __repr__(self):
        return f"Story(headline={self.headline}, publication={self.publication})"
    