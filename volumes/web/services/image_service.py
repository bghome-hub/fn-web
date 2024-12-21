import requests
from typing import List
from config import config
from models.image import Image

# fetches an image from the Unsplash API based on a given keyword
def find_image(keyword: str) -> Image:
    print(f"Finding image for keyword: {keyword}")
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
