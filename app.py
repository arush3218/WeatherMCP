from __future__ import annotations

import sys
import json
import requests
from typing import Any


WEATHER_API = "https://api.open-meteo.com/v1/forecast"


def validate_city(city: str) -> bool:
    if not city or not isinstance(city, str) or len(city.strip()) == 0:
        return False
    return True


def fetch_coordinates(city: str) -> dict[str, Any]:
    if not validate_city(city):
        raise ValueError(f"Invalid city: {city}")
    
    geocoding_api = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": city.strip(),
        "count": 1,
        "language": "en",
        "format": "json"
    }
    
    resp = requests.get(geocoding_api, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    
    if not data.get("results"):
        raise ValueError(f"City '{city}' not found")
    
    result = data["results"][0]
    return {
        "latitude": result.get("latitude"),
        "longitude": result.get("longitude"),
        "name": result.get("name"),
        "country": result.get("country"),
        "timezone": result.get("timezone")
    }


def fetch_weather(lat: float, lon: float, timezone: str) -> dict[str, Any]:
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m"
    }
    
    resp = requests.get(WEATHER_API, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    current = data.get("current", {})
    return {
        "temperature": current.get("temperature_2m"),
        "time": current.get("time")
    }


def build_response(coords: dict[str, Any], weather: dict[str, Any]) -> dict[str, Any]:
    return {
        "city": coords.get("name"),
        "country": coords.get("country"),
        "latitude": coords.get("latitude"),
        "longitude": coords.get("longitude"),
        "timezone": coords.get("timezone"),
        "temperature": weather.get("temperature"),
        "unit": "Celsius",
        "time": weather.get("time")
    }


def get_weather(city: str) -> dict[str, Any]:
    try:
        coords = fetch_coordinates(city)
        weather = fetch_weather(
            coords.get("latitude"),
            coords.get("longitude"),
            coords.get("timezone")
        )
        return build_response(coords, weather)
    except (ValueError, RuntimeError) as exc:
        raise RuntimeError(f"Weather lookup failed: {exc}") from exc


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    
    if not argv:
        print(json.dumps({"error": "City name required as argument"}), file=sys.stderr)
        return 1
    
    city = " ".join(argv)
    
    try:
        result = get_weather(city)
        print(json.dumps(result, indent=2))
        return 0
    except RuntimeError as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
