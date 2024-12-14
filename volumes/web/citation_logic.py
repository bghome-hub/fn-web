import db
from models import Citation

# Create a citation object
def create_citation(article_id, number, conent):
    return Citation(article_id, number, content)

# Save a citation object
def save_citation_to_db(citation):
    db.insert_citation(citation)
