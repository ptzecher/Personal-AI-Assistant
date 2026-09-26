import requests


def get_weather(city: str) -> dict:
    """
    Gets the current weather for a city.

    Args:
        city: The name of the city, for example Athens or London.

    Returns:
        Current weather information for the city.
    """

    # Step 1: Convert city name -> coordinates
    geocoding_url = (
        "https://geocoding-api.open-meteo.com/v1/search"
    )

    geocoding_response = requests.get(
        geocoding_url,
        params={
            "name": city,
            "count": 1
        },
        timeout=10
    )

    geocoding_response.raise_for_status()

    geocoding_data = geocoding_response.json()

    if not geocoding_data.get("results"):
        raise ValueError(
            f"City '{city}' not found"
        )

    location = geocoding_data["results"][0]
    print(f"Location:{location}")

    latitude = location["latitude"]
    longitude = location["longitude"]


    # Step 2: Coordinates -> current weather
    weather_url = (
        "https://api.open-meteo.com/v1/forecast"
    )

    weather_response = requests.get(
        weather_url,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": [
                "temperature_2m",
                "apparent_temperature",
                "wind_speed_10m"
            ]
        },
        timeout=10
    )

    weather_response.raise_for_status()

    weather_data = weather_response.json()

    print(f"Weather data: {weather_data}")

    current = weather_data["current"]

    return {
        "city": location["name"],
        "country": location.get("country"),
        "temperature": current["temperature_2m"],
        "apparent_temperature":
            current["apparent_temperature"],
        "wind_speed": current["wind_speed_10m"]
    }