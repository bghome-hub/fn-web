import logging
from typing import List, Optional

from models.story import Story

from repo.quote_repo import QuoteRepository
from repo.breakout_repo import BreakoutRepository

from services import db_service_story as story_db

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class StoryRepository:
    @staticmethod
    def fetch_by_story_id(story_id: int) -> Optional[Story]:
        '''Fetches a story from the database by ID.'''
        logging.debug(f"Fetching story by ID: {story_id}")
        conn = story_db.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM stories WHERE story_id = ?", (story_id,))
        row = cursor.fetchone()
        cursor.close()
        if row is None:
            return None
        
        story = Story(
            guid=row["guid"],
            headline=row["headline"],
            subheadline=row["subheadline"],
            journalist_name=row["journalist_name"],
            journalist_bio=row["journalist_bio"],
            journalist_email=row["journalist_email"],
            journalist_photo=row["journalist_photo"],
            publication=row["publication"],
            publication_date=row["publication_date"],
            title=row["title"],
            content=row["content"],
            keywords=row["keywords"],
            quotes=QuoteRepository.fetch_all_by_story_id(story_id),
            breakouts=BreakoutRepository.fetch_all_by_story_id(story_id),
            add_date=row["add_date"]
        )
        logging.debug(f"Fetched story: {story}")
        return story
    
    @staticmethod
    def fetch_all() -> List[Story]:
        '''Fetches all stories from the database.'''
        logging.debug("Fetching all stories")
        conn = story_db.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM stories")
        rows = cursor.fetchall()
        cursor.close()
        stories = []
        for row in rows:
            story = Story(
                guid=row["guid"],
                story_id=row["story_id"],
                headline=row["headline"],
                subheadline=row["subheadline"],
                journalist_name=row["journalist_name"],
                journalist_bio=row["journalist_bio"],
                journalist_email=row["journalist_email"],
                journalist_photo=row["journalist_photo"],
                publication=row["publication"],
                publication_date=row["publication_date"],
                title=row["title"],
                content=row["content"],
                keywords=row["keywords"],
                quotes=QuoteRepository.fetch_all_by_story_id(row["story_id"]),
                breakouts=BreakoutRepository.fetch_all_by_story_id(row["story_id"]),
                add_date=row["add_date"]
            )
            stories.append(story)
            logging.debug(f"Fetched story: {story}")
        logging.debug(f"Total stories fetched: {len(stories)}")
        return stories


    @staticmethod
    def insert(story: Story) -> int:
        '''Inserts a story into the database.'''
        logging.debug(f"Inserting story: {story}")
        conn = story_db.connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO stories (guid, headline, subheadline, journalist_name, journalist_bio, journalist_email, journalist_photo, publication, publication_date, title, content, keywords, add_date) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (story.guid, story.headline, story.subheadline, story.journalist_name, story.journalist_bio, story.journalist_email, story.journalist_photo, story.publication, story.publication_date, story.title, story.content, story.keywords, story.add_date)
        )
        conn.commit()
        story_id = cursor.lastrowid
        cursor.close()
        logging.debug(f"Inserted story with ID: {story_id}")
        return story_id
    
    @staticmethod
    def insert_full_story(story: Story) -> int:
        logging.debug(f"Inserting full story: {story}")
        story_id = StoryRepository.insert(story)
        for quote in story.quotes:
            quote.story_id = story_id
            QuoteRepository.insert(quote)
            logging.debug(f"Inserted quote: {quote}")
        for breakout in story.breakouts:
            breakout.story_id = story_id
            BreakoutRepository.insert(breakout)
            logging.debug(f"Inserted breakout: {breakout}")
        logging.debug(f"Full story inserted with ID: {story_id}")
        return story_id


    @staticmethod
    def fetch_last_x_stories(x: int) -> List[Story]:
        conn = story_db.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM stories ORDER BY story_id DESC LIMIT ?", (x,))
        rows = cursor.fetchall()
        cursor.close()
        if not rows:
            return []   
        
        return [
            Story(
                guid=row["guid"],
                story_id=row["story_id"],
                headline=row["headline"],
                subheadline=row["subheadline"],
                journalist_name=row["journalist_name"],
                journalist_bio=row["journalist_bio"],
                journalist_email=row["journalist_email"],
                journalist_photo=row["journalist_photo"],
                publication=row["publication"],
                publication_date=row["publication_date"],
                title=row["title"],
                content=row["content"],
                keywords=row["keywords"],
                quotes=QuoteRepository.fetch_all_by_story_id(row["story_id"]),
                breakouts=BreakoutRepository.fetch_all_by_story_id(row["story_id"]),
                add_date=row["add_date"]
            )
            for row in rows
        ]

    
    @staticmethod
    def delete(story_id: int) -> None:
        conn = story_db.connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM stories WHERE story_id = ?", (story_id,))
        conn.commit()
        cursor.close()
        logging.debug(f"Deleted story with ID: {story_id}")

        