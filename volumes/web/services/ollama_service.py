import json
import re
from typing import Union, Dict, Any, Optional
import requests
from config import config
import logging

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

    # Remove code fences if present
    response = response.strip().strip('```')
    logging.debug("Removed code fences.")
    
    # Step 2: Remove control characters except for common whitespace
    response = re.sub(r'[\x00-\x1F\x7F]+', '', response)
    logging.debug("Removed non-printable control characters.")

    # Step 3: Remove trailing commas before closing braces or brackets
    response = re.sub(r',\s*([\}\]])', r'\1', response)
    logging.debug("Removed trailing commas before closing braces/brackets.")

    # Step 4: Fix escaped characters (e.g., fix incorrect escaping of apostrophes)
    response = response.replace("\\'", "'")
    logging.debug("Fixed escaped characters.")

    # Step 5: Fix missing commas between JSON elements
    response = re.sub(r'"\s*([\{\[])\s*"', r'",\1"', response)
    logging.debug("Fixed missing commas between JSON elements.")

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



def query_ollama(prompt: str, decode: bool = True) -> Union[Dict[str, Any], requests.Response]:
    
    url = f"{config.OLLAMA_URL}/api/generate"
    payload = {
        "model": config.OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
    }

    Headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, headers=Headers, json=payload)
        response.raise_for_status()
        if decode:
            try:       
                data = response.json()
                return data
            except json.decoder.JSONDecodeError:
                return None
        else:
            return response
        
    except requests.exceptions.RequestException as e:
        return None






