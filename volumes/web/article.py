from models import Article, Author, Citation
import db

def create_article_from_data(response_data):
    """Creates an Article object from the response data and inserts it into the database."""
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
        prompt=prompt,  # Store the prompt
        input=input     # Store the input
    )

    # Insert the article into the database and get the article_id
    article.article_id = db.insert_article(article)

    # Now insert the authors, citations, and other related entities with the article_id
    for author in authors:
        author.article_id = article.article_id
        db.insert_author(author)

    for citation in citations:
        citation.article_id = article.article_id
        db.insert_citation(citation)

    return article
