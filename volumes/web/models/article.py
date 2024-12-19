from dataclasses import dataclass, field
from typing import Optional, List
from .author import Author
from .citation import Citation
from .figure import Figure
from .image import Image
import uuid

# Article Model
@dataclass
class Article:
    guid: Optional[str] = None
    title: Optional[str] = None
    journal: Optional[str] = None
    doi: Optional[str] = None
    abstract: Optional[str] = None
    intro: Optional[str] = None 
    methodology: Optional[str] = None   
    results: Optional[str] = None  
    discussion: Optional[str] = None
    conclusion: Optional[str] = None
    article_id: Optional[int] = None
    user_input: Optional[str] = None
    prompt: Optional[str] = None
    add_date: Optional[str] = None
    authors: List[Author] = field(default_factory=list)
    citations: List[Citation] = field(default_factory=list)
    images: List[Image] = field(default_factory=list)
    figures: List[Figure] = field(default_factory=list)

    def __post_init__(self):
        if self.guid is None:
            self.guid = uuid.uuid4()

    def __repr__(self):
        return f"Article(id={self.article_id}, title={self.title})"

