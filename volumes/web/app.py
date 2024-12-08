from flask import Flask, render_template, request, jsonify, send_from_directory
import requests
import os
import markdown
import sqlite3
import json

app = Flask(__name__)

# Read environment variables
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2.1")
PUBLIC_BASE_URL = os.getenv("PUBLIC_BASE_URL", "http://localhost:3000")

DB_PATH = "/db/articles.db"
REQUIRED_KEYS = ["Abstract", "Introduction", "Methodology", "Results", "Discussion", "Conclusion", "References"]
MAX_RETRIES = 3

def ensure_database():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT,
        abstract TEXT,
        introduction TEXT,
        methodology TEXT,
        results TEXT,
        discussion TEXT,
        conclusion TEXT,
        refs TEXT
    )
    """)
    conn.commit()
    conn.close()

def generate_article_data(topic):
    """Send a prompt to the model to produce a structured JSON article."""
    prompt = (
        f"You are a helpful assistant. Write a detailed, peer-reviewed academic article about the following declaration: '{topic}'. "
        "The article must be supportive of the claim. "
        "You MUST return your answer as a strict JSON object with the following keys only: "
        "\"Abstract\", \"Introduction\", \"Methodology\", \"Results\", \"Discussion\", \"Conclusion\", and \"References\". "
        "Each key should map to a string, except References which should be a list of at least five credible APA-formatted references. "
        "No commentary outside of the JSON is allowed.\n"
        "{\n"
        "  \"Abstract\": \"...\",\n"
        "  \"Introduction\": \"...\",\n"
        "  \"Methodology\": \"...\",\n"
        "  \"Results\": \"...\",\n"
        "  \"Discussion\": \"...\",\n"
        "  \"Conclusion\": \"...\",\n"
        "  \"References\": [\"APA ref 1\", \"APA ref 2\", \"APA ref 3\", \"APA ref 4\", \"APA ref 5\"]\n"
        "}\n\n"
        "Make sure to only output valid JSON, no extra text outside the JSON."
    )

    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    if response.status_code != 200:
        return None, f"Ollama API returned status code {response.status_code}"

    response_json = response.json()
    model_response = response_json.get("response", "").strip()

    if not model_response:
        return None, "No content received from Ollama."

    # Attempt to parse JSON
    try:
        article_data = json.loads(model_response)
    except json.JSONDecodeError:
        return None, "The model did not return valid JSON."

    # Check for all required keys
    if not all(key in article_data for key in REQUIRED_KEYS):
        return None, "The model did not provide all required sections."

    # Check references format
    if not isinstance(article_data["References"], list) or len(article_data["References"]) < 5:
        return None, "References are not in the required format."

    return article_data, None

@app.route("/config", methods=["GET"])
def get_config():
    return jsonify({
        "publicBaseUrl": PUBLIC_BASE_URL,
        "ollamaModel": OLLAMA_MODEL
    })

@app.route("/generate", methods=["POST"])
def generate_article():
    data = request.json
    topic = data.get("topic")
    if not topic:
        return jsonify({"error": "Topic is required"}), 400

    # Try multiple times to get a valid response
    for attempt in range(MAX_RETRIES):
        article_data, error_message = generate_article_data(topic)
        if article_data is not None:
            # Valid data received, store it
            abstract = article_data["Abstract"]
            introduction = article_data["Introduction"]
            methodology = article_data["Methodology"]
            results = article_data["Results"]
            discussion = article_data["Discussion"]
            conclusion = article_data["Conclusion"]
            references_list = article_data["References"]
            refs_str = "\n".join(references_list)

            # Insert into the DB
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("""
                INSERT INTO articles (topic, abstract, introduction, methodology, results, discussion, conclusion, refs)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (topic, abstract, introduction, methodology, results, discussion, conclusion, refs_str))
            article_id = c.lastrowid
            conn.commit()
            conn.close()

            return jsonify({"url": f"/article/{article_id}"})
        else:
            # Invalid data, retry if attempts remain
            if attempt < MAX_RETRIES - 1:
                print(f"Attempt {attempt+1} failed: {error_message}. Retrying...")
            else:
                # Final attempt failed
                return jsonify({"error": f"Failed after {MAX_RETRIES} attempts: {error_message}"}), 500

