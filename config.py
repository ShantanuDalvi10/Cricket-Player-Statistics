import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_KEY = os.getenv("API_KEY")
    SECRET_KEY = os.getenv("SECRET_KEY")

    API_BASE_URL = "https://api.cricketdatabase.com"
    SEARCH_ENDPOINT = "/v1/search"
    STATS_ENDPOINT = "/v1/players/{player_identifier}/stats"
    DEBUG = os.environ.get("DEBUG","False").lower() in ("true","1","yes")

    API_HEADERS = {
        "X-API-Key":API_KEY
    }
    API_TIMEOUT = 10

    @classmethod
    def validate(cls):
        if not cls.API_KEY:
            raise RuntimeError("API key is not found.")
        if not cls.SECRET_KEY:
            raise RuntimeError("Secret Key is not found.")


