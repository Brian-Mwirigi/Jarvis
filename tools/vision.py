"""
Vision Tool for Jarvis - LangChain compatible
"""
from langchain.tools import tool
from vision_remote import RemoteVision
import logging

# Initialize vision client
vision = RemoteVision()


@tool
def analyze_screen(question: str = "What do you see on the screen?") -> str:
    """
    Analyze what's currently on the screen using AI vision.
    Use this when the user asks about what's visible, what they're looking at,
    or to describe the screen contents.
    
    Args:
        question: What to ask about the screen (default: "What do you see on the screen?")
    
    Returns:
        str: Description of what's on the screen
        
    Examples:
        - "What do you see?" → analyze_screen()
        - "Describe my screen" → analyze_screen("Describe everything on this screen")
        - "What app am I using?" → analyze_screen("What application is open?")
    """
    if not vision.available:
        return "Vision system is not available. Please check VISION_URL environment variable."
    
    logging.info(f"🔧 Tool: analyze_screen('{question}')")
    result = vision.analyze_screen(question)
    return result


@tool
def analyze_camera(question: str = "What do you see?") -> str:
    """
    Capture an image from the webcam and analyze it using AI vision.
    Use this when the user asks about what they're holding, what's in front of them,
    or wants you to see them through the camera.
    
    Args:
        question: What to ask about the camera image (default: "What do you see?")
    
    Returns:
        str: Description/answer about what the camera sees
        
    Examples:
        - "What am I holding?" → analyze_camera("What is the person holding?")
        - "What do you see through the camera?" → analyze_camera()
        - "Look at me" → analyze_camera("Describe what you see")
    """
    if not vision.available:
        return "Vision system is not available. Please check VISION_URL environment variable."
    
    logging.info(f"🔧 Tool: analyze_camera('{question}')")
    result = vision.analyze_camera(question)
    return result


@tool
def analyze_image(image_path: str, question: str = "What's in this image?") -> str:
    """
    Analyze an image file using AI vision.
    Use this when the user wants to know about a specific image file.
    
    Args:
        image_path: Path to the image file to analyze
        question: What to ask about the image
    
    Returns:
        str: Description/answer about the image
        
    Examples:
        - "What's in photo.jpg?" → analyze_image("photo.jpg")
        - "Describe screenshot.png" → analyze_image("screenshot.png", "Describe this image")
    """
    if not vision.available:
        return "Vision system is not available. Please check VISION_URL environment variable."
    
    logging.info(f"🔧 Tool: analyze_image('{image_path}', '{question}')")
    result = vision.analyze_image_file(image_path, question)
    return result


# Quick test
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("\n🧪 Testing Vision Tools:")
    
    if vision.available:
        print("\n1. Testing screen analysis...")
        result = analyze_screen.invoke({"question": "What do you see?"})
        print(f"Result: {result}\n")
    else:
        print("⚠️ Vision not available. Set VISION_URL in environment.")
