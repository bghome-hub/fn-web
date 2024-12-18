from dataclasses import dataclass
from typing import Optional, List

from services.db import db 
from models.figure import Figure

# Figure Repository
# This class is responsible for handling all database operations related to the Figure model.
class FigureRepository:
    @staticmethod
    def get_by_article_id(article_id: int) -> List[Figure]:
      