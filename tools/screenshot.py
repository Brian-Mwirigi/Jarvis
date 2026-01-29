from langchain.tools import tool
import os
import mss
import mss.tools
from datetime import datetime

@tool("capture_screenshot", return_direct=True)
def take_screenshot() -> str:
    """
    Captures the current screen and saves it to a timestamped file in Pictures/Jarvis folder.
    
    Use this tool when the user says:
    - "Take a screenshot"
    - "Capture the screen"
    - "Save a screenshot"
    """
    try:
        # Create a proper screenshots directory
        if os.name == 'nt':  # Windows
            pictures_dir = os.path.join(os.path.expanduser("~"), "Pictures")
        else:  # Linux/Mac
            pictures_dir = os.path.join(os.path.expanduser("~"), "Pictures")
        
        jarvis_dir = os.path.join(pictures_dir, "Jarvis")
        os.makedirs(jarvis_dir, exist_ok=True)
        
        # Create timestamped filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_path = os.path.join(jarvis_dir, f"screenshot_{timestamp}.png")

        with mss.mss() as sct:
            monitor = sct.monitors[1]  # [1] = main monitor; [0] = all monitors
            screenshot = sct.grab(monitor)
            mss.tools.to_png(screenshot.rgb, screenshot.size, output=image_path)

        return f"Screenshot captured and saved to {image_path}"
    except Exception as e:
        return f"Failed to capture screenshot: {str(e)}"


def get_latest_screenshot() -> str:
    """
    Get the path to the most recent screenshot taken by Jarvis.
    Used by OCR tool to read the latest screenshot.
    """
    try:
        if os.name == 'nt':  # Windows
            pictures_dir = os.path.join(os.path.expanduser("~"), "Pictures")
        else:  # Linux/Mac
            pictures_dir = os.path.join(os.path.expanduser("~"), "Pictures")
        
        jarvis_dir = os.path.join(pictures_dir, "Jarvis")
        
        if not os.path.exists(jarvis_dir):
            return None
        
        # Get all screenshot files
        screenshots = [f for f in os.listdir(jarvis_dir) if f.startswith("screenshot_") and f.endswith(".png")]
        
        if not screenshots:
            return None
        
        # Sort by modification time and get the latest
        screenshots.sort(key=lambda x: os.path.getmtime(os.path.join(jarvis_dir, x)), reverse=True)
        return os.path.join(jarvis_dir, screenshots[0])
    except Exception:
        return None
