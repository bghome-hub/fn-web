from typing import List, Optional

from models.story import Story
from models.breakout import Breakout

from services import db_service_story as story_db

class BreakoutRepository:
    @staticmethod
    def fetch_by_guid(guid: str) -> Optional[Breakout]:
        '''Fetches a breakout from the database by GUID.'''
        conn = story_db.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM breakouts WHERE guid = ?", (guid,))
        row = cursor.fetchone()
        cursor.close()
        if row is None:
            return None
        
        return Breakout(
            guid=row["guid"],
            number=row["number"],
            title=row["title"],
            content=row["content"],
            story_id=row["story_id"],
            add_date=row["add_date"]
        )
    
    @staticmethod
    def fetch_all() -> List[Breakout]:
        '''Fetches all breakouts from the database.'''
        conn = story_db.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM breakouts")
        rows = cursor.fetchall()
        cursor.close()
        breakouts = []
        for row in rows:
            breakouts.append(Breakout(
                guid=row["guid"],
                number=row["number"],
                title=row["title"],
                content=row["content"],
                story_id=row["story_id"],
                add_date=row["add_date"]
            ))
        return breakouts
    
    @staticmethod
    def fetch_all_by_story_id(story_id: int) -> List[Breakout]:
        '''Fetches all breakouts for a given story.'''
        conn = story_db.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM breakouts WHERE story_id = ?", (story_id,))
        rows = cursor.fetchall()
        cursor.close()
        breakouts = []
        for row in rows:
            breakouts.append(Breakout(
                guid=row["guid"],
                number=row["number"],
                title=row["title"],
                content=row["content"],
                story_id=row["story_id"],
                add_date=row["add_date"]
            ))
        return breakouts
    
    @staticmethod
    def insert(breakout: Breakout) -> None:
        '''Inserts a breakout into the database.'''
        conn = story_db.connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO breakouts (guid, number, title, content, story_id, add_date) VALUES (?, ?, ?, ?, ?, ?)",
            (breakout.guid, breakout.number, breakout.title, breakout.content, breakout.story_id, breakout.add_date)
        )
        conn.commit()
        cursor.close()

    