import json
import re
import numpy as np
from repo.article_repo import ArticleRepository

from services.prompts import Prompt
from services import ollama_service
from services import image_service
from services import figure_service

from models.article import Article
from models.author import Author
from models.citation import Citation
from models.figure import Figure
from models.image import Image

import re
import json
import logging
from typing import Optional

def sanitize_json_response(response: str) -> Optional[dict]:
    """
    Sanitize and parse a potentially malformed JSON response.

    Args:
        response (str): The raw response string containing JSON data.

    Returns:
        Optional[dict]: The parsed JSON data if successful, else None.
    """
    # Configure logging
    logging.basicConfig(level=logging.DEBUG)
    
    # Step 1: Extract JSON content
    match = re.search(r"\{.*\}", response, re.DOTALL)
    if match:
        response = match.group(0)
        logging.debug("Extracted JSON content from response.")
    else:
        logging.error("No JSON object found in the response.")
        return None

    # Step 2: Remove control characters except for common whitespace
    response = re.sub(r'[\x00-\x1F\x7F]+', '', response)
    logging.debug("Removed non-printable control characters.")

    # Step 3: Remove triple backticks
    response = response.replace("```", "")
    logging.debug("Removed triple backticks.")

    # Step 4: Remove trailing commas before closing braces or brackets
    response = re.sub(r',\s*([\}\]])', r'\1', response)
    logging.debug("Removed trailing commas before closing braces/brackets.")

    # Step 5: Fix escaped characters (e.g., fix incorrect escaping of apostrophes)
    response = response.replace("\\'", "'")
    logging.debug("Fixed escaped characters.")

    # Optional Step: Remove any other known problematic patterns
    # For example, remove any extra commas, fix missing colons, etc.
    # This requires knowledge of the specific issues in the JSON.

    # Step 6: Attempt to parse the cleaned JSON
    try:
        sanitized_data = json.loads(response)
        logging.debug("JSON parsed successfully.")
        return sanitized_data
    except json.JSONDecodeError as e:
        logging.error(f"JSON parsing error: {e}")
        return None


# This function is responsible for generating an article from the Ollama response
def create_article_from_ollama_response(response: dict) -> Article:
    # Debugging: Print the response data
    print("Ollama Response:", response)

    inner_response = response.get('response')
    
    # Parse the JSON string in the 'response' field
    parsed_response = sanitize_json_response(inner_response)
    
    title = parsed_response.get('title')
    journal = parsed_response.get('journal')
    doi = parsed_response.get('doi')
    abstract = parsed_response.get('abstract')
    introduction = parsed_response.get('introduction')
    methodology = parsed_response.get('methodology')
    results = parsed_response.get('results')
    discussion = parsed_response.get('discussion')
    conclusion = parsed_response.get('conclusion')
    keywords = parsed_response.get('keywords')
    user_input = response.get('user_input')
    prompt = response.get('prompt')

    # Create the authors
    authors = []
    for i, author_data in enumerate(parsed_response.get('authors', [])):
        authors.append(Author(
            number= i + 1,
            name=author_data.get('name', ''),
            institution_name=author_data.get('institution_name', ''),
            institution_address=author_data.get('institution_address', ''),
            email=author_data.get('email', '')
        ))

    # Create the citations
    citations = []
    for i, citation_data in enumerate(parsed_response.get('citations', [])):
        citations.append(Citation(
            number= i + 1,
            content=citation_data.get('content', '').strip()
        ))

    
    # Create the figures
    figures = []
    for i, figure_data in enumerate(parsed_response.get('figures', [])):
        figure = Figure(
            number=i + 1,
            description=figure_data.get('description', ''),
            xaxis_title=figure_data.get('xaxis_title', ''),
            xaxis_value=np.random.randint(0, 60, 14),
            yaxis_title=figure_data.get('yaxis_title', ''),
            yaxis_value=np.random.randint(0, 30, 14)
        )
        figure.img_base64 = figure_service.create_chart(figure)
        figures.append(figure)


    # Create the images
    images = []
    for i, keyword in enumerate(parsed_response.get('keywords', '').split(',')):
        keyword = keyword.strip()

        image = image_service.find_image(keyword)
        if image is None:
            continue
        
        image.keyword = keyword
        image.number = i + 1
        images.append(image)


    # Create the Article object
    article = Article(
        title=title,
        journal=journal,
        doi=doi,
        abstract=abstract,
        introduction=introduction,
        methodology=methodology,
        results=results,
        discussion=discussion,
        conclusion=conclusion,
        keywords=keywords,
        user_input=user_input,
        prompt=prompt,
        authors=authors,
        citations=citations,
        figures=figures,
        images=images
    )

    return article


def save_article_from_ollama_response(topic: str) -> int:
    # pass the topic to the article prompt template
    prompt = Prompt.article_prompt(topic)
    response = ollama_service.query_ollama(prompt)
    
    response['prompt'] = prompt
    response['user_input'] = topic

    article = create_article_from_ollama_response(response)
    article_id =  ArticleRepository.insert_full_article(article)

    return article_id