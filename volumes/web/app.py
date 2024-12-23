from flask import Flask, request, jsonify, render_template, flash, redirect, url_for, send_file
import os, time
from config import config
from services import db_service as db
from services.db_utils import ensure_tables_created

from models import article, citation, figure, image
from repo.article_repo import ArticleRepository
from services.article_service import save_article_from_ollama_response

app = Flask(__name__)
app.secret_key = config.FLASK_SECRET_KEY
app.PUBLIC_BASE_URL = config.PUBLIC_BASE_URL

@app.before_request
def before_request():
    ensure_tables_created()

@app.route('/')
def index():
    recent_articles = ArticleRepository.fetch_last_x_articles(5)
    return render_template('index.html', recent_articles=recent_articles)

@app.route('/db_utils', methods=['GET', 'POST'])
def db_utils():
    rows = None
    if request.method == 'POST':
        tablename = request.form.get('table_name')
        rows = db.executePredefinedStatement(tablename)
    return render_template('admin/db_utils.html', results=rows)

@app.route('/tos')
def tos():
    return render_template('tos.html')

@app.route('/all_articles')
def all_articles():
    articles = ArticleRepository.fetch_all()
    return render_template('articles/all_articles.html', articles=articles)

# get count of articles
@app.route('/count_articles')
def count_articles():
    count = ArticleRepository.count_articles()
    return jsonify(count)

# create article route
@app.route('/generate_article', methods=['POST'])
def generate_article():
    
    # Get the topic from the form
    topic = request.form.get('topic')

    if not topic:
        flash('Please provide a topic for the article.', 'error')
        return redirect(url_for('index'))

    # Save the article
    try:
        article_id = save_article_from_ollama_response(topic)
        flash('Article generated successfully!', 'success')
        return redirect(url_for('view_article', article_id=article_id))
    
    except Exception as e:
        flash(f'Error generating article: {str(e)}', 'error')
        return redirect(url_for('index'))

# view_article route
@app.route('/view_article/<int:article_id>')
def view_article(article_id):
    article = ArticleRepository.fetch_by_article_id(article_id)
    return render_template('articles/article.html', article=article)
    
# delete_article route
@app.route('/delete_article/<int:article_id>', methods=['DELETE'])
def delete_article(article_id):
    ArticleRepository.delete(article_id)
    return jsonify({'success': True})

# backup and restore routes
@app.route('/db_backup', methods=['GET'])
def db_backup():
    backup_path = f'/tmp/db_backup_{int(time.time())}.db'
    db.backup_db(backup_path)
    return send_file(backup_path, as_attachment=True)

@app.route('/db_restore', methods=['POST'])
def db_restore():
    backup_file = request.files['backup_file']
    backup_path = os.path.join('/tmp', backup_file.filename)
    backup_file.save(backup_path)
    try:
        db.restore_db(backup_path)
        flash('Database restore successful!', 'success')
    except Exception as e:
        flash(f'Error during restore: {str(e)}', 'error')
    return redirect(url_for('db_utils'))

if __name__ == '__main__':
    # Initialize the database tables if not already created
    db.create_tables()

    # Start the Flask app
    app.run(debug=True)