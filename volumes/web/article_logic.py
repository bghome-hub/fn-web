import sqlite3
import os

DB_FILE = os.getenv("DB_FILE", "/db/db.db")

def fetch_article(article_id):
    """
    Fetch a specific article and its citations by article ID.
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Fetch the article
        cursor.execute('''
            SELECT id, topic, title, abstract, introduction, methodology, results, discussion, conclusion
            FROM articles WHERE id = ?
        ''', (article_id,))
        article_row = cursor.fetchone()

        if not article_row:
            return None  # Article not found

        # Fetch citations
        cursor.execute('''
            SELECT citation FROM citations WHERE article_id = ?
        ''', (article_id,))
        citations = [row[0] for row in cursor.fetchall()]

        conn.close()

        # Convert article data to a dictionary
        article = {
            "id": article_row[0],
            "topic": article_row[1],
            "title": article_row[2],
            "abstract": article_row[3],
            "introduction": article_row[4],
            "methodology": article_row[5],
            "results": article_row[6],
            "discussion": article_row[7],
            "conclusion": article_row[8],
            "citations": citations,
        }

        return article

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None

def fetch_last_20_articles():
    """
    Fetch the last 20 articles from the database.
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, title, abstract
            FROM articles
            ORDER BY id DESC
            LIMIT 20
        ''')

        articles = []
        for row in cursor.fetchall():
            articles.append({
                "id": row[0],
                "title": row[1],
                "abstract": row[2]
            })

        conn.close()
        return articles

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []

def fetch_all_articles():
    """Fetch all articles from the database, returning ID and title."""
    conn = sqlite3.connect(DB_FILE)  # Adjust the path if necessary
    cursor = conn.cursor()
    cursor.execute("SELECT id, title FROM articles")
    articles = [{'id': row[0], 'title': row[1]} for row in cursor.fetchall()]
    conn.close()
    return articles
