import requests
import os

IMAGE_API_KEY = os.getenv("IMAGE_API_KEY", "demo")
DB_FILE = os.getenv("DB_FILE", "/db/db.db")

# Search Unsplash for Image
def search_unsplash(image_value):
    url = f"https://api.unsplash.com/search/photos?query={image_value}&client_id={IMAGE_API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data['results'][0]['urls']['regular'] if data['results'] else None

