import config
import requests
from dataclasses import dataclass
from typing import Optional, List

from services.db import db
from models.image import Image

# Image Repository
# This class is responsible for handling all database operations related to the Image model.
class ImageRepository:
    @staticmethod
    def fetch_by_image_id(image_id: int) -> Optional[Image]:
        """Fetches an image from the database by ID."""
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM images WHERE id = ?", (image_id,))
        row = cursor.fetchone()
        cursor.close()
        if row is None:
            return None
        
        return Image(
            image_id=row["image_id"],
            article_id=row["article_id"],
            guid=row["guid"],
            number=row["number"],
            title=row["title"],
            description=row["description"],
            keyword=row["keyword"],
            url=row["url"],
            local=row["local"],
            add_date=row["add_date"]
        )

    @staticmethod
    def fetch_all_by_article_id(article_id: int) -> List[Image]:
        """Fetches all images for a given article."""
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM images WHERE article_id = ?", (article_id,))
        rows = cursor.fetchall()
        cursor.close()
        images = []
        for row in rows:
            images.append(Image(
                image_id=row["image_id"],
                article_id=row["article_id"],
                guid=row["guid"],
                number=row["number"],
                title=row["title"],
                description=row["description"],
                keyword=row["keyword"],
                url=row["url"],
                local=row["local"],
                add_date=row["add_date"]
            ))
        return images
    
    @staticmethod
    def fetch_all() -> List[Image]:
        """Fetches all images from the database."""
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM images")
        rows = cursor.fetchall()
        cursor.close()
        images = []
        for row in rows:
            images.append(Image(
                image_id=row["image_id"],
                article_id=row["article_id"],
                guid=row["guid"],
                number=row["number"],
                title=row["title"],
                description=row["description"],
                keyword=row["keyword"],
                url=row["url"],
                local=row["local"],
                add_date=row["add_date"]
            ))
        return images
    
    @staticmethod
    def insert(image: Image) -> int:
        """Inserts an image into the database."""
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO images (article_id, guid, number, title, description, keyword, url, local, add_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            image.article_id,
            image.guid,
            image.number,
            image.title,
            image.description,
            image.keyword,
            image.url,
            image.local,
            image.add_date
        ))
        conn.commit()
        image_id = cursor.lastrowid
        cursor.close()
        return image_id
    
    @staticmethod
    def update(image: Image) -> None:
        """Updates an image in the database."""
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE images
            SET article_id = ?, guid = ?, number = ?, title = ?, description = ?, keyword = ?, url = ?, local = ?, add_date = ?
            WHERE image_id = ?
        ''', (
            image.article_id,
            image.guid,
            image.number,
            image.title,
            image.description,
            image.keyword,
            image.url,
            image.local,
            image.add_date,
            image.image_id
        ))
        conn.commit()
        cursor.close()

    @staticmethod
    def delete(image_id: int) -> None:
        """Deletes an image from the database."""
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM images WHERE image_id = ?", (image_id,))
        conn.commit()
        cursor.close()

