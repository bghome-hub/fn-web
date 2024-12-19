from typing import List, Optional

# Model Imports
from models.article import Article
from models.author import Author
from models.citation import Citation
from models.figure import Figure
from models.image import Image

# Model Repository Imports
from repo.author_repo import AuthorRepository
from repo.citation_repo import CitationRepository
from repo.figure_repo import FigureRepository
from repo.image_repo import ImageRepository

# Service Imports
from services.db import db 

# Article Repository 
# This class is responsible for handling all database operations related to the Article model.
class ArticleRepository:
    @staticmethod
    def fetch_by_article_id(article_id: int) -> Optional[Article]:
        '''Fetches an article from the database by ID.'''
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
            user_input=row["user_input"],
            prompt=row["prompt"],
            add_date=row["add_date"],
            authors=AuthorRepository.fetch_all_by_article_id(article_id),
            citations=CitationRepository.fetch_all_by_article_id(article_id),
            images=ImageRepository.fetch_all_by_article_id(article_id), 
            figures=FigureRepository.fetch_all_by_article_id(article_id)          
        )
    
    @staticmethod
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
    
    @staticmethod
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

    @staticmethod
    def delete(article_id: int) -> None:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM articles
            WHERE article_id = ?
        ''', (article_id,))
        conn.commit()
        cursor.close()

    @staticmethod
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
                add_date=row["add_date"],
                authors=AuthorRepository.fetch_all_by_article_id(row["article_id"]),
                citations=CitationRepository.fetch_all_by_article_id(row["article_id"]),
                images=ImageRepository.fetch_all_by_article_id(row["article_id"]),
                figures=FigureRepository.fetch_all_by_article_id(row["article_id"])
            )
            for row in rows
        ]
    
    @staticmethod
    def count() -> int:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM articles')
        count = cursor.fetchone()[0]
        cursor.close()
        return count
    

    
    