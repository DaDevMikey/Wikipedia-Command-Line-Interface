import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DEFAULT_LANGUAGE = "en"
    API_ENDPOINT = "https://api.wikipedia.org/w/api.php"
    USER_AGENT = "Wiki-CLI/1.0.0 (https://github.com/yourusername/wiki-cli)"
    CACHE_DIR = os.path.expanduser("~/.cache/wiki-cli")
    HISTORY_FILE = os.path.join(CACHE_DIR, "history")
    MAX_HISTORY = 1000
    
    @classmethod
    def get_api_url(cls, lang):
        return f"https://{lang}.wikipedia.org/w/api.php"
