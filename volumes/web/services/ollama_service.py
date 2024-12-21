import json
from typing import Union, Dict, Any
import requests
from config import config

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
    






