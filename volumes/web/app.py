from flask import Flask, render_template, request, jsonify, send_from_directory
import requests
import os
import markdown
import sqlite3

app = Flask(__name__)

# Read environment variables
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")  # Backend only
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2.1")
PUBLIC_BASE_URL = os.getenv("PUBLIC_BASE_URL", "http://localhost:3000")

DB_PATH = "/db/articles.db"

# Configuration endpoint to serve environment variables to the frontend
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

    try:
        # Prepare the prompt for Ollama
        prompt = (
            f"Write a detailed, peer-reviewed academic article about the following declaration: '{topic}'. "
            "The article must be supportive of the claim made by the topic. "
            "You must make bold, assertive claims to support the topic. "
            "The article MUST have sections titled: Abstract, Introduction, Methodology, Results, Discussion, Conclusion, and References. "
            "You MUST Use markdown formatting with headings for each section. "
            "You MUST cite at least five credible sources in APA format. "
            "Do not provide any personal commentary."
        )

        # Send request to Ollama
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            }
        )

        if response.status_code != 200:
            return jsonify({"error": f"Ollama API returned status code {response.status_code}"}), 500

        response_json = response.json()
        article_content = response_json.get("response", "").strip()

        if not article_content:
            return jsonify({"error": "No content received from Ollama."}), 500

        # Convert the article content from markdown to HTML
        html_content = markdown.markdown(article_content, extensions=['extra', 'toc', 'codehilite'])

        # Save article in SQLite database
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO articles (topic, content) VALUES (?, ?)", (topic, html_content))
        article_id = c.lastrowid
        conn.commit()
        conn.close()

        return jsonify({"url": f"/article/{article_id}"})

    except Exception as e:
        print(f"Error: {e}")  # Log the error for debugging
        return jsonify({"error": str(e)}), 500

# Serve static files (if necessary, e.g., for non-template files)
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

# Serve the homepage
@app.route("/")
def home():
    return render_template("index.html")

# List all articles
@app.route("/articles", methods=["GET"])
def show_all_articles():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT id, topic FROM articles ORDER BY id DESC")
        articles = c.fetchall()
        conn.close()

        # Check if the request expects JSON
        if request.headers.get("Accept") == "application/json":
            # Return articles as JSON for API calls
            return jsonify([{"id": row[0], "topic": row[1]} for row in articles])

        # Render HTML page for browser visits
        return render_template("all_articles.html", articles=articles)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# View a specific article
@app.route("/article/<int:article_id>")
def view_article(article_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT topic, content FROM articles WHERE id=?", (article_id,))
        row = c.fetchone()
        conn.close()
        if not row:
            return "Article not found", 404
        topic, content = row
        return render_template("article.html", topic=topic, content=content)
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
