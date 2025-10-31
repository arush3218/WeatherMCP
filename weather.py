"""Weather fetcher using Open-Meteo API."""
import requests
from datetime import datetime
from typing import Dict, Optional


# City coordinates
CITY_COORDS = {
    "bangalore": {"lat": 12.9716, "lon": 77.5946},
    "delhi": {"lat": 28.7041, "lon": 77.1025}
}


def get_current_weather(city: str) -> Optional[Dict]:
    """
    Fetch current weather for a given city.
    
    Args:
        city: City name (bangalore or delhi)
        
    Returns:
        Dictionary with temperature and time, or None if error
    """
    city_lower = city.lower()
    
    if city_lower not in CITY_COORDS:
        return {
            "error": f"City '{city}' not supported. Available: bangalore, delhi"
        }
    
    coords = CITY_COORDS[city_lower]
    
    try:
        # Open-Meteo API - free, no API key required
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": coords["lat"],
            "longitude": coords["lon"],
            "current": "temperature_2m",
            "timezone": "auto"
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        current = data.get("current", {})
        
        return {
            "city": city.title(),
            "temperature": current.get("temperature_2m"),
            "unit": "°C",
            "time": current.get("time"),
            "timezone": data.get("timezone", "UTC")
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to fetch weather: {str(e)}"
        }
    except Exception as e:
        return {
            "error": f"Unexpected error: {str(e)}"
        }
