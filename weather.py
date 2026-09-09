"""
weather.py
----------
Talks to the OpenWeatherMap REST API (GET) and to weather_history.txt.
"""

from datetime import datetime

import requests

from config import API_KEY, BASE_URL, HISTORY_FILE, UNITS


class WeatherError(Exception):
    """Friendly error for main.py to print."""


def fetch_weather(city_name):
    """
    GET current weather for one city.

    Request:  GET /data/2.5/weather?q=London&appid=KEY&units=metric
    Response: JSON dictionary with temperature, humidity, wind, etc.
    """
    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": UNITS,
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
    except requests.ConnectionError as error:
        raise WeatherError(
            "No internet connection. Check your Wi-Fi and try again."
        ) from error
    except requests.Timeout as error:
        raise WeatherError(
            "The weather service took too long to respond. Try again."
        ) from error
    except requests.RequestException as error:
        raise WeatherError(
            "Could not complete the request. Please try again later."
        ) from error

    if response.status_code == 401:
        raise WeatherError(
            "Invalid API key. Check OPENWEATHER_API_KEY in your .env file."
        )
    if response.status_code == 404:
        raise WeatherError(
            f"City not found: '{city_name}'. Check the spelling and try again."
        )
    if response.status_code == 429:
        raise WeatherError("Too many requests. Wait a minute and try again.")
    if not response.ok:
        raise WeatherError(
            f"Weather API failed with status {response.status_code}."
        )

    data = response.json()
    return parse_weather(data)


def parse_weather(data):
    """Turn the API JSON into a smaller dictionary we control."""
    try:
        return {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"],
        }
    except (KeyError, IndexError, TypeError) as error:
        raise WeatherError(
            "The API returned unexpected data."
        ) from error


def format_report(weather):
    """Turn one weather dictionary into readable text."""
    return (
        f"City: {weather['city']}, {weather['country']}\n"
        f"Temperature: {weather['temperature']} °C "
        f"(feels like {weather['feels_like']} °C)\n"
        f"Humidity: {weather['humidity']}%\n"
        f"Description: {weather['description']}\n"
        f"Wind Speed: {weather['wind_speed']} m/s"
    )


def save_report(report_text):
    """Append one report to the history file (write / append)."""
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    block = f"\n--- {stamp} ---\n{report_text}\n"

    try:
        with open(HISTORY_FILE, "a", encoding="utf-8") as file:
            file.write(block)
    except OSError as error:
        raise WeatherError(
            "Could not save the report to weather_history.txt."
        ) from error


def read_history():
    """Read the whole history file and return its text."""
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return "No history yet. Look up a city first."
    except OSError as error:
        raise WeatherError("Could not read weather_history.txt.") from error


def compare_cities(weather_list):
    """
    weather_list is a list of weather dictionaries.
    Returns a short comparison using a loop over that list.
    """
    if not weather_list:
        return "No cities to compare."

    hottest = weather_list[0]
    for item in weather_list:
        if item["temperature"] > hottest["temperature"]:
            hottest = item

    lines = ["City comparison:"]
    for item in weather_list:
        lines.append(
            f"  - {item['city']}: {item['temperature']} °C, {item['description']}"
        )
    lines.append(
        f"Hottest right now: {hottest['city']} ({hottest['temperature']} °C)"
    )
    return "\n".join(lines)