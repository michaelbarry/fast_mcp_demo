# weather_server.py
from fastmcp import FastMCP
import os, requests
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
if not API_KEY:
    raise RuntimeError("Missing OPENWEATHER_API_KEY")

mcp = FastMCP("Weather")

@mcp.tool()
async def get_current_weather(city: str) -> str:
    """Return current weather for a city using One Call API."""
    # Get coordinates for the city
    lat, lon = await get_coordinates(city)
    
    # Make the weather API call
    r = requests.get(
        "https://api.openweathermap.org/data/3.0/onecall",
        params={
            "lat": lat, 
            "lon": lon, 
            "exclude": "minutely,hourly,daily,alerts", 
            "appid": API_KEY, 
            "units": "metric"
        },
        timeout=10,
    )
    r.raise_for_status()
    data = r.json()
    desc = data["current"]["weather"][0]["description"]
    temp = data["current"]["temp"]
    return f"{city}: {desc}, {temp} °C"

@mcp.tool()
async def get_coordinates(city: str) -> tuple:
    """Convert city name to latitude and longitude."""
    r = requests.get(
        "https://api.openweathermap.org/geo/1.0/direct",
        params={"q": city, "limit": 1, "appid": API_KEY},
        timeout=10,
    )
    r.raise_for_status()
    data = r.json()
    if not data:
        raise ValueError(f"Could not find coordinates for {city}")
    lat = data[0]["lat"]
    lon = data[0]["lon"]
    return lat, lon

if __name__ == "__main__":
    # Expose as an SSE service on 0.0.0.0:8000/sse
    mcp.run(transport="sse")       # host/port/path can be overridden
