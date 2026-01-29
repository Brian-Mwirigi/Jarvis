"""
Reminders and Timers for Jarvis
"""
from langchain.tools import tool
import threading
import time
import logging
import platform
import subprocess


def play_alert_sound():
    """Play a system alert sound"""
    try:
        system = platform.system()
        if system == "Windows":
            # Play Windows notification sound
            import winsound
            winsound.MessageBeep(winsound.MB_ICONASTERISK)
        elif system == "Darwin":  # macOS
            subprocess.run(["afplay", "/System/Library/Sounds/Glass.aiff"])
        elif system == "Linux":
            subprocess.run(["paplay", "/usr/share/sounds/freedesktop/stereo/complete.oga"])
    except Exception as e:
        logging.error(f"Alert sound error: {e}")


def show_notification(title: str, message: str):
    """Show system notification"""
    try:
        system = platform.system()
        if system == "Windows":
            # Use PowerShell to show notification
            ps_command = f"""
[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
[Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null

$template = @"
<toast>
    <visual>
        <binding template="ToastText02">
            <text id="1">{title}</text>
            <text id="2">{message}</text>
        </binding>
    </visual>
</toast>
"@

$xml = New-Object Windows.Data.Xml.Dom.XmlDocument
$xml.LoadXml($template)
$toast = [Windows.UI.Notifications.ToastNotification]::new($xml)
[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("Jarvis").Show($toast)
"""
            subprocess.run(["powershell", "-Command", ps_command], 
                         capture_output=True, 
                         creationflags=subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0)
        elif system == "Darwin":  # macOS
            subprocess.run([
                "osascript", "-e", 
                f'display notification "{message}" with title "{title}"'
            ])
        elif system == "Linux":
            subprocess.run(["notify-send", title, message])
    except Exception as e:
        logging.error(f"Notification error: {e}")


def reminder_thread(message: str, minutes: int):
    """Background thread for reminder"""
    time.sleep(minutes * 60)
    play_alert_sound()
    show_notification("Jarvis Reminder", message)
    logging.info(f"Reminder fired: {message}")


def timer_thread(seconds: int, label: str = "Timer"):
    """Background thread for timer"""
    time.sleep(seconds)
    play_alert_sound()
    show_notification("Jarvis Timer", f"{label} completed!")
    logging.info(f"Timer fired: {label}")


@tool
def set_reminder(message: str, minutes: int) -> str:
    """
    Set a reminder for X minutes from now.
    
    Args:
        message: Reminder message
        minutes: Minutes from now
    
    Examples:
        - "Remind me in 10 minutes to check email"
        - "Set a reminder for 30 minutes: meeting starts"
        - "Remind me in 5 minutes about the call"
    
    Returns:
        Confirmation message
    """
    try:
        if minutes < 1:
            return "Reminder must be at least 1 minute"
        if minutes > 1440:  # 24 hours
            return "Reminder cannot be more than 24 hours"
        
        # Start reminder in background thread
        thread = threading.Thread(target=reminder_thread, args=(message, minutes), daemon=True)
        thread.start()
        
        return f"Reminder set: '{message}' in {minutes} minute{'s' if minutes != 1 else ''}"
        
    except Exception as e:
        logging.error(f"Reminder error: {e}")
        return f"Failed to set reminder: {e}"


@tool
def set_timer(minutes: int, label: str = "Timer") -> str:
    """
    Set a countdown timer.
    
    Args:
        minutes: Duration in minutes
        label: Optional label for the timer (default: "Timer")
    
    Examples:
        - "Set a timer for 5 minutes"
        - "Timer for 10 minutes: pizza"
        - "Set 15 minute timer"
    
    Returns:
        Confirmation message
    """
    try:
        if minutes < 1:
            return "Timer must be at least 1 minute"
        if minutes > 180:  # 3 hours
            return "Timer cannot be more than 3 hours"
        
        seconds = minutes * 60
        
        # Start timer in background thread
        thread = threading.Thread(target=timer_thread, args=(seconds, label), daemon=True)
        thread.start()
        
        return f"Timer set for {minutes} minute{'s' if minutes != 1 else ''}: {label}"
        
    except Exception as e:
        logging.error(f"Timer error: {e}")
        return f"Failed to set timer: {e}"


@tool
def quick_timer(seconds: int) -> str:
    """
    Set a quick countdown timer in seconds.
    
    Args:
        seconds: Duration in seconds
    
    Examples:
        - "Set timer for 30 seconds"
        - "Quick 45 second timer"
    
    Returns:
        Confirmation message
    """
    try:
        if seconds < 1:
            return "Timer must be at least 1 second"
        if seconds > 300:  # 5 minutes
            return "For timers over 5 minutes, use set_timer with minutes"
        
        # Start timer in background thread
        thread = threading.Thread(target=timer_thread, args=(seconds, f"{seconds}s timer"), daemon=True)
        thread.start()
        
        return f"Timer set for {seconds} second{'s' if seconds != 1 else ''}"
        
    except Exception as e:
        logging.error(f"Timer error: {e}")
        return f"Failed to set timer: {e}"
