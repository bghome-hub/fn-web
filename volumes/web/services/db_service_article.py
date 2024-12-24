# Description: This file contains the functions to interact with the SQLite database.
import sqlite3
from titlecase import titlecase
import shutil

from config import config 

# Connect to the SQLite database
def connect_db():
    conn = sqlite3.connect(config.DB_FILE_ARTICLES)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn

# Backup and restore database functions
def backup_db(backup_path):
    shutil.copyfile(config.DB_FILE_ARTICLES, backup_path)

# Restore the database from a backup file
def restore_db(backup_path):
    shutil.copyfile(backup_path, config.DB_FILE_ARTICLES)
    
# Export the database to a SQL file
def export_data(export_path):
    conn = connect_db()
    with open(export_path, 'w') as f:
        for line in conn.iterdump():
            f.write('%s\n' % line)
    conn.close()

    
# Create the necessary tables in the database
def create_tables():
    conn = connect_db()
    cursor = conn.cursor()
    
    # Articles table
    cursor.execute('''CREATE TABLE IF NOT EXISTS articles (
                       article_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       guid TEXT,
                       title TEXT, 
                       journal TEXT,
                       doi TEXT,
                       abstract TEXT, 
                       introduction TEXT, 
                       methodology TEXT, 
                       results TEXT, 
                       discussion TEXT, 
                       conclusion TEXT,
                       keywords TEXT,
                       user_input TEXT,
                       prompt TEXT,
                       add_date datetime DEFAULT CURRENT_TIMESTAMP
                       )''')
    
    # Authors table
    cursor.execute('''CREATE TABLE IF NOT EXISTS authors (
                       author_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       article_id INTEGER, 
                       guid TEXT,
                       number INTEGER,
                       name TEXT,
                       institution_name TEXT,
                       institution_address TEXT,
                       email TEXT,
                       add_date datetime DEFAULT CURRENT_TIMESTAMP,
                       FOREIGN KEY(article_id) REFERENCES articles(article_id) ON DELETE CASCADE
                       )''')
    
    # Citations table
    cursor.execute('''CREATE TABLE IF NOT EXISTS citations (
                       citation_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       article_id INTEGER, 
                       guid TEXT,   
                       number INTEGER,
                       content TEXT,
                       add_date datetime DEFAULT CURRENT_TIMESTAMP,
                       FOREIGN KEY(article_id) REFERENCES articles(article_id) ON DELETE CASCADE
                       )''')
    
    # Images table
    cursor.execute('''CREATE TABLE IF NOT EXISTS images (
                       image_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       article_id INTEGER,
                       guid TEXT,
                       number INTEGER,
                       title TEXT,
                       description TEXT,
                       keyword TEXT,
                       url TEXT,
                       local integer DEFAULT 0,
                       add_date datetime DEFAULT CURRENT_TIMESTAMP,
                       FOREIGN KEY(article_id) REFERENCES articles(article_id) ON DELETE CASCADE
                       )''')
    
    # Figures table (Fixed the missing closing parenthesis in the FOREIGN KEY constraint)
    cursor.execute('''CREATE TABLE IF NOT EXISTS figures (
                       figure_id INTEGER PRIMARY KEY AUTOINCREMENT,
                       article_id INTEGER,
                       guid TEXT,
                       number INTEGER,
                       title TEXT,
                       description TEXT,
                       url TEXT,
                       xaxis_title TEXT,
                       xaxis_value INTEGER,
                       yaxis_title TEXT,
                       yaxis_value INTEGER,
                       local integer DEFAULT 0,
                       img_base64 TEXT,
                       add_date datetime DEFAULT CURRENT_TIMESTAMP,
                       FOREIGN KEY(article_id) REFERENCES articles(article_id) ON DELETE CASCADE
                       )''')

    conn.commit()
    conn.close()

def executePredefinedStatement(tablename: str):
    conn = connect_db()
    cursor = conn.cursor()
    query = f"SELECT * FROM {tablename}"
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    cursor.close()
    conn.close()
    return {"columns": columns, "data": rows}


def executePreparedStatement(sql, values):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(sql, values)
    conn.commit()
    conn.close()
