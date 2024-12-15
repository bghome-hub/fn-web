# Description: This file contains the models for the database tables. Each class represents a table in the database.
# models.py
from typing import Optional, List, Tuple
import ollama
import db

class Article:
    def __init__(self, prompt, input, title, journal, doi, abstract, intro, methodology, results, discussion, conclusion, keywords, id=None, authors=None, citations=None, images=None, figures=None, add_date=None, update_date=None):
        self.prompt = prompt  # Store the prompt
        self.input = input
        self.title = title
        self.journal = journal
        self.doi = doi
        self.abstract = abstract
        self.intro = intro
        self.methodology = methodology
        self.results = results
        self.discussion = discussion
        self.conclusion = conclusion
        self.keywords = keywords
        self.id = id
        self.add_date = add_date
        self.update_date = update_date

        # Initialize lists if none are provided
        self.authors = authors if authors else []
        self.citations = citations if citations else []
        self.images = images if images else []
        self.figures = figures if figures else []
        
    # This is a magic method that allows us to print the object in a more readable format
    def __repr__(self):
        return f"Article({self.title}, {len(self.authors)} authors, {len(self.citations)} citations)"
    
    @classmethod
    def create_from_topic(cls, topic):
        
        # Query Ollama API for the topic
        ollama_response = ollama.query_ollama(topic)
        
        # Extract relevant fields from the response
        title = ollama_response['title']
        journal = ollama_response['journal']
        doi = ollama_response['doi']
        abstract = ollama_response['abstract']
        intro = ollama_response['introduction']
        methodology = ollama_response['methodology']
        results = ollama_response['results']
        discussion = ollama_response['discussion']
        conclusion = ollama_response['conclusion']
        keywords = ollama_response['keywords']
        prompt = ollama_response['prompt']
        input = ollama_response['input']
        
        # Create Author objects from the authors field in the response
        authors = []
        for i, author_data in enumerate(ollama_response['authors']):
            authors.append(Author(
                number=i + 1, 
                name=author_data.get('name', ''), 
                institution_name=author_data.get('institution_name', ''),
                institution_address=author_data.get('institution_address', ''),
                email=author_data.get('email', '')
            ))

        # Create Citation objects from the citations field in the response
        citations = []
        for i, citation_data in enumerate(ollama_response['citations']):
            citations.append(Citation(
                number=i + 1,
                content=citation_data.get('content', '').strip()
            ))

        # Create Article object
        return cls(
            title=title,
            journal=journal,
            doi=doi,
            abstract=abstract,
            intro=intro,
            methodology=methodology,
            results=results,
            discussion=discussion,
            conclusion=conclusion,
            keywords=keywords,
            authors=authors,
            citations=citations,
            prompt=prompt,
            input=input
        )
    
    def save_to_db(self):
        # Insert the article into the database
        self.id = db.insert_article(self)
        
        # Insert the authors, citations, images, and figures into the database
        for author in self.authors:
            author.article_id = self.id
            author.save_to_db()

        for citation in self.citations:
            citation.article_id = self.id
            citation.save_to_db()

        for image in self.images:
            image.article_id = self.id
            image.save_to_db()

        for figure in self.figures:
            figure.article_id = self.id
            figure.save_to_db()

        return self
    
    # This function is used to create an Article object from a row in the database
    @classmethod
    def create_from_id(cls, id: Tuple) -> 'Article':
        article = cls(
            title=id[1],
            journal=id[2],
            doi=id[3],
            abstract=id[4],
            intro=id[5],
            methodology=id[6],
            results=id[7],
            discussion=id[8],
            conclusion=id[9],
            keywords=id[10],
            prompt=id[11],
            input=id[12],
            id=id[0],
            add_date=id[13],
            update_date=id[14]
        )

        return article
    
    @classmethod
    def get_by_id(cls, id: int) -> Optional['Article']:
        """Returns an Article object with the given id."""
        row = db.get_article_by_id(id)
        if row:
            article = cls.create_from_id(row)
            article.authors = Author.get_by_article_id(article.id)
            article.citations = Citation.get_by_article_id(article.id)
            article.images = Image.get_by_article_id(article.id)
            article.figures = Figure.get_by_article_id(article.id)
            return article
        else:
            return None
            
    @classmethod
    def get_all(cls) -> List['Article']:
        """Returns a list of all articles as Article objects."""
        rows = db.get_all_articles()
        articles = []

        for row in rows:
            article = cls.create_from_id(row)
            article.authors = Author.get_by_article_id(article.id)
            article.citations = Citation.get_by_article_id(article.id)
            article.images = Image.get_by_article_id(article.id)
            article.figures = Figure.get_by_article_id(article.id)
            articles.append(article)

        return articles
        
    @classmethod
    def count(cls) -> int:
        """Returns the count of articles in the database."""
        return db.get_count_of_articles()
        

    @classmethod
    def get_last_x_articles(cls, x: int) -> List['Article']:
        """Returns the last x articles added to the database."""
        rows = db.get_last_x_articles(x)
        articles = []

        for row in rows:
            article = cls.create_from_id(row)
            article.authors = Author.get_by_article_id(article.id)
            article.citations = Citation.get_by_article_id(article.id)
            article.images = Image.get_by_article_id(article.id)
            article.figures = Figure.get_by_article_id(article.id)
            articles.append(article)

        return articles

class Author:
    def __init__(self, number, name, institution_name, institution_address, email, article_id=None):
        self.number = number
        self.name = name
        self.institution_name = institution_name
        self.institution_address = institution_address
        self.email = email
        self.article_id = article_id

    def save_to_db(self):
        db.insert_author(self)

    @classmethod
    def get_by_article_id(cls, article_id):
        rows = db.get_authors_by_article_id(article_id)
        authors = []
        for row in rows:
            authors.append(cls(
                number=row[2],
                name=row[3],
                institution_name=row[4],
                institution_address=row[5],
                email=row[6],
                article_id=row[1]
            ))
        return authors

class Citation:
    def __init__(self, number, content, article_id=None):
        self.number = number
        self.content = content
        self.article_id = article_id

    def save_to_db(self):
        db.insert_citation(self)

    @classmethod
    def get_by_article_id(cls, article_id):
        rows = db.get_citations_by_article_id(article_id)
        citations = []
        for row in rows:
            citations.append(cls(
                number=row[2],
                content=row[3],
                article_id=row[1]
            ))
        return citations

class Image:
    def __init__(self, number, description, keywords, url, article_id=None):
        self.number = number
        self.description = description
        self.keywords = keywords
        self.url = url
        self.article_id = article_id

    def save_to_db(self):
        db.insert_image(self)

    @classmethod
    def get_by_article_id(cls, article_id):
        rows = db.get_images_by_article_id(article_id)
        images = []
        for row in rows:
            images.append(cls(
                number=row[2],
                description=row[3],
                keywords=row[4],
                url=row[5],
                article_id=row[1]
            ))
        return images

class Figure:
    def __init__(self, number, description, url, article_id=None):
        self.number = number        
        self.description = description
        self.url = url
        self.article_id = article_id

    def save_to_db(self):
        db.insert_figure(self)

    @classmethod
    def get_by_article_id(cls, article_id):
        rows = db.get_figures_by_article_id(article_id)
        figures = []
        for row in rows:
            figures.append(cls(
                number=row[2],
                description=row[3],
                url=row[4],
                article_id=row[1]
            ))
        return figures
