from dataclasses import dataclass, field
from typing import Optional, List
import uuid

@dataclass
class ResponseFigure:
    description: Optional[str] = None
    xaxis_title: Optional[str] = None
    xaxis_value: Optional[str] = None
    yaxis_title: Optional[str] = None
    yaxis_value: Optional[str] = None

@dataclass
class ResponseCitation:
    content: Optional[str] = None

@dataclass
class ResponseAuthor:
    name: Optional[str] = None
    institution_name: Optional[str] = None
    institution_address: Optional[str] = None
    email: Optional[str] = None

@dataclass
class ResponseKeyword:
    content: Optional[str] = None

@dataclass
class ResponseArticle:
    guid: Optional[str] = None
    journal: Optional[str] = None
    doi: Optional[str] = None
    title: Optional[str] = None
    abstract: Optional[str] = None
    introduction: Optional[str] = None
    methodology: Optional[str] = None
    results: Optional[str] = None
    discussion: Optional[str] = None
    conclusion: Optional[str] = None
    keywords: Optional[str] = None
    user_input: Optional[str] = None
    prompt: Optional[str] = None
    citations: List[ResponseCitation] = field(default_factory=list)
    authors: List[ResponseAuthor] = field(default_factory=list)
    figures: List[ResponseAuthor] = field(default_factory=list)

    def __post_init__(self):
        if self.guid is None:
            self.guid = uuid.uuid4()

    def __repr__(self):
        return f"OllamaResponse(guid={self.guid}, title={self.title})"