import logging
from flask import Flask, request, jsonify, render_template, flash, redirect, url_for, send_file
import os, time
from config import config
from services import db_service_article as article_db
from services import db_service_story as story_db

from services.db_utils import ensure_tables_created

from models import article, citation, figure, image
from repo.article_repo import ArticleRepository
from repo.story_repo import StoryRepository

from services.article_service import save_article_from_ollama_response
from services.story_service import save_story_from_ollama_response

app = Flask(__name__)
app.secret_key = config.FLASK_SECRET_KEY
app.PUBLIC_BASE_URL = config.PUBLIC_BASE_URL

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.before_request
def before_request():
    logger.debug("Before request: Ensuring tables are created.")
    ensure_tables_created()

@app.route('/')
def index():
    logger.debug("Route '/' accessed.")
    try:
        recent_articles = ArticleRepository.fetch_last_x_articles(5)
        logger.debug(f"Fetched {len(recent_articles)} recent articles.")
        return render_template('index.html', recent_articles=recent_articles)
    except Exception as e:
        logger.error(f"Error fetching recent articles: {e}")
        flash("An error occurred while fetching recent articles.", "error")
        return render_template('index.html', recent_articles=[])

@app.route('/db_utils', methods=['GET', 'POST'])
def db_utils():
    logger.debug("Route '/db_utils' accessed with method: %s", request.method)
    rows = None
    if request.method == 'POST':
        tablename = request.form.get('table_name')
        logger.debug(f"Executing predefined statement for table: {tablename}")
        try:
            rows = article_db.executePredefinedStatement(tablename)
            logger.debug(f"Fetched {len(rows)} rows from table: {tablename}")
        except Exception as e:
            logger.error(f"Error executing statement on table {tablename}: {e}")
            flash(f"An error occurred while accessing table {tablename}.", "error")
    return render_template('admin/db_utils.html', results=rows)

@app.route('/tos')
def tos():
    logger.debug("Route '/tos' accessed.")
    return render_template('tos.html')

@app.route('/all_articles')
def all_articles():
    logger.debug("Route '/all_articles' accessed.")
    try:
        articles = ArticleRepository.fetch_all()
        logger.debug(f"Fetched {len(articles)} articles.")
        return render_template('articles/all_articles.html', articles=articles)
    except Exception as e:
        logger.error(f"Error fetching all articles: {e}")
        flash("An error occurred while fetching all articles.", "error")
        return render_template('articles/all_articles.html', articles=[])

@app.route('/all_stories')
def all_stories():
    logger.debug("Route '/all_stories' accessed.")
    try:
        stories = StoryRepository.fetch_all()
        logger.debug(f"Fetched {len(stories)} stories.")
        return render_template('stories/all_stories.html', stories=stories)
    except Exception as e:
        logger.error(f"Error fetching all stories: {e}")
        flash("An error occurred while fetching all stories.", "error")
        return render_template('stories/all_stories.html', stories=[])

# get count of articles
@app.route('/count_articles')
def count_articles():
    count = ArticleRepository.count_articles()
    return jsonify(count)

# create story route
@app.route('/generate_story', methods=['POST'])
def generate_story():
    
    # Get the topic from the form
    headline_input = request.form.get('headline_input')

    if not headline_input:
        flash('Please provide a topic for the story.', 'error')

    # Save the story
    try:
        story_id = save_story_from_ollama_response(headline_input)
        flash('Story generated successfully!', 'success')
        return redirect(url_for('view_story', story_id=story_id))
    
    except Exception as e:
        flash(f'Error generating story: {str(e)}', 'error')
        return redirect(url_for('index'))

#view_story route
@app.route('/view_story/<int:story_id>')
def view_story(story_id):
    story = StoryRepository.fetch_by_story_id(story_id)
    return render_template('stories/story.html', story=story)

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
    article_db.backup_db(backup_path)
    return send_file(backup_path, as_attachment=True)

@app.route('/db_restore', methods=['POST'])
def db_restore():
    backup_file = request.files['backup_file']
    backup_path = os.path.join('/tmp', backup_file.filename)
    backup_file.save(backup_path)
    try:
        article_db.restore_db(backup_path)
        flash('Database restore successful!', 'success')
    except Exception as e:
        flash(f'Error during restore: {str(e)}', 'error')
    return redirect(url_for('db_utils'))

if __name__ == '__main__':
    logger.info("Starting Flask application.")
    app.run(debug=True)