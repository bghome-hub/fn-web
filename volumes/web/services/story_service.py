from typing import Optional
import json
import re
import uuid
import time
import logging

from repo.story_repo import StoryRepository
from services.ollama_service import sanitize_json_response

from services.image_service import find_journalist_image

from services.prompts import Prompt
from services import ollama_service
from services import image_service

from models.story import Story
from models.author import Author
from models.breakout import Breakout
from models.quote import Quote

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def create_story_from_ollama_response(response: dict) -> Story:
    logging.debug('Ollama response: %s', response)

    inner_response = response.get('response')
    logging.debug('Inner response: %s', inner_response)

    parsed_response = sanitize_json_response(inner_response)
    if parsed_response is None:
        logging.error("Failed to parse JSON response")
        raise ValueError("Failed to parse JSON response")

    logging.debug('Parsed response: %s', parsed_response)

    headline = parsed_response.get('headline')
    logging.debug('Headline: %s', headline)
    subheadline = parsed_response.get('subheadline')
    logging.debug('Subheadline: %s', subheadline)
    journalist_name = parsed_response.get('journalist_name')
    journalist_bio = parsed_response.get('journalist_bio')
    journalist_email = parsed_response.get('journalist_email')
    publication = parsed_response.get('publication')
    publication_date = time.strftime("%Y-%m-%d")
    title = parsed_response.get('title')
    content = parsed_response.get('content')
    keywords = parsed_response.get('keywords')
    user_input = parsed_response.get('user_input')
    prompt = parsed_response.get('prompt')

    # Add breakouts
    breakouts = []
    logging.debug('Breakouts: %s', breakouts)
    for i, breakout_data in enumerate(parsed_response.get("breakouts", [])):
        logging.debug('Breakout data: %s', breakout_data)
        breakouts.append(Breakout(
            number=i + 1,
            title=breakout_data.get('title'),
            content=breakout_data.get('content').strip()
        ))
    logging.debug('Breakouts: %s', breakouts)

    # Add quotes
    quotes = []
    for i, quote_data in enumerate(parsed_response.get("quotes", [])):
        logging.debug('Quote data: %s', quote_data)
        quotes.append(Quote(
            number=i + 1,
            content=quote_data.get('content'),
            speaker=quote_data.get('speaker'),
        ))
    logging.debug('Quotes: %s', quotes)

    # Get Journalist Photo

    story = Story(
        guid=response.get("guid", str(uuid.uuid4())),
        headline=headline,
        subheadline=subheadline,
        journalist_name=journalist_name,
        journalist_bio=journalist_bio,
        journalist_email=journalist_email,
        publication=publication,
        publication_date=publication_date,
        title=title,
        content=content,
        keywords=keywords,
        user_input=user_input,
        prompt=prompt,
        quotes=quotes,
        breakouts=breakouts,
        add_date=time.strftime("%Y-%m-%d")
    )

    logging.debug('Story: %s', story)

    return story

def fix_missing_line_breaks(content: str) -> str:
    pattern = r'(?<!\s)\.(?!\s)'

    # Replace such periods with a period followed by a newline
    processed_text = re.sub(pattern, '.\n', content)
    
    # Replace single quotes with double quotes
    quote_pattern = r"(?<=\s)'|'(?=\s|[.,!?])"
    processed_text = re.sub(quote_pattern, '"', processed_text)

    return processed_text


def save_story_from_ollama_response(headline_input: str) -> int:
    prompt = Prompt.story_prompt(headline_input)
    response = ollama_service.query_ollama(prompt)
    logging.debug('Ollama response: %s', response)

    response['prompt'] = prompt
    response['user_input'] = headline_input

    story = create_story_from_ollama_response(response)
    story.journalist_photo = find_journalist_image()
    story.content = fix_missing_line_breaks(story.content)
    story_id = StoryRepository.insert_full_story(story)

    return story_id

