from dataclasses import dataclass
import os

@dataclass 
class config:
    IMAGE_API_URL = os.getenv('IMAGE_URL', 'https://api.unsplash.com/search/photos')
    IMAGE_API_KEY = os.getenv('IMAGE_API_KEY', 'your-api-key')  
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DB_FILE_ARTICLES = os.getenv("DB_FILE_ARTICLES", "db.db")
    DB_FILE_STORIES = os.getenv("DB_FILE_STORIES", "stories.db")
    OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://localhost:5000/ollama')
    OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'default')
    PUBLIC_BASE_URL = os.getenv('PUBLIC_BASE_URL', 'http://localhost:5000')
    FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'your-secret-key')
    MAX_OLLAMA_RETRIES = int(os.getenv('MAX_OLLAMA_RETRIES', 3))
    OLLAMA_RETRY_DELAY = int(os.getenv('OLLAMA_RETRY_DELAY', 2)) # seconds
    OLLAMA_TIMEOUT = int(os.getenv('OLLAMA_TIMEOUT', 360))