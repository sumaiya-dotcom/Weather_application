

from config import validate_config
from weather import (
    WeatherError,
    compare_cities,
    fetch_weather,
    format_report,
    read_history,
    save_report,
)


def lookup_one_city():
    city = input("Enter city name: ").strip()
    if not city:
        print("Please type a city name.\n")
        return

    weather = fetch_weather(city)
    report = format_report(weather)
    print("\n" + report + "\n")
    save_report(report)
    print("Saved this report to weather_history.txt\n")


def lookup_several_cities():
    raw = input("Enter cities separated by commas (e.g. London, Paris, Tokyo): ").strip()
    cities = [name.strip() for name in raw.split(",") if name.strip()]

    if not cities:
        print("Please type at least one city.\n")
        return

    results = []
    for city in cities:
        try:
            weather = fetch_weather(city)
            results.append(weather)
            report = format_report(weather)
            print("\n" + report)
            save_report(report)
        except WeatherError as error:
            print(f"\nSkipped '{city}': {error}")

    if results:
        print("\n" + compare_cities(results) + "\n")


def show_history():
    print("\n" + read_history() + "\n")


def run():
    print("Weather Information Application")
    print("-" * 34)

    try:
        validate_config()
    except ValueError as error:
        print(error)
        return

    while True:
        print("1. Look up one city")
        print("2. Compare several cities")
        print("3. View saved history")
        print("4. Quit")
        choice = input("Choose 1-4: ").strip()

        if choice == "1":
            try:
                lookup_one_city()
            except WeatherError as error:
                print(f"\nError: {error}\n")
        elif choice == "2":
            lookup_several_cities()
        elif choice == "3":
            try:
                show_history()
            except WeatherError as error:
                print(f"\nError: {error}\n")
        elif choice in {"4", "quit", "exit", "q"}:
            print("Goodbye.")
            break
        else:
            print("Please choose 1, 2, 3, or 4.\n")


if __name__ == "__main__":
    run()