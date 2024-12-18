from dataclasses import dataclass
import os

@dataclass 
class config:
    IMAGE_URL = os.getenv('IMAGE_URL', 'https://api.unsplash.com/search/photos')
    IMAGE_API_KEY = os.getenv('IMAGE_API_KEY', 'your-api-key')  
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DB_FILE = os.getenv("DB_FILE", "db.db")
    OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://localhost:5000/ollama')
    OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'default')
    PUBLIC_BASE_URL = os.getenv('PUBLIC_BASE_URL', 'http://localhost:5000')
    FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'your-secret-key')
