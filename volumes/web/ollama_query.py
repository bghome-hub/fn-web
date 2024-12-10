from titlecase import titlecase
import requests
import sqlite3
import json
import os

# Configuration
DB_FILE = os.getenv("DB_FILE", "/db/db.db")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama-service:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "default-model")

# Initialize SQLite Database
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

        conn.commit()
        conn.close()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")

# Generate Article Data
def generate_article_data(topic):
    """Send a prompt to the Ollama model to produce a structured JSON article."""
    prompt = (
        f"Write a detailed, peer-reviewed academic article about the following topic: '{topic}'. "
        "The article must be supportive of the claim. You may make extreme conclusions. "
        "No commentary is allowed. "
        "You MUST return your answer as a strict JSON object with the following keys only: "
        "\"Abstract\", \"Introduction\", \"Methodology\", \"Results\", \"Discussion\", \"Conclusion\", and \"References\". "
        "You MUST return your response in the following JSON format:\n"
        "{\n"
        "  \"Abstract\": \"...\",\n"
        "  \"Introduction\": \"...\",\n"
        "  \"Methodology\": \"...\",\n"
        "  \"Results\": \"...\",\n"
        "  \"Discussion\": \"...\",\n"
        "  \"Conclusion\": \"...\",\n"
        "  \"References\": [\"<APA ref 1>\", \"<APA ref 2>\", \"<APA ref 3>\", \"<APA ref 4>\", \"<APA ref 5>\"]\n"
        "}\n\n"
    )

    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout = 180 # seconds
        )

        if response.status_code != 200:
            return None, f"Ollama API returned status code {response.status_code}: {response.text}"

        # Parse Response
        data = response.json()
        text_response = json.loads(data['response'])

        # Verify required keys are present
        required_keys = ["Abstract", "Introduction", "Methodology", "Results", "Discussion", "Conclusion", "References"]
        missing_keys = [key for key in required_keys if key not in text_response]
        if missing_keys:
            return None, f"Missing keys in response: {', '.join(missing_keys)}"

        # Extract Article Sections
        article_data = {
            "abstract": text_response.get("Abstract"),
            "introduction": text_response.get("Introduction"),
            "methodology": text_response.get("Methodology"),
            "results": text_response.get("Results"),
            "discussion": text_response.get("Discussion"),
            "conclusion": text_response.get("Conclusion"),
            "citations": text_response.get("References", [])
        }

        return article_data, None

    except Exception as e:
        return None, f"Error communicating with Ollama API: {str(e)}"

# Save Article Data to Database
def save_to_database(topic, article_data):
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
            topic, topic, article_data["abstract"], article_data["introduction"],
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
