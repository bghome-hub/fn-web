from dataclasses import dataclass, field
from typing import Optional, List

from models.author import Author
from services import db_service_article as article_db

# Author Repository
# This class is responsible for handling all database operations related to the Author model.
class AuthorRepository:
    @staticmethod
    def fetch_by_author_id(author_id: int) -> Optional[Author]:
        '''Fetches an author from the database by ID.'''
        conn = article_db.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE author_id = ?", (author_id,))
        row = cursor.fetchone()
        cursor.close()
        if row is None:
            return None

        return Author(
            author_id=row["author_id"],
            article_id=row["article_id"],
            guid=row["guid"],
            number=row["number"],
            name=row["name"],
            institution_name=row["institution_name"],
            institution_address=row["institution_address"],
            email=row["email"],
            add_date=row["add_date"]
        )
    
    @staticmethod
    def fetch_all_by_article_id(article_id: int) -> List[Author]:
        '''Fetches all authors for a given article.'''
        conn = article_db.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE article_id = ?", (article_id,))
        rows = cursor.fetchall()
        cursor.close()
        authors = []
        for row in rows:
            authors.append(Author(
                author_id=row["author_id"],
                article_id=row["article_id"],
                guid=row["guid"],
                number=row["number"],
                name=row["name"],
                institution_name=row["institution_name"],
                institution_address=row["institution_address"],
                email=row["email"],
                add_date=row["add_date"]
            ))
        return authors

    @staticmethod
    def fetch_all() -> List[Author]:
        '''Fetches all authors from the database.'''
        conn = article_db.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors")
        rows = cursor.fetchall()
        cursor.close()
        authors = []
        for row in rows:
            authors.append(Author(
                author_id=row["author_id"],
                article_id=row["article_id"],
                guid=row["guid"],
                number=row["number"],
                name=row["name"],
                institution_name=row["institution_name"],
                institution_address=row["institution_address"],
                email=row["email"],
                add_date=row["add_date"]
            ))
        return authors

    @staticmethod
    def insert(author: Author) -> int:
        '''Inserts an author into the database.'''
        conn = article_db.connect_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO authors (article_id, guid, number, name, institution_name, institution_address, email)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            author.article_id,
            author.guid,
            author.number,
            author.name,
            author.institution_name,
            author.institution_address,
            author.email
        ))
        conn.commit()
        author_id = cursor.lastrowid
        cursor.close()
        return author_id
    
    @staticmethod
    def update(author: Author) -> None:
        '''Updates an author in the database.'''
        conn = article_db.connect_db()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE authors SET article_id = ?, guid = ?, number = ?, name = ?, institution_name = ?, institution_address = ?, email = ?
            WHERE author_id = ?
        ''', (
            author.article_id,
            author.guid,
            author.number,
            author.name,
            author.institution_name,
            author.institution_address,
            author.email,
            author.author_id
        ))
        conn.commit()
        cursor.close()
   
    @staticmethod
    def delete(author_id: int) -> None:
        '''Deletes an author from the database.'''
        conn = article_db.connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM authors WHERE author_id = ?", (author_id,))
        conn.commit()
        cursor.close()

    