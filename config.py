"""
config.py
---------
Project settings. API keys stay here (loaded from .env), not in weather.py.
"""

import os
from dotenv import load_dotenv

# Reads KEY=VALUE pairs from the .env file into environment variables.
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
UNITS = "metric"  # Celsius and meters/second
HISTORY_FILE = "weather_history.txt"


def validate_config():
    """Stop early if the API key is missing or still the placeholder."""
    if not API_KEY or API_KEY == "your_api_key_here":
        raise ValueError(
            "Missing API key. Open the .env file and set OPENWEATHER_API_KEY "
            "to the key from https://home.openweathermap.org/users/sign_up"
        )