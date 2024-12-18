from dataclasses import dataclass, field
from typing import Optional, List

from services.db import db
from models.author import Author

# Author Repository
# This class is responsible for handling all database operations related to the Author model.
class AuthorRepository:
    @staticmethod
    def get_by_article_id(article_id: int) -> List[Author]:
   