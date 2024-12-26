from typing import List, Optional

from models.quote import Quote
from models.story import Story

from services import db_service_story as story_db

class QuoteRepository:    
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
                quote_id=row["quote_id"],
                guid=row["guid"],
                number=row["number"],
                description=row["description"],
                content=row["content"],
                speaker=row["speaker"],
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
                quote_id=row["quote_id"],
                guid=row["guid"],
                number=row["number"],
                description=row["description"],
                content=row["content"],
                speaker=row["speaker"],
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
            "INSERT INTO quotes (guid, number, description, content, speaker, story_id, add_date) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (quote.guid, quote.number, quote.description, quote.content, quote.speaker, quote.story_id, quote.add_date)
        )
        conn.commit()
        cursor.close()
        conn.close()

