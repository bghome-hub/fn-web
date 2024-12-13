import json
import requests
import os

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama-service:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "default-model")

def prompt_full_article(topic):
    """Send a prompt to the Ollama model to produce a structured JSON article."""
    prompt = (
        f"Write a detailed, peer-reviewed academic article about the following topic: '{topic}'.\n"
        "The article must affirm the topic and provide a comprehensive overview of the subject matter.\n"
        "The article must be scholarly, realistic, and well-researched, with a clear structure and logical flow.\n"
        "The sources and authors must be credible, realistic, and authoritative.\n"
        "Return the following data in the exact JSON structure below. Ensure that all fields are populated.\n\n"
        'Return the output in JSON format as shown below:\n'
        '''{
          "title": "string: the title of the article",
          "abstract": "string: brief summary of the article",
          "introduction": "string: introduction to the article",
          "methodology": "string: description of research methods",
          "results": "string: summary of research findings",
          "discussion": "string: discussion of results and implications",
          "conclusion": "string: summary of conclusions",
          "keyword": "string: keyword related to the topic for image search",
          "citations": [
            {
              "content": "string: APA-formatted source 1"
            },
            {
              "content": "string: APA-formatted source 2"
            },
            {
              "content": "string: APA-formatted source 3"
            },
            {
              "content": "string: APA-formatted source 4"
            },
            {
              "content": "string: APA-formatted source 5"
            }
          ],
          "authors": [
            {
              "name": "string: author name",
              "institution_name": "string: author institution",
              "institution_address": "string: author institution address",
              "email": "string: author email"
            },
            {
              "name": "string: author name",
              "institution_name": "string: author institution",
              "institution_address": "string: author institution address",
              "email": "string: author email"
            }
          ]
        }'''
        "Please provide the responses in the exact structure shown above, ensuring that the APA sources are properly formatted with author(s), title, journal name, volume, issue, and year."
    )

    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            }
        )
        
        if response.status_code == 200:
            response_data = json.loads(response.json().get('response', '{}'))

            # Insert the Prompt and Topic into the response data
            response_data['prompt'] = prompt
            response_data['input'] = topic

            return response_data
        
        else:
            raise Exception(f"Error querying Ollama: {response.text}")
    except Exception as e:
        raise Exception(f"Error in Ollama request: {str(e)}")
