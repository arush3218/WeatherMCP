"""
MCP Server implementation for Weather Service.
This provides a proper MCP protocol interface instead of HTTP REST API.
"""
import sys
import json
from weather import get_current_weather, CITY_COORDS


def send_response(response):
    """Send JSON response to stdout."""
    print(json.dumps(response))
    sys.stdout.flush()


def handle_request(request):
    """Handle incoming MCP requests."""
    method = request.get("method")
    params = request.get("params", {})
    
    if method == "tools/list":
        # List available tools
        return {
            "tools": [
                {
                    "name": "get_temperature",
                    "description": "Get current temperature for a city (Bangalore or Delhi)",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "city": {
                                "type": "string",
                                "description": "City name (bangalore or delhi)",
                                "enum": ["bangalore", "delhi"]
                            }
                        },
                        "required": ["city"]
                    }
                },
                {
                    "name": "get_all_temperatures",
                    "description": "Get current temperature for all supported cities",
                    "inputSchema": {
                        "type": "object",
                        "properties": {}
                    }
                }
            ]
        }
    
    elif method == "tools/call":
        tool_name = params.get("name")
        tool_params = params.get("arguments", {})
        
        if tool_name == "get_temperature":
            city = tool_params.get("city")
            result = get_current_weather(city)
            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(result, indent=2)
                    }
                ]
            }
        
        elif tool_name == "get_all_temperatures":
            results = {}
            for city in CITY_COORDS.keys():
                results[city] = get_current_weather(city)
            return {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(results, indent=2)
                    }
                ]
            }
        
        else:
            return {
                "error": {
                    "code": -32601,
                    "message": f"Tool not found: {tool_name}"
                }
            }
    
    elif method == "initialize":
        return {
            "protocolVersion": "2024-11-05",
            "serverInfo": {
                "name": "weather-mcp-server",
                "version": "1.0.0"
            },
            "capabilities": {
                "tools": {}
            }
        }
    
    else:
        return {
            "error": {
                "code": -32601,
                "message": f"Method not found: {method}"
            }
        }


def main():
    """Main MCP server loop."""
    # Send initialization
    send_response({
        "jsonrpc": "2.0",
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "serverInfo": {
                "name": "weather-mcp-server",
                "version": "1.0.0"
            },
            "capabilities": {
                "tools": {}
            }
        }
    })
    
    # Process requests from stdin
    for line in sys.stdin:
        try:
            request = json.loads(line.strip())
            response = handle_request(request)
            
            result = {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "result": response
            }
            send_response(result)
            
        except json.JSONDecodeError:
            send_response({
                "jsonrpc": "2.0",
                "error": {
                    "code": -32700,
                    "message": "Parse error"
                }
            })
        except Exception as e:
            send_response({
                "jsonrpc": "2.0",
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            })


if __name__ == "__main__":
    main()
