import requests
from models import Image
import db

def fetch_image_url(topic):
    api_key = 'your_unsplash_api_key'
    url = f'https://api.unsplash.com/photos/random?query={topic}&client_id={api_key}'
    response = requests.get(url)
    data = response.json()
    return data[0]['urls']['regular']  # Return the regular image URL

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

def create_figure_for_article(article_id, description, url):
    """Creates a Figure object and inserts it into the database."""
    figure = Figure(
        number=None,  # Set based on your logic (or count existing figures for the article)
        description=description,
        url=url,
        article_id=article_id
    )

    # Insert figure into the database
    db.insert_figure(figure)
