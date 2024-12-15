# Description: This module contains the function create_article_from_response_data which creates an Article object from the response data and inserts it into the database.
# article.py
import db
import ollama
from models import Article, Author, Citation
import author_logic, citation_logic, image_logic, figure_logic

#Create article from topic
def create_article_from_topic(topic):
    ollama_response = ollama.query_ollama(topic)
    article = create_article_from_ollama_response(ollama_response)
    return article

def create_article_from_ollama_response(response_data):
    
    # Extract relevant fields from the response
    title = response_data['title']
    abstract = response_data['abstract']
    intro = response_data['introduction']
    methodology = response_data['methodology']
    results = response_data['results']
    discussion = response_data['discussion']
    conclusion = response_data['conclusion']
    prompt = response_data['prompt']
    input = response_data['input']
    
    # Create Author objects from the authors field in the response
    authors = []
    for i, author_data in enumerate(response_data['authors']):
        authors.append(Author(
            number=i + 1, 
            name=author_data.get('name', ''), 
            institution_name=author_data.get('institution_name', ''),
            institution_address=author_data.get('institution_address', ''),
            email=author_data.get('email', '')
        ))

    # Create Citation objects from the citations field in the response
    citations = []
    for i, citation_data in enumerate(response_data['citations']):
        citations.append(Citation(
            number=i + 1,
            content=citation_data.get('content', '').strip()
        ))

    # Create Article object
    article = Article(
        title=title,
        abstract=abstract,
        intro=intro,
        methodology=methodology,
        results=results,
        discussion=discussion,
        conclusion=conclusion,
        authors=authors,
        citations=citations,
        prompt=prompt,
        input=input
    )

    return article

# Save the article and related entities to the database
def save_article_to_db(article):
    
    article.id = db.insert_article(article)

    # Now insert the authors, citations, and other related entities with the id
    for author in article.authors:
        author.article_id = article.id
        author_logic.save_author_to_db(author)

    for citation in article.citations:
        citation.article_id = article.id
        citation_logic.save_citation_to_db(citation)

    return article

# get article by id
def get_article_by_id(id):
    """Returns an Article object with the given id."""
    article = db.get_article_by_id(id)
    if article:
        article = Article(
            id=article[0],
            title=article[1],
            abstract=article[2],
            intro=article[3],
            methodology=article[4],
            results=article[5],
            discussion=article[6],
            conclusion=article[7],
            prompt=article[8],
            input=article[9],
            add_date=article[10],
            update_date=article[11]
        )
        return article
    else:
        return None

def get_all_articles():
    """Returns a list of all articles as Article objects."""
    article_rows = db.get_all_articles()
    articles = []

    for row in article_rows:
        article = Article(
            id=row[0],
            title=row[1],
            abstract=row[2],
            intro=row[3],
            methodology=row[4],
            results=row[5],
            discussion=row[6],
            conclusion=row[7],
            prompt=row[8],
            input=row[9],
            add_date=row[10],
            update_date=row[11]
        )
        articles.append(article)

    return articles

def get_count_of_articles():
    """Returns the count of articles in the database."""
    count = db.get_count_of_articles()
    return count