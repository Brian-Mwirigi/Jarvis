# tools/time_tool.py

from langchain.tools import tool
from datetime import datetime
import pytz

# Comprehensive city-to-timezone mapping
CITY_TIMEZONES = {
    # North America
    "new york": "America/New_York",
    "los angeles": "America/Los_Angeles",
    "chicago": "America/Chicago",
    "toronto": "America/Toronto",
    "vancouver": "America/Vancouver",
    "mexico city": "America/Mexico_City",
    "miami": "America/New_York",
    "san francisco": "America/Los_Angeles",
    "seattle": "America/Los_Angeles",
    "boston": "America/New_York",
    "washington": "America/New_York",
    "dc": "America/New_York",
    "denver": "America/Denver",
    "phoenix": "America/Phoenix",
    "las vegas": "America/Los_Angeles",
    
    # Europe
    "london": "Europe/London",
    "paris": "Europe/Paris",
    "berlin": "Europe/Berlin",
    "madrid": "Europe/Madrid",
    "rome": "Europe/Rome",
    "amsterdam": "Europe/Amsterdam",
    "brussels": "Europe/Brussels",
    "vienna": "Europe/Vienna",
    "zurich": "Europe/Zurich",
    "stockholm": "Europe/Stockholm",
    "oslo": "Europe/Oslo",
    "copenhagen": "Europe/Copenhagen",
    "helsinki": "Europe/Helsinki",
    "dublin": "Europe/Dublin",
    "lisbon": "Europe/Lisbon",
    "athens": "Europe/Athens",
    "moscow": "Europe/Moscow",
    "istanbul": "Europe/Istanbul",
    "prague": "Europe/Prague",
    "warsaw": "Europe/Warsaw",
    
    # Asia
    "tokyo": "Asia/Tokyo",
    "beijing": "Asia/Shanghai",
    "shanghai": "Asia/Shanghai",
    "hong kong": "Asia/Hong_Kong",
    "singapore": "Asia/Singapore",
    "seoul": "Asia/Seoul",
    "mumbai": "Asia/Kolkata",
    "delhi": "Asia/Kolkata",
    "bangalore": "Asia/Kolkata",
    "dubai": "Asia/Dubai",
    "bangkok": "Asia/Bangkok",
    "jakarta": "Asia/Jakarta",
    "manila": "Asia/Manila",
    "kuala lumpur": "Asia/Kuala_Lumpur",
    "tel aviv": "Asia/Jerusalem",
    "riyadh": "Asia/Riyadh",
    "karachi": "Asia/Karachi",
    "tehran": "Asia/Tehran",
    
    # Oceania
    "sydney": "Australia/Sydney",
    "melbourne": "Australia/Melbourne",
    "brisbane": "Australia/Brisbane",
    "perth": "Australia/Perth",
    "auckland": "Pacific/Auckland",
    "wellington": "Pacific/Auckland",
    
    # Africa
    "cairo": "Africa/Cairo",
    "johannesburg": "Africa/Johannesburg",
    "cape town": "Africa/Johannesburg",
    "lagos": "Africa/Lagos",
    "nairobi": "Africa/Nairobi",
    "casablanca": "Africa/Casablanca",
    
    # South America
    "sao paulo": "America/Sao_Paulo",
    "rio de janeiro": "America/Sao_Paulo",
    "buenos aires": "America/Argentina/Buenos_Aires",
    "santiago": "America/Santiago",
    "lima": "America/Lima",
    "bogota": "America/Bogota",
}

@tool
def get_time(city: str) -> str:
    """
    Returns the current time in a given city.
    Supports major cities worldwide including New York, London, Tokyo, Sydney, Paris, Berlin,
    Singapore, Dubai, Mumbai, and many more.
    
    Args:
        city: Name of the city (e.g., "New York", "Tokyo", "London")
    
    Returns:
        str: Current time in that city
    """
    try:
        city_key = city.lower().strip()
        
        # Try exact match first
        if city_key in CITY_TIMEZONES:
            timezone_name = CITY_TIMEZONES[city_key]
        else:
            # Try fuzzy matching - check if input is contained in any city name
            matches = [tz for city_name, tz in CITY_TIMEZONES.items() if city_key in city_name or city_name in city_key]
            if matches:
                timezone_name = matches[0]
            else:
                # List some examples
                return (f"Sorry, I don't have timezone information for '{city}'. "
                       f"Try cities like: New York, London, Tokyo, Sydney, Paris, Berlin, Singapore, Dubai, etc.")

        timezone = pytz.timezone(timezone_name)
        current_time = datetime.now(timezone)
        
        # Format with date and time for better context
        formatted_time = current_time.strftime("%I:%M %p")
        formatted_date = current_time.strftime("%A, %B %d, %Y")
        
        return f"The current time in {city.title()} is {formatted_time} ({formatted_date})"
    except Exception as e:
        return f"Error getting time for {city}: {e}"
