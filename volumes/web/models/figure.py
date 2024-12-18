from dataclasses import dataclass
from typing import Optional, List
import uuid

@dataclass
class Figure:
    guid: Optional[str] = None
    number: Optional[int] = None   
    title: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    local: Optional[int] = 0
    xaxis_title: Optional[str] = None
    xaxis_value: Optional[int] = None
    yaxis_title: Optional[str] = None
    yaxis_value: Optional[int] = None
    figure_id: Optional[int] = None
    article_id: Optional[int] = None
    add_date: Optional[str] = None

    def __post_init__(self):
        if self.guid is None:
            self.guid = str(uuid.uuid4())

    def __repr__(self):
        return f"Figure(id={self.figure_id}, description={self.title})"
