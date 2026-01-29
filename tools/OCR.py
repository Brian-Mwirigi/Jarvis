from langchain.tools import tool
from PIL import Image
import pytesseract
import os
from tools.screenshot import get_latest_screenshot

@tool("read_latest_screenshot", return_direct=True)
def read_text_from_latest_image() -> str:
    """
    Reads and extracts text from the most recent screenshot taken by Jarvis.
    Use this tool when the user says something like:
    - "Read the screen"
    - "What does the screenshot say?"
    - "Extract text from the image"
    """
    image_path = get_latest_screenshot()

    if not image_path or not os.path.exists(image_path):
        return "No screenshot found. Please take a screenshot first using the screenshot tool."

    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        if text and text.strip():
            return f"Text extracted from screenshot:\n\n{text.strip()}"
        else:
            return "No readable text found in the screenshot."
    except Exception as e:
        return f"Failed to extract text: {str(e)}"
