from flask import Flask, request, jsonify, render_template, flash, redirect, url_for, send_file
import os, time
from models.article import Article
import services.db as db

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')
app.PUBLIC_BASE_URL = os.getenv('PUBLIC_BASE_URL')

@app.route('/')
def index():
    recent_articles = Article.get_last_x_articles(5)
    return render_template('index.html', recent_articles=recent_articles)

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
        # Create an article from the topic
        article = Article.create_from_topic(topic)
        # Search for an image based on the topic
        article.search_image()
        # Save the article to the database
        article.save_to_db()
        flash(f'Article created successfully! <a href="/view_article/{article.id}">View Article</a>', 'success')
        return redirect(url_for('index'))
    
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