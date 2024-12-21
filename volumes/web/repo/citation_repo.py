from dataclasses import dataclass
from typing import Optional, List

from models.citation import Citation
from services import db_service as db

# Citation Repository
# This class is responsible for handling all database operations related to the Citation model.
class CitationRepository:
    @staticmethod
    def fetch_by_citation_id(citation_id: int) -> Optional[Citation]:
        '''Fetches a citation from the database by ID.'''
        conn = db.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM citations WHERE citation_id = ?", (citation_id,))
        row = cursor.fetchone()
        cursor.close()
        if row is None:
            return None

        return Citation(
            citation_id=row["citation_id"],
            article_id=row["article_id"],
            guid=row["guid"],
            number=row["number"],
            content=row["content"],
            add_date=row["add_date"]
        )

    @staticmethod
    def fetch_all_by_article_id(article_id: int) -> List[Citation]:
        '''Fetches all citations for a given article.'''
        conn = db.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM citations WHERE article_id = ?", (article_id,))
        rows = cursor.fetchall()
        cursor.close()
        citations = []
        for row in rows:
            citations.append(Citation(
                citation_id=row["citation_id"],
                article_id=row["article_id"],
                guid=row["guid"],
                number=row["number"],
                content=row["content"],
                add_date=row["add_date"]
            ))
        return citations
    
    @staticmethod
    def fetch_all() -> List[Citation]:
        '''Fetches all citations from the database.'''
        conn = db.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM citations")
        rows = cursor.fetchall()
        cursor.close()
        citations = []
        for row in rows:
            citations.append(Citation(
                citation_id=row["citation_id"],
                article_id=row["article_id"],
                guid=row["guid"],
                number=row["number"],
                content=row["content"],
                add_date=row["add_date"]
            ))
        return citations
    
    @staticmethod
    def insert(citation: Citation) -> None:
        '''Inserts a new citation into the database.'''
        conn = db.connect_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO citations (article_id, guid, number, content)
            VALUES (?, ?, ?, ?)'''
        , (
            citation.article_id,
            citation.guid,
            citation.number,
            citation.content
        ))

        conn.commit()
        cursor.close()

    @staticmethod
    def update(citation: Citation) -> None:
        '''Updates an existing citation in the database.'''
        conn = db.connect_db()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE citations
            SET article_id = ?, guid = ?, number = ?, content = ?
            WHERE citation_id = ?
        ''', (
            citation.article_id,
            citation.guid,
            citation.number,
            citation.content,
            citation.citation_id
        ))
        conn.commit()
        cursor.close()

    @staticmethod
    def delete(citation_id: int) -> None:
        '''Deletes a citation from the database by ID.'''
        conn = db.connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM citations WHERE citation_id = ?", (citation_id,))
        conn.commit()
        cursor.close()


