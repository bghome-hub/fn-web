from flask import Flask, request, jsonify, render_template, flash
import os
from models import Article, Author, Citation, Figure, Image
import db

app = Flask(__name__)

app.secret_key = os.getenv('FLASK_SECRET_KEY')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/db_utils', methods=['GET', 'POST'])
def db_utils():
    results = None
    if request.method == 'POST':
        query_name = request.form.get('query_name')
        results = db.execute_predefined_query(query_name)
    return render_template('admin/db_utils.html', results=results)

@app.route('/tos')
def tos():
    return render_template('tos.html')

@app.route('/all_articles')
def all_articles():
    articles = Article.get_all()
    return render_template('articles/all_articles.html', articles=articles)

# get count of articles
@app.route('/count_articles')
def count_articles():
    count = Article.count()
    return jsonify(count)

# create article route
@app.route('/create_article', methods=['POST'])
def create_article():

    topic = request.form.get('topic')
    if not topic:
        return jsonify({'error': 'Topic is required!'}), 400
    
    try:
        article = Article.create_from_topic(topic)
        article.save_to_db()
        return jsonify({'message': 'Article created successfully!'}), 201
    
    except Exception as e:
        error_message = str(e)
        if("Max reties exceeded" in error_message):
            flash("Max retries exceeded for Ollama request.")
        else:
            flash(f"Error {error_message}", "error")
        return render_template('index.html'), 500

# view_article route
@app.route('/view_article/<int:id>')
def view_article(id):
    article = Article.get_by_id(id)
    return render_template('articles/article.html', article=article)
    
if __name__ == '__main__':
    # Initialize the database tables if not already created
    db.create_tables()

    # Start the Flask app
    app.run(debug=True)