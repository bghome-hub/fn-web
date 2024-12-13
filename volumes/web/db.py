import os
import sqlite3
from titlecase import titlecase

DB_FILE = os.getenv("DB_FILE", "/db/db.db")

def connect_db():
    return sqlite3.connect(DB_FILE)

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()
    
    # Articles table
    cursor.execute('''CREATE TABLE IF NOT EXISTS articles (
                       id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       title TEXT, 
                       abstract TEXT, 
                       intro TEXT, 
                       methodology TEXT, 
                       results TEXT, 
                       discussion TEXT, 
                       conclusion TEXT,
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

def insert_article(article):
    """Inserts an article object into the articles table and returns the article_id."""
    conn = connect_db()
    cursor = conn.cursor()
    
    # Insert the article into the articles table
    cursor.execute('''INSERT INTO articles (title, abstract, intro, methodology, results, discussion, conclusion, prompt, input) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                   (titlecase(article.title), article.abstract, article.intro, article.methodology, article.results, article.discussion, article.conclusion, article.prompt, article.input))
    
    conn.commit()
    
    # Retrieve the article_id of the newly inserted article
    article_id = cursor.lastrowid
    
    conn.close()
    
    return article_id  # Return the article_id

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
