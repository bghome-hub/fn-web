from dataclasses import dataclass
from typing import Optional, List

import uuid

@dataclass    
class Citation:
    guid: Optional[str] = None
    number: Optional[int] = None
    content: Optional[str] = None
    citation_id: Optional[int] = None
    article_id: Optional[int] = None
    add_date: Optional[str] = None

    def __post_init__(self):
        if self.guid is None:
            self.guid = str(uuid.uuid4())

    def __repr__(self):
        return f"Citation(id={self.citation_id}, content={self.content})"
    