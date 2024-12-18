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
    def get_by_article_id(article_id: int) -> List[Image]:
      

def fetch_image_url(keywords):
    """Fetches the URL of an image based on the keywords."""
    params = {
        "query": keywords,
        "per_page": 1,  # Only fetch one result to ensure top relevance
        "page": 1
    }
    headers = {
        "Authorization": f"Client-ID {config.IMAGE_API_KEY}"
    }

    response = requests.get(config.image_url, headers=headers, params=params)
    response.raise_for_status()

    data = response.json()
    results = data.get("results", [])
    if not results:
        return None  # No results found

    # Return the URL of the topmost image result
    return results[0]["urls"]["regular"]

def create_image(article_id, number, description, keywords, local, url):
    return Image(article_id, number, description, keywords, local, url)

def save_image(image):
    db.insert_image(image)

def create_image_for_article(article_id, description, keywords, url):
    """Creates an Image object and inserts it into the database."""
    image = Image(
        number=None,  # Set based on your logic (or count existing images for the article)
        description=description,
        keywords=keywords,
        url=url,
        article_id=article_id
    )

    # Insert image into the database
    db.insert_image(image)