@app.route("/retry", methods=["POST"])
def retry_article():
    topic = request.form.get("topic")
    if not topic:
        return jsonify({"error": "Topic is required to retry"}), 400
    return generate_article()

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/articles", methods=["GET"])
def show_all_articles():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT id, topic FROM articles ORDER BY id DESC")
        rows = c.fetchall()
        conn.close()

        articles_data = [dict(r) for r in rows]

        # If JSON requested
        if request.headers.get("Accept") == "application/json":
            return jsonify(articles_data)

        return render_template("all_articles.html", articles=articles_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/article/<int:article_id>")
def show_article(article_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT topic, abstract, introduction, methodology, results, discussion, conclusion, refs FROM articles WHERE id=?", (article_id,))
        row = c.fetchone()
        conn.close()
        if not row:
            return "Article not found", 404

        # Construct HTML content
        content = (
            f"<h2>Abstract</h2><p>{row['abstract']}</p>"
            f"<h2>Introduction</h2><p>{row['introduction']}</p>"
            f"<h2>Methodology</h2><p>{row['methodology']}</p>"
            f"<h2>Results</h2><p>{row['results']}</p>"
            f"<h2>Discussion</h2><p>{row['discussion']}</p>"
            f"<h2>Conclusion</h2><p>{row['conclusion']}</p>"
            f"<div class='references'>"
            f"<h2>References</h2>"
            + "".join(f"<p>{ref.strip()}</p>" for ref in row['refs'].split('\n'))
            + "</div>"
        )

        # Since we now trust the JSON structure, is_valid is always True
        is_valid = True
        missing_sections = []

        return render_template(
            "article.html",
            topic=row["topic"],
            content=content,
            is_valid=is_valid,
            missing_sections=missing_sections
        )
    except Exception as e:
        return f"Error: {e}", 500

@app.route('/articles/rename/<int:article_id>', methods=['PUT'])
def rename_article(article_id):
    try:
        data = request.get_json()
        new_name = data.get('new_name')
        if not new_name:
            return jsonify({'error': 'New name is required'}), 400

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('UPDATE articles SET topic = ? WHERE id = ?', (new_name, article_id))
        conn.commit()
        conn.close()

        return jsonify({'success': 'Article renamed successfully'}), 200
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'error': 'Failed to rename article'}), 500

@app.route('/articles/delete/<int:article_id>', methods=['DELETE'])
def delete_article(article_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('DELETE FROM articles WHERE id = ?', (article_id,))
        conn.commit()
        conn.close()

        return jsonify({'success': 'Article deleted successfully'}), 200
    except Exception as e:
        print(f'Error: {e}')
        return jsonify({'error': 'Failed to delete article'}), 500

@app.route("/db_maintenance", methods=["GET"])
def db_maintenance():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM articles ORDER BY id ASC")
    articles = c.fetchall()
    conn.close()

    return render_template("db_maintenance.html", articles=[dict(r) for r in articles])

@app.route("/run_sql", methods=["POST"])
def run_sql():
    sql_command = request.form.get("sql_command", "").strip()
    sql_result = None
    sql_columns = None
    sql_error = None

    if sql_command:
        try:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute(sql_command)

            if sql_command.lower().strip().startswith("select"):
                rows = c.fetchall()
                # Determine columns
                sql_columns = [description[0] for description in c.description]
                sql_result = rows
                conn.close()
            else:
                conn.commit()
                conn.close()

        except Exception as e:
            sql_error = str(e)

    # Re-display main table
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM articles ORDER BY id ASC")
    main_rows = c.fetchall()
    conn.close()

    articles = [dict(r) for r in main_rows]

    return render_template(
        "db_maintenance.html",
        articles=articles,
        sql_result=sql_result,
        sql_columns=sql_columns,
        sql_error=sql_error
    )

if __name__ == "__main__":
    ensure_database()
    app.run(host="0.0.0.0", port=5000)
