from flask import render_template, request
import os
import sqlite3

DB_FILE = os.getenv("DB_FILE", "/db/db.db")

def execute_sql_query(sql_query):
    """
    Executes the provided SQL query against the database.
    
    Parameters:
        sql_query (str): The SQL query to execute.
        
    Returns:
        dict: A dictionary containing the results and metadata.
    """
    try:
        with sqlite3.connect(DB_FILE) as conn:
            conn.row_factory = sqlite3.Row  # Enable accessing columns by name
            cursor = conn.cursor()
            cursor.execute(sql_query)

            # Determine the type of query
            if sql_query.strip().lower().startswith("select"):
                rows = cursor.fetchall()
                columns = rows[0].keys() if rows else []
                results = {
                    'columns': columns,
                    'rows': [tuple(row) for row in rows]
                }
                return {'results': results, 'error': None, 'affected_rows': None}
            else:
                conn.commit()
                affected_rows = cursor.rowcount
                return {'results': None, 'error': None, 'affected_rows': affected_rows}
    except sqlite3.Error as e:
        return {'results': None, 'error': str(e), 'affected_rows': None}
    except Exception as ex:
        return {'results': None, 'error': str(ex), 'affected_rows': None}

def get_all_articles():
    conn = sqlite3.connect(DB_FILE)  # Adjust the database name/path if necessary
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, summary FROM articles")
    articles = [
        {'id': row[0], 'title': row[1], 'summary': row[2]}
        for row in cursor.fetchall()
    ]
    conn.close()
    return articles

def rename_article_by_id(article_id, new_title):
    """
    Rename an article's title by its ID.
    Returns a tuple (success: bool, error_message: str).
    """
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE articles SET title = ? WHERE id = ?", (new_title, article_id))
            if cursor.rowcount == 0:
                return False, "Article not found."
            conn.commit()
        return True, ""
    except sqlite3.Error as e:
        return False, str(e)

def delete_article_by_id(article_id):
    """
    Delete an article by its ID.
    Returns a tuple (success: bool, error_message: str).
    """
    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            # Delete citations associated with the article first to maintain referential integrity
            cursor.execute("DELETE FROM citations WHERE article_id = ?", (article_id,))
            cursor.execute("DELETE FROM articles WHERE id = ?", (article_id,))
            if cursor.rowcount == 0:
                return False, "Article not found."
            conn.commit()
        return True, ""
    except sqlite3.Error as e:
        return False, str(e)