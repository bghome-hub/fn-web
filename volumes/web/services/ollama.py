import json
import logging
from typing import Optional
from pydantic import ValidationError
from pydantic.error_wrappers import ValidationError
from config import config
from ollama import Client

from models.story import Story

def structured_story_query(prompt: str) -> Optional[Story]:

    url = f"{config.OLLAMA_URL}"
    logging.debug(f"URL: {url}")

    model = config.OLLAMA_MODEL
    logging.debug(f"Model: {model}")

    client = Client(url)
    logging.debug(f"Client: {client}")

    response = client.chat(
        messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ],
        model=model,
        stream=False,
        format=Story.model_json_schema()
    )

    logging.debug(f"prompt: {prompt}")
    logging.debug(f"response: {response.message.content}")

    try:
        story = Story.model_validate_json(response.message.content)
        print(story)
        return story
    except json.JSONDecodeError as e:
        logging.error(f"JSON decoding failed: {e}")
        return None
    except ValidationError as ve:
        logging.error(f"Validation error: {ve}")
        return None