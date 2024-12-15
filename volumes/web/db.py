# Description: This file contains the functions to interact with the SQLite database.
import sqlite3
from titlecase import titlecase
import os


# Get the path to the database file from the environment variable or use the default path
DB_FILE = os.getenv("DB_FILE", "/db/db.db")

# Connect to the SQLite database
def connect_db():
    return sqlite3.connect(DB_FILE)

# Create the necessary tables in the database
def create_tables():
    conn = connect_db()
    cursor = conn.cursor()
    
    # Articles table
    cursor.execute('''CREATE TABLE IF NOT EXISTS articles (
                       id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       title TEXT, 
                       journal TEXT,
                       doi TEXT,
                       abstract TEXT, 
                       intro TEXT, 
                       methodology TEXT, 
                       results TEXT, 
                       discussion TEXT, 
                       conclusion TEXT,
                       keywords TEXT,
                       prompt TEXT,
                       input TEXT,
                       add_date datetime DEFAULT CURRENT_TIMESTAMP,
                       update_date datetime DEFAULT CURRENT_TIMESTAMP
                       )''')
    
    # Authors table
    cursor.execute('''CREATE TABLE IF NOT EXISTS authors (
                       id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       article_id INTEGER, 
                       number INTEGER,
                       name TEXT,
                       institution_name TEXT,
                       institution_address TEXT,
                       email TEXT,
                       add_date datetime DEFAULT CURRENT_TIMESTAMP,
                       FOREIGN KEY(article_id) REFERENCES articles(id)
                       )''')
    
    # Citations table
    cursor.execute('''CREATE TABLE IF NOT EXISTS citations (
                       id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       article_id INTEGER,    
                       number INTEGER,
                       content TEXT,
                       add_date datetime DEFAULT CURRENT_TIMESTAMP,
                       FOREIGN KEY(article_id) REFERENCES articles(id)
                       )''')
    
    # Images table
    cursor.execute('''CREATE TABLE IF NOT EXISTS images (
                       id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       article_id INTEGER,
                       number INTEGER,
                       description TEXT,
                       keywords TEXT,
                       url TEXT,
                       add_date datetime DEFAULT CURRENT_TIMESTAMP,
                       FOREIGN KEY(article_id) REFERENCES articles(id)
                       )''')
    
    # Figures table (Fixed the missing closing parenthesis in the FOREIGN KEY constraint)
    cursor.execute('''CREATE TABLE IF NOT EXISTS figures (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       article_id INTEGER,
                       number INTEGER,
                       description TEXT,
                       url TEXT,
                       add_date datetime DEFAULT CURRENT_TIMESTAMP,
                       FOREIGN KEY(article_id) REFERENCES articles(id)
                       )''')

    conn.commit()

# initialize the database tables
create_tables()


'''
INSERT functions
'''
def insert_article(article):
    """Inserts an article object into the articles table and returns the article_id."""
    conn = connect_db()
    cursor = conn.cursor()
    
    # Insert the article into the articles table
    cursor.execute('''INSERT INTO articles (title, journal, doi, abstract, intro, methodology, results, discussion, conclusion, keywords, prompt, input) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                   (titlecase(article.title), article.journal, article.doi, article.abstract, article.intro, article.methodology, article.results, article.discussion, article.conclusion, article.keywords, article.prompt, article.input))
    conn.commit()
    
    # Retrieve the article_id of the newly inserted article
    id = cursor.lastrowid
    conn.close()

    return id  # Return the article_id

def insert_author(author):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO authors (article_id, number, name, institution_name, institution_address, email) 
                      VALUES (?, ?, ?, ?, ?, ?)''',
                   (author.article_id, author.number, author.name, author.institution_name, author.institution_address, author.email))
    conn.commit()

def insert_citation(citation):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO citations (article_id, number, content) 
                      VALUES (?, ?, ?)''',
                   (citation.article_id, citation.number, citation.content))
    conn.commit()

def insert_image(image):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO images (article_id, number, description, keywords, url) 
                      VALUES (?, ?, ?, ?, ?)''',
                   (image.article_id, image.number, image.description, image.keywords, image.url))
    conn.commit()

def insert_figure(figure):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO figures (article_id, number, description, url) 
                      VALUES (?, ?, ?, ?)''',
                   (figure.article_id, figure.number, figure.description, figure.url))
    conn.commit()

'''
GET functions
'''
def get_article_by_id(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM articles WHERE id = ?''', (id,))
    article_data = cursor.fetchone()
    conn.close()
    return article_data

def get_authors_by_article_id(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM authors WHERE article_id = ?''', (id,))
    authors_data = cursor.fetchall()
    conn.close()
    return authors_data

def get_citations_by_article_id(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM citations WHERE article_id = ?''', (id,))
    citations_data = cursor.fetchall()
    conn.close()
    return citations_data

def get_images_by_article_id(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM images WHERE article_id = ?''', (id,))
    images_data = cursor.fetchall()
    conn.close()
    return images_data

def get_figures_by_article_id(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM figures WHERE article_id = ?''', (id,))
    figures_data = cursor.fetchall()
    conn.close()
    return figures_data

def get_all_articles():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM articles''')
    all_articles = cursor.fetchall()
    conn.close()
    return all_articles

def get_count_of_articles():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''SELECT COUNT(*) FROM articles''')
    count_of_articles = cursor.fetchone()
    conn.close()
    return count_of_articles

def execute_predefined_query(query_name):
    queries = {
        'get_all_articles': 'SELECT * FROM articles',
        'get_all_authors': 'SELECT * FROM authors',
        'get_all_citations': 'SELECT * FROM citations',
    }

    query = queries.get(query_name)
    if not query:
        return None

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    conn.close()

    return {'columns': columns, 'data': data}