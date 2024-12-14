from flask import Flask, request, jsonify, render_template
import article_logic
import db

app = Flask(__name__)

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


@app.route('/all_articles')
def all_articles():
    articles = article_logic.get_all_articles()
    return render_template('articles/all_articles.html', articles=articles)

# get count of articles
@app.route('/count_articles')
def count_articles():
    count = article_logic.get_count_of_articles()
    return jsonify(count)

# create article route
@app.route('/create_article', methods=['POST'])
def create_article():
    topic = request.form.get('topic')
    if not topic:
        return jsonify({'error': 'Topic is required!'}), 400
    
    try:
        article = article_logic.create_article_from_topic(topic)
        article_logic.save_article_to_db(article)
        return jsonify({'message': 'Article created successfully!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# view_article route
@app.route('/view_article/<int:id>')
def view_article(id):
    article = article_logic.get_article_by_id(id)
    return render_template('articles/article.html', article=article)
    
if __name__ == '__main__':
    # Initialize the database tables if not already created
    db.create_tables()

    # Start the Flask app
    app.run(debug=True)