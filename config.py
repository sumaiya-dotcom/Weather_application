

import os
from dotenv import load_dotenv

# Reads KEY=VALUE pairs from the .env file into environment variables.
load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
UNITS = "metric"  # Celsius and meters/second
HISTORY_FILE = "weather_history.txt"


def validate_config():
  
    if not API_KEY or API_KEY == "a1d5286dc0a9e7e8571ddba5fb7d265a":
        raise ValueError(
            "Missing API key. Open the .env file and set OPENWEATHER_API_KEY "
            "to the key from https://home.openweathermap.org/users/sign_up"
        )