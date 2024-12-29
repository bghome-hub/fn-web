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
                       subheadline TEXT,
                       journalist_name TEXT,
                       journalist_bio TEXT,
                       journalist_email TEXT,
                       journalist_photo TEXT,
                       publication TEXT,
                       publication_date TEXT,
                       title TEXT,
                       content TEXT,
                       keywords TEXT,
                       photo_url TEXT,
                       user_input TEXT,
                       prompt TEXT,
                       add_date datetime DEFAULT CURRENT_TIMESTAMP
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

# Backup database
def backup_db(backup_path):
    try:
        shutil.copyfile(config.DB_FILE_STORIES, backup_path)
    except Exception as e:
        raise e

# Restore database
def restore_db(backup_path):
    try:
        shutil.copyfile(backup_path, config.DB_FILE_STORIES)
    except Exception as e:
        raise e


# Execute a predefined statement (e.g., SELECT * FROM table)
def executePredefinedStatement(tablename: str):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        query = f"SELECT * FROM {tablename}"
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        cursor.close()
        conn.close()
        return {"columns": columns, "data": rows}
    except Exception as e:
        raise e

# Export the database to a SQL file
def export_data(export_path):
    try:
        conn = connect_db()
        with open(export_path, 'w') as f:
            for line in conn.iterdump():
                f.write('%s\n' % line)
        conn.close()
    except Exception as e:
        raise e