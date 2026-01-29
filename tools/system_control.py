"""
System Control Tools for Jarvis - Control computer settings
"""
from langchain.tools import tool
import platform
import subprocess
import logging

@tool
def set_volume(level: int) -> str:
    """
    Set system volume level (0-100).
    
    Args:
        level: Volume level from 0 (mute) to 100 (max)
    
    Examples:
        - "Set volume to 50"
        - "Volume 75"
        - "Mute" (use level=0)
    
    Returns:
        Confirmation message
    """
    try:
        level = max(0, min(100, level))  # Clamp between 0-100
        
        system = platform.system()
        
        if system == "Windows":
            # Use nircmd or PowerShell
            ps_command = f"""
$obj = New-Object -ComObject WScript.Shell
for ($i=0; $i -lt 50; $i++) {{
    $obj.SendKeys([char]174)  # Volume down key
}}
$targetVolume = {level}
$steps = [math]::Round($targetVolume / 2)
for ($i=0; $i -lt $steps; $i++) {{
    $obj.SendKeys([char]175)  # Volume up key
}}
"""
            subprocess.run(
                ["powershell", "-Command", ps_command],
                capture_output=True,
                timeout=5
            )
            return f"Volume set to {level}%"
            
        elif system == "Darwin":  # macOS
            subprocess.run(["osascript", "-e", f"set volume output volume {level}"])
            return f"Volume set to {level}%"
            
        elif system == "Linux":
            subprocess.run(["amixer", "set", "Master", f"{level}%"])
            return f"Volume set to {level}%"
            
        else:
            return f"Volume control not supported on {system}"
            
    except Exception as e:
        logging.error(f"Volume control error: {e}")
        return f"Failed to set volume: {e}"


@tool
def lock_computer() -> str:
    """
    Lock the computer screen.
    
    Examples:
        - "Lock my computer"
        - "Lock screen"
    
    Returns:
        Confirmation message
    """
    try:
        system = platform.system()
        
        if system == "Windows":
            subprocess.Popen(["rundll32.exe", "user32.dll,LockWorkStation"])
            return "Computer locked"
            
        elif system == "Darwin":  # macOS
            subprocess.Popen(["/System/Library/CoreServices/Menu Extras/User.menu/Contents/Resources/CGSession", "-suspend"])
            return "Computer locked"
            
        elif system == "Linux":
            # Try different lock commands
            for cmd in [["gnome-screensaver-command", "-l"], ["xdg-screensaver", "lock"]]:
                try:
                    subprocess.Popen(cmd)
                    return "Computer locked"
                except FileNotFoundError:
                    continue
            return "Could not find screen lock command"
            
        else:
            return f"Lock not supported on {system}"
            
    except Exception as e:
        logging.error(f"Lock error: {e}")
        return f"Failed to lock computer: {e}"


@tool
def shutdown_computer(minutes: int = 0) -> str:
    """
    Schedule computer shutdown.
    
    Args:
        minutes: Minutes from now to shutdown (0 = immediate)
    
    Examples:
        - "Shut down in 10 minutes"
        - "Shutdown now"
    
    Returns:
        Confirmation message
    """
    try:
        system = platform.system()
        
        if system == "Windows":
            seconds = minutes * 60
            subprocess.Popen(["shutdown", "/s", "/t", str(seconds)])
            if minutes == 0:
                return "Shutting down now..."
            else:
                return f"Computer will shut down in {minutes} minutes"
                
        elif system == "Darwin":  # macOS
            if minutes == 0:
                subprocess.Popen(["sudo", "shutdown", "-h", "now"])
                return "Shutting down now..."
            else:
                subprocess.Popen(["sudo", "shutdown", "-h", f"+{minutes}"])
                return f"Computer will shut down in {minutes} minutes"
                
        elif system == "Linux":
            if minutes == 0:
                subprocess.Popen(["shutdown", "-h", "now"])
                return "Shutting down now..."
            else:
                subprocess.Popen(["shutdown", "-h", f"+{minutes}"])
                return f"Computer will shut down in {minutes} minutes"
                
        else:
            return f"Shutdown not supported on {system}"
            
    except Exception as e:
        logging.error(f"Shutdown error: {e}")
        return f"Failed to schedule shutdown: {e}"


@tool
def cancel_shutdown() -> str:
    """
    Cancel a scheduled shutdown.
    
    Examples:
        - "Cancel shutdown"
        - "Stop shutdown"
    
    Returns:
        Confirmation message
    """
    try:
        system = platform.system()
        
        if system == "Windows":
            subprocess.run(["shutdown", "/a"])
            return "Shutdown cancelled"
            
        elif system in ["Darwin", "Linux"]:
            subprocess.run(["sudo", "shutdown", "-c"])
            return "Shutdown cancelled"
            
        else:
            return f"Cancel not supported on {system}"
            
    except Exception as e:
        logging.error(f"Cancel error: {e}")
        return f"Failed to cancel shutdown: {e}"


@tool
def restart_computer(minutes: int = 0) -> str:
    """
    Schedule computer restart.
    
    Args:
        minutes: Minutes from now to restart (0 = immediate)
    
    Examples:
        - "Restart in 5 minutes"
        - "Restart now"
    
    Returns:
        Confirmation message
    """
    try:
        system = platform.system()
        
        if system == "Windows":
            seconds = minutes * 60
            subprocess.Popen(["shutdown", "/r", "/t", str(seconds)])
            if minutes == 0:
                return "Restarting now..."
            else:
                return f"Computer will restart in {minutes} minutes"
                
        elif system == "Darwin":  # macOS
            if minutes == 0:
                subprocess.Popen(["sudo", "shutdown", "-r", "now"])
                return "Restarting now..."
            else:
                subprocess.Popen(["sudo", "shutdown", "-r", f"+{minutes}"])
                return f"Computer will restart in {minutes} minutes"
                
        elif system == "Linux":
            if minutes == 0:
                subprocess.Popen(["shutdown", "-r", "now"])
                return "Restarting now..."
            else:
                subprocess.Popen(["shutdown", "-r", f"+{minutes}"])
                return f"Computer will restart in {minutes} minutes"
                
        else:
            return f"Restart not supported on {system}"
            
    except Exception as e:
        logging.error(f"Restart error: {e}")
        return f"Failed to schedule restart: {e}"
