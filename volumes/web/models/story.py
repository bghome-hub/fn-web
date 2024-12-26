from dataclasses import dataclass, field
from typing import Optional, List

from .breakout import Breakout
from .quote import Quote

import uuid

@dataclass    
class Story:
    guid: Optional[str] = None
    headline: Optional[str] = None
    subheadline: Optional[str] = None
    journalist_name: Optional[str] = None
    journalist_bio: Optional[str] = None
    journalist_email: Optional[str] = None
    publication: Optional[str] = None
    publication_date: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None
    keywords: Optional[str] = None
    story_id: Optional[int] = None
    user_input: Optional[str] = None
    prompt: Optional[str] = None
    add_date: Optional[str] = None
    quotes: List[Quote] = field(default_factory=list)
    breakouts: List[Breakout] = field(default_factory=list)

    def __post_init__(self):
        if self.guid is None:
            self.guid = str(uuid.uuid4())

    def __repr__(self):
        return f"Story(headline={self.headline}, publication={self.publication})"
    