"""Simple MCP server for weather data."""
from flask import Flask, request, jsonify
from weather import get_current_weather, CITY_COORDS


app = Flask(__name__)


@app.route('/')
def home():
    """Home endpoint with API info."""
    return jsonify({
        "service": "Weather MCP Server",
        "version": "1.0.0",
        "endpoints": {
            "/temperature": "Get temperature for a city (query param: city=bangalore or city=delhi)",
            "/all": "Get temperatures for all supported cities"
        },
        "supported_cities": list(CITY_COORDS.keys())
    })


@app.route('/temperature')
def get_temperature():
    """Get temperature for a specific city."""
    city = request.args.get('city')
    
    if not city:
        return jsonify({
            "error": "Missing 'city' query parameter",
            "example": "/temperature?city=bangalore"
        }), 400
    
    result = get_current_weather(city)
    
    if "error" in result:
        return jsonify(result), 404 if "not supported" in result["error"] else 500
    
    return jsonify(result)


@app.route('/all')
def get_all_temperatures():
    """Get temperatures for all supported cities."""
    results = {}
    
    for city in CITY_COORDS.keys():
        weather_data = get_current_weather(city)
        results[city] = weather_data
    
    return jsonify({
        "cities": results,
        "count": len(results)
    })


if __name__ == '__main__':
    print("🌤️  Weather MCP Server starting...")
    print("📍 Supported cities: Bangalore, Delhi")
    print("🌐 Server running on http://127.0.0.1:5000")
    app.run(debug=True, host='127.0.0.1', port=5000)
