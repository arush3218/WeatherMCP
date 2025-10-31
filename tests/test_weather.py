"""Tests for weather fetcher."""
import pytest
import sys
from pathlib import Path

# Add parent directory to path to import weather module
sys.path.insert(0, str(Path(__file__).parent.parent))

from weather import get_current_weather, CITY_COORDS


def test_supported_cities():
    """Test that Bangalore and Delhi are supported."""
    assert "bangalore" in CITY_COORDS
    assert "delhi" in CITY_COORDS


def test_get_weather_bangalore():
    """Test fetching weather for Bangalore."""
    result = get_current_weather("bangalore")
    
    assert result is not None
    assert "error" not in result
    assert "city" in result
    assert result["city"] == "Bangalore"
    assert "temperature" in result
    assert "time" in result
    assert "unit" in result
    assert result["unit"] == "°C"


def test_get_weather_delhi():
    """Test fetching weather for Delhi."""
    result = get_current_weather("delhi")
    
    assert result is not None
    assert "error" not in result
    assert "city" in result
    assert result["city"] == "Delhi"
    assert "temperature" in result
    assert "time" in result


def test_unsupported_city():
    """Test handling of unsupported city."""
    result = get_current_weather("mumbai")
    
    assert result is not None
    assert "error" in result
    assert "not supported" in result["error"]


def test_case_insensitive():
    """Test that city names are case-insensitive."""
    result1 = get_current_weather("BANGALORE")
    result2 = get_current_weather("Bangalore")
    result3 = get_current_weather("bangalore")
    
    assert "error" not in result1
    assert "error" not in result2
    assert "error" not in result3
