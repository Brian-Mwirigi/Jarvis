"""
Music Control Tool for Jarvis
Control Spotify playback (requires Spotify desktop app running)
"""
from langchain.tools import tool
import subprocess
import platform
import logging
import webbrowser


@tool
def play_spotify_song(song_name: str) -> str:
    """
    Search and play a song on Spotify.
    
    Args:
        song_name: Name of the song or artist to play
    
    Examples:
        - "Play Bohemian Rhapsody on Spotify"
        - "Play The Beatles"
        - "Play some jazz music"
    
    Returns:
        Confirmation message
    """
    try:
        # Open Spotify search in browser (works cross-platform)
        search_url = f"https://open.spotify.com/search/{song_name.replace(' ', '%20')}"
        webbrowser.open(search_url)
        return f"🎵 Opened Spotify search for '{song_name}'"
        
    except Exception as e:
        logging.error(f"Spotify play error: {e}")
        return f"❌ Could not open Spotify: {str(e)}"


@tool
def control_music_playback(action: str) -> str:
    """
    Control music playback (play/pause/next/previous).
    
    Args:
        action: Control action (play, pause, next, previous, stop)
    
    Examples:
        - "Pause music"
        - "Next song"
        - "Play music"
        - "Previous track"
    
    Returns:
        Confirmation message
    """
    try:
        system = platform.system()
        action = action.lower()
        
        if system == "Windows":
            # Windows media keys
            import pyautogui
            if action in ["pause", "play"]:
                pyautogui.press("playpause")
                return f"🎵 {action.title()} command sent"
            elif action == "next":
                pyautogui.press("nexttrack")
                return "🎵 Skipped to next track"
            elif action == "previous":
                pyautogui.press("prevtrack")
                return "🎵 Back to previous track"
            elif action == "stop":
                pyautogui.press("stop")
                return "🎵 Music stopped"
            else:
                return f"❌ Unknown action: {action}"
        
        elif system == "Darwin":  # macOS
            # Use AppleScript to control Spotify
            scripts = {
                "play": 'tell application "Spotify" to play',
                "pause": 'tell application "Spotify" to pause',
                "next": 'tell application "Spotify" to next track',
                "previous": 'tell application "Spotify" to previous track'
            }
            
            if action in scripts:
                subprocess.run(["osascript", "-e", scripts[action]], check=True)
                return f"🎵 {action.title()} command sent to Spotify"
            else:
                return f"❌ Unknown action: {action}"
        
        elif system == "Linux":
            # Use dbus to control media players
            dbus_commands = {
                "play": "Play",
                "pause": "Pause",
                "next": "Next",
                "previous": "Previous"
            }
            
            if action in dbus_commands:
                subprocess.run([
                    "dbus-send",
                    "--print-reply",
                    "--dest=org.mpris.MediaPlayer2.spotify",
                    "/org/mpris/MediaPlayer2",
                    f"org.mpris.MediaPlayer2.Player.{dbus_commands[action]}"
                ], check=True)
                return f"🎵 {action.title()} command sent"
            else:
                return f"❌ Unknown action: {action}"
        
        else:
            return f"❌ Music control not supported on {system}"
            
    except Exception as e:
        logging.error(f"Music control error: {e}")
        return f"❌ Could not control music: {str(e)}. Make sure Spotify is running."


@tool
def get_current_track() -> str:
    """
    Get information about currently playing track.
    
    Examples:
        - "What's playing?"
        - "What song is this?"
        - "Current track info"
    
    Returns:
        Current track information
    """
    try:
        system = platform.system()
        
        if system == "Darwin":  # macOS
            script = '''
            tell application "Spotify"
                if player state is playing then
                    set trackName to name of current track
                    set artistName to artist of current track
                    return trackName & " by " & artistName
                else
                    return "No track playing"
                end if
            end tell
            '''
            result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, check=True)
            return f"🎵 {result.stdout.strip()}"
        
        elif system == "Windows":
            # Note: Windows doesn't have easy native way to get track info
            # Would need Windows.Media.Control or Spotify API
            return "🎵 Track info not available on Windows (check Spotify app)"
        
        elif system == "Linux":
            result = subprocess.run([
                "dbus-send", "--print-reply", "--dest=org.mpris.MediaPlayer2.spotify",
                "/org/mpris/MediaPlayer2", "org.freedesktop.DBus.Properties.Get",
                "string:org.mpris.MediaPlayer2.Player", "string:Metadata"
            ], capture_output=True, text=True)
            
            # Parse output (simplified)
            if "xesam:title" in result.stdout:
                return "🎵 Track info retrieved (parsing needed)"
            else:
                return "🎵 No track playing"
        
        return "🎵 Track info not available"
        
    except Exception as e:
        logging.error(f"Track info error: {e}")
        return f"❌ Could not get track info: {str(e)}"


@tool
def set_music_volume(volume_percent: int) -> str:
    """
    Set music playback volume.
    
    Args:
        volume_percent: Volume level (0-100)
    
    Examples:
        - "Set music volume to 50"
        - "Turn music volume to 80 percent"
    
    Returns:
        Confirmation message
    """
    try:
        if not (0 <= volume_percent <= 100):
            return "❌ Volume must be between 0 and 100"
        
        system = platform.system()
        
        if system == "Darwin":  # macOS
            script = f'tell application "Spotify" to set sound volume to {volume_percent}'
            subprocess.run(["osascript", "-e", script], check=True)
            return f"🎵 Spotify volume set to {volume_percent}%"
        
        else:
            # For Windows/Linux, use system volume control from system_control tool
            from tools.system_control import set_volume
            return set_volume.invoke({"level": volume_percent})
            
    except Exception as e:
        logging.error(f"Volume control error: {e}")
        return f"❌ Could not set volume: {str(e)}"


# Quick test
if __name__ == "__main__":
    print("Music control tools created. Requires Spotify running.")
    print("Test: Opening Spotify search...")
    result = play_spotify_song.invoke({"song_name": "Bohemian Rhapsody"})
    print(result)
