from models import Author
import db

# Create an author object
def create_author(article_id, number, name, institution_name, institution_address, email):
    return Author(article_id, number, name, institution_name, institution_address, email)

# Save an author object
def save_author_to_db(author):
    db.insert_author(author)
