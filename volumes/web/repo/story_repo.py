from typing import List, Optional

from models.story import Story
from models.author import Author
from models.quote import Quote

from repo.author_repo import AuthorRepository
from repo.quote_repo import QuoteRepository
from repo.breakout_repo import BreakoutRepository


from services import db_service_story as story_db

class StoryRepository:
    @staticmethod
    def fetch_by_guid(story_id: str) -> Optional[Story]:
        '''Fetches a story from the database by GUID.'''
        conn = story_db.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM stories WHERE guid = ?", (story_id,))
        row = cursor.fetchone()
        cursor.close()
        if row is None:
            return None

        return Story(
            guid=row["guid"],
            headline=row["headline"],
            publication=row["publication"],
            publication_date=row["publication_date"],
            title=row["title"],
            content=row["content"],
            keywords=row["keywords"],
            article_id=row["article_id"],
            add_date=row["add_date"],
            authors=AuthorRepository.fetch_all_by_story_id(story_id),
            quotes=QuoteRepository.fetch_all_by_story_id(story_id),
            breakouts=BreakoutRepository.fetch_all_by_story_id(story_id)
        )

    @staticmethod
    def fetch_all() -> List[Story]:
        '''Fetches all stories from the database.'''
        conn = story_db.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM stories")
        rows = cursor.fetchall()
        cursor.close()
        stories = []
        for row in rows:
            stories.append(Story(
                guid=row["guid"],
                headline=row["headline"],
                publication=row["publication"],
                publication_date=row["publication_date"],
                content=row["content"],
                article_id=row["article_id"],
                add_date=row["add_date"]
            ))
        return stories

    @staticmethod
    def fetch_all_by_story_id(story_id: int) -> List[Story]:
        '''Fetches all stories for a given article.'''
        conn = story_db.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM stories WHERE story_id = ?", (story_id,))
        rows = cursor.fetchall()
        cursor.close()
        stories = []
        for row in rows:
            stories.append(Story(
                guid=row["guid"],
                headline=row["headline"],
                publication=row["publication"],
                publication_date=row["publication_date"],
                content=row["content"],
                article_id=row["article_id"],
                add_date=row["add_date"]
            ))
        return stories

    @staticmethod
    def insert(story: Story) -> int:
        '''Inserts a story into the database.'''
        conn = story_db.connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO stories (guid, headline, publication, publication_date, content, add_date) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (story.guid, story.headline, story.publication, story.publication_date, story.content, story.add_date)
        )
        conn.commit()
        story_id = cursor.lastrowid
        cursor.close()
        return story_id
    

    @staticmethod
    def insert_full_story(story: Story) -> int:
        story_id = StoryRepository.insert(story)
        for author in story.authors:
            author.article_id = story_id
            AuthorRepository.insert(author)
        for quote in story.quotes:
            quote.article_id = story_id
            QuoteRepository.insert(quote)
        for breakout in story.breakouts:
            breakout.story_id = story_id
            BreakoutRepository.insert(breakout)

        return story_id
    

    
