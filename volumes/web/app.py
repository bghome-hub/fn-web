import os
from flask import Flask, request, jsonify, render_template, abort, url_for
from ollama_query import init_db, generate_article_data, save_to_database
from article_logic import fetch_article, fetch_last_20_articles, fetch_all_articles
from db_utils import execute_sql_query, get_all_articles, rename_article_by_id, delete_article_by_id
from datetime import datetime

app = Flask(__name__)

# Initialize the database on startup
init_db()

# Index Route
@app.route('/')
def index():
    return render_template('index.html')

# Generate Article Endpoint
@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    topic = data.get("topic")

    if not topic:
        return jsonify({"error": "Topic is required"}), 400

    # Generate Article Data
    article_data, error = generate_article_data(topic)
    if error:
        return jsonify({"error": error}), 500

    # Save to Database
    result, error = save_to_database(topic, article_data)
    if error:
        return jsonify({"error": error}), 500

    return jsonify({"status": "success", "article_id": result["article_id"]}), 200

# Get Articles Endpoint
@app.route('/articles', methods=['GET'])
def get_articles():
    articles = fetch_last_20_articles()
    return jsonify(articles), 200

# View Specific Article
@app.route('/article/<int:article_id>')
def article(article_id):
    article = fetch_article(article_id)
    if not article:
        abort(404, description="Article not found")

    return render_template('article.html', article=article)
# All articles
@app.route('/all_articles')
def all_articles():
    """Display a page with all article IDs and titles."""
    articles = fetch_all_articles()
    current_year = datetime.now().year
    return render_template('all_articles.html', articles=articles, current_year=current_year)

# Rename Article Endpoint
@app.route('/articles/rename/<int:article_id>', methods=['PUT'])
def rename_article(article_id):
    """
    Rename an article by its ID.
    Expects JSON data with 'new_name'.
    """
    data = request.get_json()
    new_name = data.get('new_name')

    if not new_name:
        return jsonify({'error': 'New name is required.'}), 400

    success, error = rename_article_by_id(article_id, new_name)
    if success:
        return jsonify({'message': 'Article renamed successfully.'}), 200
    else:
        return jsonify({'error': error}), 400

# Delete Article Endpoint
@app.route('/articles/delete/<int:article_id>', methods=['DELETE'])
def delete_article(article_id):
    """
    Delete an article by its ID.
    """
    success, error = delete_article_by_id(article_id)
    if success:
        return jsonify({'message': 'Article deleted successfully.'}), 200
    else:
        return jsonify({'error': error}), 400


# New Route: DB Utilities Page
@app.route('/db_utils', methods=['GET'])
def db_utils():
    """Render the Database Utilities page."""
    current_year = datetime.now().year
    return render_template('db_utils.html', current_year=current_year, query=False)

# New Route: Execute SQL Query
@app.route('/execute_query', methods=['POST'])
def execute_query():
    """Handle the execution of SQL queries from the DB Utilities page."""
    sql_query = request.form.get('sql_query')

    if not sql_query:
        error = "No SQL query provided."
        return render_template('db_utils.html',
                               current_year=datetime.now().year,
                               query=True,
                               results=None,
                               error=error,
                               affected_rows=None)

    # Execute the SQL query using the db_utils module
    query_result = execute_sql_query(sql_query)

    return render_template('db_utils.html',
                           current_year=datetime.now().year,
                           query=True,
                           results=query_result['results'],
                           error=query_result['error'],
                           affected_rows=query_result['affected_rows'])

# Error Handler for 404
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', message=error.description), 404


# Run the Flask App
if __name__ == '__main__':
    debug_mode = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
