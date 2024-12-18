import json
import requests
import time
from config import config

# Define the function to generate an article using the Ollama model
def query_ollama(topic, max_retries=3):
    """Send a prompt to the Ollama model to produce a structured JSON article."""
    prompt = (
        f"Write a detailed, peer-reviewed academic article about the following topic: '{topic}'.\n"
        "The article must affirm the topic and provide a comprehensive overview of the subject matter.\n"
        "The article must be scholarly, realistic, and well-researched, with a clear structure and logical flow.\n"
        "The sources and authors must be credible, realistic, and authoritative. Author data MUST NOT be generic.\n"
        "Also provide a keyword related to the topic for image search.\n"
        "Return the following data in the exact JSON structure below. Ensure that all fields are populated.\n\n"
        'Return the output in JSON format as shown below:\n'
        '''{
          "journal": "string: the name of the journal",
          "doi": "string: the DOI of the article",
          "title": "string: the title of the article",
          "abstract": "string: brief summary of the article",
          "introduction": "string: introduction to the article",
          "methodology": "string: description of research methods",
          "results": "string: summary of research findings",
          "discussion": "string: discussion of results and implications",
          "conclusion": "string: summary of conclusions",
          "keywords": [
          { "keyword": "string: keyword 1 related to the topic for image search" }
          { "keyword": "string: keyword 2 related to the topic for image search" }
          ],
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
              "name": "string: <realistic, random name>",
              "institution_name": "string: <realistic, relevant insitution name>",
              "institution_address": "string: <realistic,  institution address",
              "email": "string: <realistic author email>"
            },
            {
              "name": "string: <realistic, random name>",
              "institution_name": "string: <realistic, relevant insitution name>",
              "institution_address": "string: <realistic,  institution address",
              "email": "string: <realistic author email>"
            },
            "figures": [
            {
              "description: "string: description of figure 1 ",
              "xaxis_title": "string: title of x-axis 1",
              "xaxis_value": "integer: value of x-axis 1",
              "yaxis_title": "string: title of y-axis 1",
              "yaxis_value": "integer: value of y-axis 1"
            },
                        {
              "description: "string: description of figure 2",
              "xaxis_title": "string: title of x-axis 2",
              "xaxis_value": "integer: value of x-axis 2",
              "yaxis_title": "string: title of y-axis 2",
              "yaxis_value": "integer: value of y-axis 2"
            }
          ]
        }'''
        "Please provide the responses in the exact structure shown above, ensuring that the APA sources are properly formatted with author(s), title, journal name, volume, issue, and year."
    )

    retries = 0
    while retries < max_retries:
        try:
            response = requests.post(
                f"{config.OLLAMA_URL}/api/generate",
                json={
                "model": config.OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
              })
          
            if response.status_code == 200:
                response_data = json.loads(response.json().get('response', '{}'))

                if response_data:
                    # Insert the Prompt and Topic into the response data
                    response_data['prompt'] = prompt
                    response_data['input'] = topic

                    return response_data
                else:
                    raise ValueError("Invalid response from Ollama")
        
            else: 
                raise Exception(f"Error in Ollama request: {response.text}")
    
        except Exception as e:
            error_messsage = str(e)
            if "Expecting value" in error_messsage:
                retries += 1
                time.sleep(2)
                continue # retry
            raise Exception(f"Error in Ollama request: {error_messsage}")
    raise Exception(f"Max retries exceeded for Ollama request.")