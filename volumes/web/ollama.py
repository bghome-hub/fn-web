
import requests
import json
import os

# Configuration
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama-service:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "default-model")

# Generate Article Data
def generate_article_data(topic):
    """Send a prompt to the Ollama model to produce a structured JSON article."""
    prompt = (
        f"Write a detailed, peer-reviewed academic article about the following topic: '{topic}'. "
        "The article must be supportive of the claim. You may make extreme conclusions. "
        "No commentary is allowed. "
        "You MUST return your answer as a strict JSON object with the following keys only: "
        "\"Abstract\", \"Introduction\", \"Methodology\", \"Results\", \"Discussion\", \"Conclusion\", and \"References\". "
        "You MUST return your response in the following JSON format:\n"
        "{\n"
        "  \"Abstract\": \"...\",\n"
        "  \"Introduction\": \"...\",\n"
        "  \"Methodology\": \"...\",\n"
        "  \"Results\": \"...\",\n"
        "  \"Discussion\": \"...\",\n"
        "  \"Conclusion\": \"...\",\n"
        "  \"References\": [\"<APA ref 1>\", \"<APA ref 2>\", \"<APA ref 3>\", \"<APA ref 4>\", \"<APA ref 5>\"]\n"
        "}\n\n"
    )

    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout = 180 # seconds
        )

        if response.status_code != 200:
            return None, f"Ollama API returned status code {response.status_code}: {response.text}"

        # Parse Response
        data = response.json()
        text_response = json.loads(data['response'])

        # Verify required keys are present
        required_keys = ["Abstract", "Introduction", "Methodology", "Results", "Discussion", "Conclusion", "References"]
        missing_keys = [key for key in required_keys if key not in text_response]
        if missing_keys:
            return None, f"Missing keys in response: {', '.join(missing_keys)}"

        # Extract Article Sections
        article_data = {
            "abstract": text_response.get("Abstract"),
            "introduction": text_response.get("Introduction"),
            "methodology": text_response.get("Methodology"),
            "results": text_response.get("Results"),
            "discussion": text_response.get("Discussion"),
            "conclusion": text_response.get("Conclusion"),
            "citations": text_response.get("References", [])
        }

        return article_data, None

    except Exception as e:
        return None, f"Error communicating with Ollama API: {str(e)}"

