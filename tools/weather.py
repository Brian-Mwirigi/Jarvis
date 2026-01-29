"""
Weather Information Tool for Jarvis
Uses wttr.in - a free weather API that requires no API key!
"""
from langchain.tools import tool
import requests
import logging


@tool
def get_weather(location: str = "") -> str:
    """
    Get current weather information for a location.
    Uses wttr.in free weather service (no API key needed).
    
    Args:
        location: City name or location (e.g., "London", "New York", "Tokyo")
                 If empty, uses IP-based location
    
    Examples:
        - "What's the weather in London?"
        - "Weather in Tokyo"
        - "Will it rain today?"
        - "Temperature in Paris"
    
    Returns:
        Weather information including temperature, conditions, and forecast
    """
    try:
        # wttr.in provides weather in simple format
        # Format: ?format=... with custom tokens
        # %C = Weather condition
        # %t = Temperature
        # %h = Humidity
        # %w = Wind
        # %l = Location
        # %m = Moon phase
        
        if not location:
            location = ""  # wttr.in will use IP location
        
        # Get current weather
        url = f"https://wttr.in/{location}?format=%l:+%C+%t+%h+%w"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            weather_info = response.text.strip()
            
            # Get 3-day forecast in simple format
            forecast_url = f"https://wttr.in/{location}?format=%l\nToday:+%C+%t\nTomorrow:+%C+%t\nDay+after:+%C+%t"
            forecast_response = requests.get(forecast_url, timeout=10)
            
            if forecast_response.status_code == 200:
                return forecast_response.text.strip()
            else:
                return weather_info
        else:
            return f"Could not get weather for {location}. Try a different location."
            
    except requests.exceptions.Timeout:
        return "Weather request timed out. Please try again."
    except requests.exceptions.RequestException as e:
        logging.error(f"Weather API error: {e}")
        return "Could not connect to weather service. Check your internet connection."
    except Exception as e:
        logging.error(f"Weather error: {e}")
        return f"Weather error: {e}"


@tool
def get_detailed_weather(location: str) -> str:
    """
    Get detailed weather forecast for a location.
    
    Args:
        location: City name (e.g., "London", "Tokyo")
    
    Examples:
        - "Detailed weather for London"
        - "Full forecast for Tokyo"
    
    Returns:
        Detailed weather forecast
    """
    try:
        # Get detailed ASCII weather art from wttr.in
        url = f"https://wttr.in/{location}?0T"  # 0 = current, T = no ANSI colors
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            # Return first 500 chars to avoid too long output
            weather = response.text.strip()
            if len(weather) > 500:
                # Get just the summary lines
                lines = weather.split('\n')[:10]  # First 10 lines
                return '\n'.join(lines)
            return weather
        else:
            return f"Could not get detailed weather for {location}"
            
    except Exception as e:
        logging.error(f"Detailed weather error: {e}")
        return f"Error getting detailed weather: {e}"
