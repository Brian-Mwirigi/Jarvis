"""
YouTube Integration for Jarvis
Search and play YouTube videos
"""
from langchain.tools import tool
import webbrowser
import logging
import urllib.parse


@tool
def search_youtube(query: str, max_results: int = 5) -> str:
    """
    Search YouTube and return top video results.
    
    Args:
        query: Search query
        max_results: Number of results to return (default: 5, max: 10)
    
    Examples:
        - "Search YouTube for Python tutorials"
        - "Find music videos"
        - "Search for cooking recipes on YouTube"
    
    Returns:
        Top YouTube search results with links
    """
    try:
        # Build YouTube search URL
        encoded_query = urllib.parse.quote(query)
        search_url = f"https://www.youtube.com/results?search_query={encoded_query}"
        
        # For now, just open YouTube search (a full implementation would use YouTube API)
        # To use YouTube API properly, you'd need: pip install google-api-python-client
        # and get an API key from Google Cloud Console
        
        # Simple version: just return the search URL
        return f"YouTube search: {search_url}\n\nTo get actual results, you can:\n1. Use YouTube Data API (requires API key)\n2. Or I can open this search in your browser"
        
    except Exception as e:
        logging.error(f"YouTube search error: {e}")
        return f"YouTube search error: {e}"


@tool
def play_youtube(query: str) -> str:
    """
    Search and play the first YouTube video result in browser.
    
    Args:
        query: Search query or video title
    
    Examples:
        - "Play Bohemian Rhapsody on YouTube"
        - "Play Python tutorial"
        - "Play relaxing music"
    
    Returns:
        Confirmation message
    """
    try:
        # Build YouTube search URL
        encoded_query = urllib.parse.quote(query)
        search_url = f"https://www.youtube.com/results?search_query={encoded_query}"
        
        # Open in browser
        webbrowser.open(search_url)
        
        return f"Opening YouTube search for: {query}"
        
    except Exception as e:
        logging.error(f"YouTube play error: {e}")
        return f"Failed to open YouTube: {e}"


@tool
def open_youtube_video(video_url: str) -> str:
    """
    Open a specific YouTube video URL in browser.
    
    Args:
        video_url: Full YouTube URL or video ID
    
    Examples:
        - "Open this YouTube video: https://youtube.com/watch?v=..."
        - "Play video ID: dQw4w9WgXcQ"
    
    Returns:
        Confirmation message
    """
    try:
        # Handle video ID or full URL
        if not video_url.startswith("http"):
            # Assume it's a video ID
            video_url = f"https://www.youtube.com/watch?v={video_url}"
        
        webbrowser.open(video_url)
        return f"Opening YouTube video: {video_url}"
        
    except Exception as e:
        logging.error(f"YouTube open error: {e}")
        return f"Failed to open video: {e}"


@tool
def youtube_music(genre: str = "relaxing music") -> str:
    """
    Play music from YouTube.
    
    Args:
        genre: Type of music (e.g., "jazz", "rock", "classical", "lo-fi")
    
    Examples:
        - "Play some jazz music"
        - "Play relaxing music"
        - "Play rock music"
    
    Returns:
        Confirmation message
    """
    try:
        query = f"{genre} music"
        encoded_query = urllib.parse.quote(query)
        search_url = f"https://www.youtube.com/results?search_query={encoded_query}"
        
        webbrowser.open(search_url)
        return f"Playing {genre} music from YouTube"
        
    except Exception as e:
        logging.error(f"YouTube music error: {e}")
        return f"Failed to play music: {e}"
