"""
MCP Server implementation for Weather Service.
This provides a proper MCP protocol interface instead of HTTP REST API.
"""
import sys
import json
import logging
from weather import get_current_weather, CITY_COORDS

# Log to stderr so it doesn't interfere with JSON-RPC
logging.basicConfig(level=logging.INFO, stream=sys.stderr)


def send_response(response):
    """Send JSON response to stdout."""
    print(json.dumps(response), flush=True)


def handle_request(request):
    """Handle incoming MCP requests."""
    method = request.get("method")
    params = request.get("params", {})
    
    logging.info(f"Received method: {method}")
    
    if method == "initialize":
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
    
    elif method == "tools/list":
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
                        "properties": {},
                        "required": []
                    }
                }
            ]
        }
    
    elif method == "tools/call":
        tool_name = params.get("name")
        tool_params = params.get("arguments", {})
        
        logging.info(f"Calling tool: {tool_name} with params: {tool_params}")
        
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
            raise Exception(f"Unknown tool: {tool_name}")
    
    else:
        raise Exception(f"Unknown method: {method}")


def main():
    """Main MCP server loop - wait for requests on stdin."""
    logging.info("Weather MCP Server starting...")
    
    # Process requests from stdin
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
            
        try:
            request = json.loads(line)
            logging.info(f"Request: {request}")
            
            response = handle_request(request)
            
            result = {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "result": response
            }
            
            logging.info(f"Sending response: {result}")
            send_response(result)
            
        except json.JSONDecodeError as e:
            logging.error(f"JSON decode error: {e}")
            send_response({
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32700,
                    "message": "Parse error"
                }
            })
        except Exception as e:
            logging.error(f"Error handling request: {e}", exc_info=True)
            send_response({
                "jsonrpc": "2.0",
                "id": request.get("id") if 'request' in locals() else None,
                "error": {
                    "code": -32603,
                    "message": str(e)
                }
            })


if __name__ == "__main__":
    main()
