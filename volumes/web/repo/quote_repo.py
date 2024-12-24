from typing import List, Optional

from models.quote import Quote
from models.story import Story

from services import db_service_story as story_db

class QuoteRepository:
    @staticmethod
    def fetch_by_guid(guid: str) -> Optional[Story]:
        '''Fetches a quote from the database by GUID.'''
        conn = story_db.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM quotes WHERE guid = ?", (guid,))
        row = cursor.fetchone()
        cursor.close()
        if row is None:
            return None
    
        return Quote(
            guid=row["guid"],
            content=row["content"],
            story_id=row["story_id"],
            add_date=row["add_date"]
        )
    
    @staticmethod
    def fetch_all() -> List[Quote]:
        '''Fetches all quotes from the database.'''
        conn = story_db.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM quotes")
        rows = cursor.fetchall()
        cursor.close()
        quotes = []
        for row in rows:
            quotes.append(Quote(
                guid=row["guid"],
                content=row["content"],
                story_id=row["story_id"],
                add_date=row["add_date"]
            ))
        return quotes
    
    @staticmethod
    def fetch_all_by_story_id(story_id: int) -> List[Quote]:
        '''Fetches all quotes for a given story.'''
        conn = story_db.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM quotes WHERE story_id = ?", (story_id,))

        rows = cursor.fetchall()
        cursor.close()
        quotes = []
        for row in rows:
            quotes.append(Quote(
                guid=row["guid"],
                content=row["content"],
                story_id=row["story_id"],
                add_date=row["add_date"]
            ))
        return quotes
    
    @staticmethod
    def insert(quote: Quote) -> None:
        '''Inserts a quote into the database.'''
        conn = story_db.connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO quotes (guid, content, story_id, add_date) VALUES (?, ?, ?, ?)",
            (quote.guid, quote.content, quote.story_id, quote.add_date)
        )
        conn.commit()
        cursor.close()
        conn.close()

        