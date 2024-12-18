from dataclasses import dataclass
from typing import Optional, List

from models.citation import Citation
from services.db import db

# Citation Repository
# This class is responsible for handling all database operations related to the Citation model.
class CitationRepository:
    @staticmethod
    def get_by_article_id(article_id: int) -> List[Citation]:
        rows = db.get_citations_by_article_id(article_id)
       
