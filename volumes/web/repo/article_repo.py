from typing import List, Optional
from dataclasses import dataclass

# Model Imports
from models.article import Article
from services.db import db 

# Article Repository 
# This class is responsible for handling all database operations related to the Article model.
class ArticleRepository:
    @staticmethod
    def fetch_from_db(article_id: int) -> Optional[Article]:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE id = ?", (article_id,))
        row = cursor.fetchone()
        cursor.close()
        if row is None:
            return None

        return Article(
            article_id=row["article_id"],
            guid=row["guid"],
            title=row["title"],
            journal=row["journal"],
            doi=row["doi"],
            abstract=row["abstract"],
            intro=row["intro"],
            methodology=row["methodology"],
            results=row["results"],
            discussion=row["discussion"],
            conclusion=row["conclusion"],
            prompt=row["prompt"],
            user_input=row["user_input"],
            add_date=row["add_date"]
        )
    

    
    def insert(article: Article) -> int:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO articles (guid, prompt, user_input, title, journal, doi, abstract, intro, methodology, results, discussion, conclusion)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            article.guid,
            article.prompt,
            article.user_input,
            article.title,
            article.journal,
            article.doi,
            article.abstract,
            article.intro,
            article.methodology,
            article.results,
            article.discussion,
            article.conclusion
        ))
        conn.commit()
        cursor.close()
        return cursor.lastrowid
    
    def update(article: Article) -> None:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE articles
            SET guid = ?, prompt = ?, user_input = ?, title = ?, journal = ?, doi = ?, abstract = ?, intro = ?, methodology = ?, results = ?, discussion = ?, conclusion = ?
            WHERE article_id = ?
        ''', (
            article.guid,
            article.prompt,
            article.user_input,
            article.title,
            article.journal,
            article.doi,
            article.abstract,
            article.intro,
            article.methodology,
            article.results,
            article.discussion,
            article.conclusion,
            article.article_id
        ))
        conn.commit()
        cursor.close()

    def delete(article_id: int) -> None:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM articles
            WHERE article_id = ?
        ''', (article_id,))
        conn.commit()
        cursor.close()

    def fetch_all() -> List[Article]:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM articles')
        rows = cursor.fetchall()
        cursor.close()
        return [
            Article(
                article_id=row["article_id"],
                guid=row["guid"],
                title=row["title"],
                journal=row["journal"],
                doi=row["doi"],
                abstract=row["abstract"],
                intro=row["intro"],
                methodology=row["methodology"],
                results=row["results"],
                discussion=row["discussion"],
                conclusion=row["conclusion"],
                prompt=row["prompt"],
                user_input=row["user_input"],
                add_date=row["add_date"]
            )
            for row in rows
        ]
    
    