import requests
import random
from typing import List
from config import config
from models.image import Image

# fetches an image from the Unsplash API based on a given keyword
def find_image(keyword: str) -> Image:

    params = {
        "query": keyword,
        "per_page": 1,  # Only fetch one result to ensure top relevance
        "page": 1
    }
    headers = {
        "Authorization": f"Client-ID {config.IMAGE_API_KEY}"
    }

    response = requests.get(config.IMAGE_API_URL, headers=headers, params=params)
    response.raise_for_status()

    # parse out url of topmost image result and title and description   
    data = response.json()
    results = data.get("results", [])
    if not results:
        return None  # No results found
    
    url = results[0]["urls"]["regular"]
    image = Image(
        keyword=keyword,
        url=url
    )

    return image

# fetches an image from the Unsplash API, no keyword required
def find_journalist_image() -> str:

    params = {
        "query": "headshot",
        "per_page": 30,  # Only fetch one result to ensure top relevance
        "page": 1
    }
    headers = {
        "Authorization": f"Client-ID {config.IMAGE_API_KEY}"
    }

    response = requests.get(config.IMAGE_API_URL, headers=headers, params=params)
    response.raise_for_status()

    # parse out url of topmost image result and title and description   
    data = response.json()
    results = data.get("results", [])
    if not results:
        return None  # No results found
    
    random_image = random.choice(results)
    url = random_image["urls"]["regular"]
     
    return url



# fetches an image from the Unsplash API based on a given keyword
def find_image_url(keyword: str) -> str:

    params = {
        "query": keyword,
        "per_page": 1,  # Only fetch one result to ensure top relevance
        "page": 1
    }
    headers = {
        "Authorization": f"Client-ID {config.IMAGE_API_KEY}"
    }

    response = requests.get(config.IMAGE_API_URL, headers=headers, params=params)
    response.raise_for_status()

    # parse out url of topmost image result and title and description   
    data = response.json()
    results = data.get("results", [])
    if not results:
        return None  # No results found
    
    url = results[0]["urls"]["regular"]

    return url