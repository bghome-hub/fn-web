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