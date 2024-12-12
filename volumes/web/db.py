from titlecase import titlecase
import os
import sqlite3

DB_FILE = os.getenv("DB_FILE", "/db/db.db")

def init_db():
    try:
        os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Create Articles Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                title TEXT NOT NULL,
                abstract TEXT,
                introduction TEXT,
                methodology TEXT,
                results TEXT,
                discussion TEXT,
                conclusion TEXT
            )
        ''')

        # Create Citations Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS citations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                article_id INTEGER,
                citation TEXT,
                FOREIGN KEY (article_id) REFERENCES articles (id)
            )
        ''')

        # Create Authors Table
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS authors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,   
                article_id INTEGER,
                author_name TEXT,
                FOREIGN KEY (article_id) REFERENCES articles (id)
            )
        ''')

        # Create Images Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                search_term TEXT NOT NULL,
                image_url TEXT NOT NULL,
                article_id INTEGER,
                FOREIGN KEY (article_id) REFERENCES articles (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")

def execute_sql_query(sql_query):
    """Executes the provided SQL query against the database."""
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

# Save Article Data to Database
def save_article_to_db(topic, article_data):
    """Save generated article data and citations to the database."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Capitalize
        title = titlecase(topic)

        # Insert into Articles Table
        cursor.execute('''
            INSERT INTO articles (topic, title, abstract, introduction, methodology, results, discussion, conclusion)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            topic, title, article_data["abstract"], article_data["introduction"],
            article_data["methodology"], article_data["results"], article_data["discussion"],
            article_data["conclusion"]
        ))

        # Get the article's ID
        article_id = cursor.lastrowid

        # Insert into Citations Table
        for citation in article_data["citations"]:
            cursor.execute('''
                INSERT INTO citations (article_id, citation)
                VALUES (?, ?)
            ''', (article_id, citation))

        conn.commit()
        conn.close()
        return {"status": "success", "article_id": article_id}, None

    except Exception as e:
        return None, f"Database error: {str(e)}"


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


def get_article_part(fields=None, conditions=None):
    """
    Fetch articles from the database with specified fields and optional conditions.

    :param fields: List of fields to retrieve. Defaults to ['id', 'title', 'abstract'].
    :param conditions: Dictionary of conditions {field_name: value} for the WHERE clause.
    :return: List of dictionaries representing articles.
    """
    # Default fields if none are specified
    if fields is None:
        fields = ['id', 'title', 'abstract', 'introduction', 'methodology', 'results', 'discussion', 'conclusion']
    
    # Allowed fields to prevent SQL injection
    allowed_fields = {
        'id', 'title', 'summary', 'abstract', 'introduction',
        'methodology', 'results', 'discussion', 'conclusion'
    }
    invalid_fields = set(fields) - allowed_fields
    if invalid_fields:
        raise ValueError(f"Invalid fields requested: {invalid_fields}")
    
    # Safely construct the SELECT clause
    field_str = ', '.join(fields)
    query = f"SELECT {field_str} FROM articles"
    
    # List for query parameters
    params = []
    
    # Build WHERE clause if conditions are provided
    if conditions:
        # Validate condition fields
        invalid_condition_fields = set(conditions.keys()) - allowed_fields
        if invalid_condition_fields:
            raise ValueError(f"Invalid condition fields: {invalid_condition_fields}")
        
        # Construct WHERE clause with placeholders
        where_clauses = []
        for field, value in conditions.items():
            where_clauses.append(f"{field} = ?")
            params.append(value)
        where_clause = " AND ".join(where_clauses)
        query += f" WHERE {where_clause}"
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    # Convert rows to list of dictionaries
    articles = [dict(zip(fields, row)) for row in rows]
    return articles


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


# function to accept a search term and save the image url to the database
def save_image_url(article_id, search_term, image_url):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO images (article_id, image_url) VALUES (?, ?)", (search_term, image_url))
    conn.commit()
    conn.close()
    return True