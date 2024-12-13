from models import Citation
import db

def create_citation(article_id, number, citation_text):
    return Citation(article_id, number, citation_text)

def save_citation(citation):
    db.insert_citation(citation)
