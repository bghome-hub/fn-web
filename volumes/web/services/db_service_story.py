# Description: This file contains the functions to interact with the SQLite database.
import sqlite3
from titlecase import titlecase
import shutil

from config import config 

# Connect to the SQLite database
def connect_db():
    conn = sqlite3.connect(config.DB_FILE_STORIES)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn

# Create the necessary tables in the database
def create_tables():
    conn = connect_db()
    cursor = conn.cursor()
    
    # Stories table
    cursor.execute('''CREATE TABLE IF NOT EXISTS stories (
                       story_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       guid TEXT,
                       headline TEXT, 
                       publication TEXT,
                       publication_date TEXT,
                       keywords TEXT,
                       user_input TEXT,
                       prompt TEXT,
                       add_date datetime DEFAULT CURRENT_TIMESTAMP
                       )''')
    
    # Authors table
    cursor.execute('''CREATE TABLE IF NOT EXISTS authors (
                       author_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       story_id INTEGER, 
                       guid TEXT,
                       number INTEGER,
                       name TEXT,
                       affiliation TEXT,
                       email TEXT,
                       add_date datetime DEFAULT CURRENT_TIMESTAMP,
                       FOREIGN KEY(story_id) REFERENCES stories(story_id) ON DELETE CASCADE
                       )''')
    
    # Quotes table
    cursor.execute('''CREATE TABLE IF NOT EXISTS quotes (
                       quote_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       story_id INTEGER, 
                       guid TEXT,
                       number INTEGER,
                       description TEXT,
                       content TEXT,
                       speaker TEXT,
                       add_date datetime DEFAULT CURRENT_TIMESTAMP,
                       FOREIGN KEY(story_id) REFERENCES stories(story_id) ON DELETE CASCADE
                   )''')

    # Breakout Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS breakouts (
                       breakout_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       story_id INTEGER, 
                       guid TEXT,
                       number INTEGER,
                       title TEXT,
                       content TEXT,
                       add_date datetime DEFAULT CURRENT_TIMESTAMP,
                       FOREIGN KEY(story_id) REFERENCES stories(story_id) ON DELETE CASCADE
                     )''')
    
    conn.commit()
    conn.close()