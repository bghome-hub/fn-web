from typing import Optional
import json
import re
import time

from repo.story_repo import StoryRepository
from services.article_service import sanitize_json_response

from services.prompts import Prompt
from services import ollama_service
from services import image_service

from models.story import Story
from models.author import Author
from models.breakout import Breakout
from models.quote import Quote


def create_story_from_ollama_response(response: dict) -> Story:
    print('Ollama response:', response)

    inner_response = response.get('response')

    parsed_response = sanitize_json_response(inner_response)

    headline=parsed_response.get('headline')
    publication=parsed_response.get('publication')
    publication_date= time.strftime("%Y-%m-%d")
    title = parsed_response.get('title')
    content = parsed_response.get('content')
    keywords = parsed_response.get('keywords')
    user_input = response.get('user_input')
    prompt = response.get('prompt')

    # Add authors
    authors = []
    for i, author_data in enumerate(parsed_response.get("authors", [])):
        authors.append(Author(
            number=i + 1,
            name=author_data.get('name'),
            institution_name=author_data.get('institution_name'),
            institution_address=author_data.get('institution_address'),
            email=author_data.get('email')
        ))

    # Add breakouts
    breakouts =[]
    for i, breakout_data in enumerate(parsed_response.get("breakouts", [])):
        breakouts.append(Breakout(
            number=i + 1,
            title=breakout_data.get('title'),
            content=breakout_data.get('content').strip()
        ))

    quotes = []
    for i, quote_data in enumerate(parsed_response.get("quotes", [])):
        quotes.append(Quote(
            number=i + 1,
            content=quote_data.get('content'),
            author=quote_data.get('author')
        ))

    story = Story(
        headline=headline,
        publication=publication,
        publication_date=publication_date,
        title=title,
        content=content,
        keywords=keywords,
        user_input=user_input,
        prompt=prompt,
        authors=authors,
        breakouts=breakouts,
        quotes=quotes
    )

    return story

def save_story_from_ollama_response(headline_input: str) -> int:
    prompt = Prompt.story_prompt(headline_input)
    response = ollama_service.query_ollama(prompt)
    print('Ollama response:', response)

    response['prompt'] = prompt
    response['user_input'] = headline_input

    story = create_story_from_ollama_response(response)
    story_id = StoryRepository.insert_story(story)

    return story_id