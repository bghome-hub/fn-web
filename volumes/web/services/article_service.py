import json
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


# This function is responsible for generating an article from the Ollama response
def create_article_from_ollama_response(response: dict) -> Article:
    # Debugging: Print the response data
    print("Ollama Response:", response)
    
    # Parse the JSON string in the 'response' field
    parsed_response = json.loads(response['response'])
    
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
#    figures = []
#    for i, figure_data in enumerate(parsed_response.get('figures', [])):
#        figures.append(Figure(
#            number= i + 1,
#            description=figure_data.get('description', ''),
#            xaxis_title=figure_data.get('xaxis_title', ''),
#            xaxis_value=figure_data.get('xaxis_value', 0),
#            yaxis_title=figure_data.get('yaxis_title', ''),
#            yaxis_value=figure_data.get('yaxis_value', 0)
#        ))

    # Create the figures
    figures = []
    for i, figure_data in enumerate(parsed_response.get('figures', [])):
        figure = Figure(
            number=i + 1,
            description=figure_data.get('description', ''),
            xaxis_title=figure_data.get('xaxis_title', ''),
            xaxis_value=figure_data.get('xaxis_value', 0),
            yaxis_title=figure_data.get('yaxis_title', ''),
            yaxis_value=figure_data.get('yaxis_value', 0)
        )
        figure.figure_base64 = figure_service.create_chart(figure)
        figures.append(figure)

    # Create the images
    images = []
    for i, keyword in enumerate(parsed_response.get('keywords', '').split(',')):
        keyword = keyword.strip()
        
        # only search for max of 2 images
        if i < 2:
            image = image_service.find_image(keyword)

        if image:
            image.number = i + 1
            images.append(image)
        else:
            images.append(Image(
                keyword=keyword,
                image_id=i + 1
            ))


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