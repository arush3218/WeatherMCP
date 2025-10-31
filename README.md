# Weather MCP Server 🌤️

A simple Model Context Protocol (MCP) server that fetches current temperature data for Bangalore and Delhi using the Open-Meteo API.

## Features

- ✅ Fetch current temperature for Bangalore and Delhi
- ✅ Returns temperature reading with timestamp
- ✅ No API key required (uses Open-Meteo free API)
- ✅ Simple REST API endpoints
- ✅ Error handling for network issues
- ✅ Unit tests with pytest

## Setup

### Install Dependencies

```powershell
pip install -r requirements.txt
```

## Running the Server

Start the Flask server:

```powershell
python app.py
```

The server will start on `http://127.0.0.1:5000`

## API Endpoints

### 1. Home / Info
```
GET /
```

Returns server information and available endpoints.

### 2. Get Temperature for a City
```
GET /temperature?city=bangalore
GET /temperature?city=delhi
```

**Response Example:**
```json
{
  "city": "Bangalore",
  "temperature": 24.5,
  "unit": "°C",
  "time": "2025-10-31T10:30",
  "timezone": "Asia/Kolkata"
}
```

### 3. Get All Temperatures
```
GET /all
```

Returns temperature data for all supported cities.

## Testing

Run the test suite:

```powershell
pytest tests/
```

Run tests with verbose output:

```powershell
pytest tests/ -v
```

## Usage Examples

### Using curl (PowerShell)

```powershell
# Get Bangalore temperature
curl http://127.0.0.1:5000/temperature?city=bangalore

# Get Delhi temperature
curl http://127.0.0.1:5000/temperature?city=delhi

# Get all cities
curl http://127.0.0.1:5000/all
```

### Using Python requests

```python
import requests

# Get temperature for Bangalore
response = requests.get('http://127.0.0.1:5000/temperature?city=bangalore')
data = response.json()
print(f"{data['city']}: {data['temperature']}°C at {data['time']}")
```

## Project Structure

```
WeatherMCP/
├── app.py              # Flask MCP server
├── weather.py          # Weather fetching logic
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── tests/
    └── test_weather.py # Unit tests
```

## API Data Source

This project uses the free [Open-Meteo API](https://open-meteo.com/) which requires no API key and provides weather data under the CC BY 4.0 license.

## Adding to VS Code as MCP Server

### Method 1: Using VS Code Settings (Recommended)

1. Open VS Code Settings (JSON):
   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
   - Type "Preferences: Open User Settings (JSON)"
   - Press Enter

2. Add the MCP server configuration to your `settings.json`:

```json
{
  "github.copilot.chat.mcp.servers": {
    "weather": {
      "command": "python",
      "args": [
        "c:\\Users\\arush\\OneDrive\\Desktop\\WeatherMCP\\mcp_server.py"
      ]
    }
  }
}
```

3. Restart VS Code or reload the window (`Ctrl+Shift+P` → "Developer: Reload Window")

### Method 2: Using Workspace Settings

1. The configuration is already in `.vscode/mcp-settings.json`
2. Copy the contents to your VS Code User settings as shown above

### Using the MCP Server in Copilot Chat

Once configured, you can use it in GitHub Copilot Chat:

```
@weather get temperature for bangalore
@weather get temperature for delhi
@weather get all temperatures
```

Or ask natural language questions:
```
What's the current temperature in Bangalore?
Show me the weather for Delhi
```

## Two Ways to Use This Project

### 1. As an HTTP REST API (Current `app.py`)
- Run: `python app.py`
- Access via: `http://127.0.0.1:5000`
- Use with curl, Postman, or any HTTP client

### 2. As an MCP Server for VS Code (`mcp_server.py`)
- Configure in VS Code settings (see above)
- Use with GitHub Copilot Chat
- Automatic integration with AI tools

## Notes

- Temperature is returned in Celsius (°C)
- The API uses coordinates: Bangalore (12.97°N, 77.59°E), Delhi (28.70°N, 77.10°E)
- Timestamps are in ISO 8601 format with automatic timezone detection
