"""
Clipboard Operations for Jarvis
"""
from langchain.tools import tool
import logging

try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False
    logging.warning("⚠️ pyperclip not installed. Install with: pip install pyperclip")


@tool
def read_clipboard() -> str:
    """
    Read the current content of the clipboard.
    
    Examples:
        - "What's in my clipboard?"
        - "Read clipboard"
        - "What did I copy?"
    
    Returns:
        Current clipboard content
    """
    if not CLIPBOARD_AVAILABLE:
        return "Clipboard operations require pyperclip. Install with: pip install pyperclip"
    
    try:
        content = pyperclip.paste()
        if not content:
            return "Clipboard is empty"
        return f"Clipboard contains: {content}"
    except Exception as e:
        logging.error(f"Clipboard read error: {e}")
        return f"Failed to read clipboard: {e}"


@tool
def write_clipboard(text: str) -> str:
    """
    Write text to the clipboard.
    
    Args:
        text: Text to copy to clipboard
    
    Examples:
        - "Copy this to clipboard: Hello World"
        - "Put this in clipboard: [text]"
    
    Returns:
        Confirmation message
    """
    if not CLIPBOARD_AVAILABLE:
        return "Clipboard operations require pyperclip. Install with: pip install pyperclip"
    
    try:
        pyperclip.copy(text)
        return f"Copied to clipboard: {text[:50]}{'...' if len(text) > 50 else ''}"
    except Exception as e:
        logging.error(f"Clipboard write error: {e}")
        return f"Failed to write clipboard: {e}"


@tool
def clear_clipboard() -> str:
    """
    Clear the clipboard contents.
    
    Examples:
        - "Clear clipboard"
        - "Empty clipboard"
    
    Returns:
        Confirmation message
    """
    if not CLIPBOARD_AVAILABLE:
        return "Clipboard operations require pyperclip. Install with: pip install pyperclip"
    
    try:
        pyperclip.copy("")
        return "Clipboard cleared"
    except Exception as e:
        logging.error(f"Clipboard clear error: {e}")
        return f"Failed to clear clipboard: {e}"
