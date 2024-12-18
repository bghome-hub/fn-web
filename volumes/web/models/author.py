from dataclasses import dataclass, field
from typing import Optional, List
import uuid


# Author Model
@dataclass
class Author:
    guid: Optional[str] = None
    number: Optional[int] = None
    name: Optional[str] = None
    institution_name: Optional[str] = None
    institution_address: Optional[str] = None
    email: Optional[str] = None
    author_id: Optional[int] = None
    article_id: Optional[int] = None
    add_date: Optional[str] = None

    def __post_init__(self):
        if self.guid is None:
            self.guid = str(uuid.uuid4())

    def __repr__(self):
        return f"Author(id={self.author_id}, name={self.name})"
