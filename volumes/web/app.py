from flask import Flask, request, jsonify
import models
import ollama
import article
import image
import citation
import figure
import db

app = Flask(__name__)

@app.route('/create-article', methods=['POST'])
def create_article():
    topic = request.json.get('topic')
    
    # Step 1: Query Ollama model for the data
    try:
        ollama_data = ollama.query_ollama(topic)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    # Step 2: Validate the response from Ollama
    if not ollama.validate_ollama_response(ollama_data):
        return jsonify({'error': 'Incomplete or invalid data from Ollama.'}), 400

    # Step 3: Create Article object and other related objects (authors, citations, etc.)
    new_article = article.create_article_from_data(ollama_data)
    
    # Step 4: Save the article and related objects (authors, citations, images, figures) to the database
    article.save_article_to_db(new_article)
    
    return jsonify({'message': 'Article created successfully'}), 201

if __name__ == '__main__':
    # Test generating an article for a specific topic
    topic = "Machine Learning in Healthcare"
    article = ollama.prompt_full_article(topic)

    # Accessing data from the article object
    print(article.abstract)  # Prints the abstract of the article
    print(article.authors)    # Prints the list of authors
    print(article.citations)  # Prints the list of citations
    db.create_tables()  # Ensure tables are created
    app.run(debug=True)
