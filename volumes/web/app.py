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
        recent_stories = StoryRepository.fetch_last_x_stories(5)
        logger.debug(f"Fetched {len(recent_articles)} recent articles.")
        return render_template('index.html', recent_articles=recent_articles, recent_stories=recent_stories)
    except Exception as e:
        logger.error(f"Error fetching recent articles: {e}")
        flash("An error occurred while fetching recent articles.", "error")
        return render_template('index.html', recent_articles=[], recent_stories=[])

@app.route('/db_utils', methods=['GET', 'POST'])
def db_utils():
    logger.debug("Route '/db_utils' accessed with method: %s", request.method)
    rows = None
    if request.method == 'POST':
        tablename = request.form.get('table_name')
        logger.debug(f"Executing predefined statement for table: {tablename}")
        
        # Define which tables belong to which database
        articles_tables = {'articles', 'authors', 'citations', 'images', 'figures'}
        stories_tables = {'stories', 'quotes', 'breakouts'}

        try:
            if tablename in articles_tables:
                query_result = article_db.executePredefinedStatement(tablename)
                logger.debug(f"Executed query on Articles DB for table: {tablename}")
            elif tablename in stories_tables:
                query_result = story_db.executePredefinedStatement(tablename)
                logger.debug(f"Executed query on Stories DB for table: {tablename}")
            else:
                flash(f"Unknown table: {tablename}", "error")
                query_result = None
            
            if query_result:
                rows = query_result
        except Exception as e:
            logger.error(f"Error executing query on table {tablename}: {e}")
            flash(f"Error executing query: {e}", "error")
    
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

# delete_story route
@app.route('/delete_story/<int:story_id>', methods=['DELETE'])
def delete_story(story_id):
    StoryRepository.delete(story_id)
    return jsonify({'success': True})

# Backup database route
@app.route('/db_backup', methods=['GET'])
def db_backup():
    db_to_backup = request.args.get('db_backup')  # 'articles' or 'stories'
    if db_to_backup == 'articles':
        backup_path = f'/tmp/db_backup_articles_{int(time.time())}.db'
        article_db.backup_db(backup_path)
        logger.debug(f"Backing up Articles DB to {backup_path}")
    elif db_to_backup == 'stories':
        backup_path = f'/tmp/db_backup_stories_{int(time.time())}.db'
        story_db.backup_db(backup_path)
        logger.debug(f"Backing up Stories DB to {backup_path}")
    else:
        flash("Invalid database selection for backup.", "error")
        return redirect(url_for('db_utils'))
    
    return send_file(backup_path, as_attachment=True)

# Restore database route
@app.route('/db_restore', methods=['POST'])
def db_restore():
    db_to_restore = request.form.get('db_restore')  # 'articles' or 'stories'
    backup_file = request.files.get('backup_file')
    
    if not db_to_restore or not backup_file:
        flash("Missing database selection or backup file.", "error")
        return redirect(url_for('db_utils'))
    
    backup_filename = backup_file.filename
    backup_path = os.path.join('/tmp', backup_filename)
    backup_file.save(backup_path)
    logger.debug(f"Saved backup file to {backup_path} for restoring {db_to_restore} DB.")
    
    try:
        if db_to_restore == 'articles':
            article_db.restore_db(backup_path)
            logger.debug(f"Restored Articles DB from {backup_path}")
        elif db_to_restore == 'stories':
            story_db.restore_db(backup_path)
            logger.debug(f"Restored Stories DB from {backup_path}")
        else:
            flash("Invalid database selection for restore.", "error")
            return redirect(url_for('db_utils'))
        flash(f"Database '{db_to_restore}' restored successfully.", "success")
    except Exception as e:
        logger.error(f"Failed to restore {db_to_restore} DB: {e}")
        flash(f"Failed to restore {db_to_restore} DB: {e}", "error")
    finally:
        # Optionally remove the backup file after restoring
        if os.path.exists(backup_path):
            os.remove(backup_path)
            logger.debug(f"Removed temporary backup file {backup_path}")
    
    return redirect(url_for('db_utils'))

if __name__ == '__main__':
    logger.info("Starting Flask application.")
    app.run(debug=True)