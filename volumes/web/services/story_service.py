from typing import Optional
import json
import re
import uuid
import time
import logging

from repo.story_repo import StoryRepository
#from services.ollama_service import sanitize_json_response
from services import ollama
from services.image_service import find_journalist_image, find_image_url

from services.prompts import Prompt
from services import image_service

from models.story import Story
from models.author import Author
from models.breakout import Breakout
from models.quote import Quote

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def get_story_image_url(keywords: str) -> Optional[str]:
    # if story has no photo url get an image from the first story.keywords
    # story.keywords is a string of comma separated keywords, get the first one

    if keywords is not None:
        keyword = keywords.split(",")
        photo_url = image_service.find_image(keyword)
    
    return photo_url

def create_story_from_ollama_response(headline_input: str) -> Story:
    prompt = Prompt.story_prompt_simple(headline_input)
    logging.debug(f"Prompt: {prompt}")
    story = ollama.structured_story_query(prompt)
    logging.debug(f"Story: {story}")
    
    return story

def save_story_from_ollama_response(headline_input: str) -> int:

    story = create_story_from_ollama_response(headline_input)
    
    attempt = 0
    max_attempts = 3

    # keep trying to get a story from Ollama until we get one and story.content is not None
    while story is None or story.content is None:
        logging.debug(f"Attempt {attempt} to get a story from Ollama")
        story = create_story_from_ollama_response(headline_input)
        attempt += 1
        if attempt >= max_attempts:
            break
        time.sleep(1)
        
    story.journalist_photo = find_journalist_image()
    story.photo_url = find_image_url(story.keywords)
    story_id = StoryRepository.insert_full_story(story)

    return story_id

