from models import Figure
import db

def create_figure(article_id, section, number, identifier, description, local, url):
    return Figure(article_id, section, number, identifier, description, local, url)

def save_figure(figure):
    db.insert_figure(figure)
