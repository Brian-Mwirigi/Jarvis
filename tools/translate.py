"""
Translation Tool for Jarvis
Translate text between languages using deep-translator (no API key needed!)
"""
from langchain.tools import tool
from deep_translator import GoogleTranslator
import logging


# Language codes mapping for common languages
LANGUAGE_CODES = {
    "spanish": "es", "french": "fr", "german": "de", "italian": "it",
    "portuguese": "pt", "russian": "ru", "japanese": "ja", "chinese": "zh-CN",
    "korean": "ko", "arabic": "ar", "hindi": "hi", "turkish": "tr",
    "dutch": "nl", "polish": "pl", "swedish": "sv", "norwegian": "no",
    "danish": "da", "finnish": "fi", "greek": "el", "hebrew": "he",
    "thai": "th", "vietnamese": "vi", "indonesian": "id", "malay": "ms",
    "filipino": "fil", "czech": "cs", "hungarian": "hu", "romanian": "ro",
    "ukrainian": "uk", "bengali": "bn", "urdu": "ur", "persian": "fa"
}


@tool
def translate_text(text: str, target_language: str, source_language: str = "auto") -> str:
    """
    Translate text from one language to another.
    
    Args:
        text: The text to translate
        target_language: Target language (e.g., "Spanish", "French", "Japanese")
        source_language: Source language (default: "auto" for automatic detection)
    
    Examples:
        - "Translate 'hello' to Spanish" → translate_text("hello", "Spanish")
        - "What is 'thank you' in Japanese?" → translate_text("thank you", "Japanese")
        - "Translate 'bonjour' from French to English" → translate_text("bonjour", "English", "French")
    
    Returns:
        Translated text
    """
    try:
        # Normalize language names to codes
        target = LANGUAGE_CODES.get(target_language.lower(), target_language.lower())
        source = "auto" if source_language == "auto" else LANGUAGE_CODES.get(source_language.lower(), source_language.lower())
        
        # Create translator
        translator = GoogleTranslator(source=source, target=target)
        
        # Translate
        result = translator.translate(text)
        
        if source == "auto":
            return f"Translation: {result}"
        else:
            return f"Translation ({source_language} → {target_language}): {result}"
            
    except Exception as e:
        logging.error(f"Translation error: {e}")
        return f"Could not translate text. Error: {str(e)}"


@tool
def detect_language(text: str) -> str:
    """
    Detect the language of given text.
    
    Args:
        text: The text to analyze
    
    Examples:
        - "What language is 'bonjour'?" → detect_language("bonjour")
        - "Detect language of 'こんにちは'" → detect_language("こんにちは")
    
    Returns:
        Detected language name
    """
    try:
        from langdetect import detect, DetectorFactory
        DetectorFactory.seed = 0  # For consistent results
        
        lang_code = detect(text)
        
        # Map code back to language name
        reverse_map = {v: k for k, v in LANGUAGE_CODES.items()}
        language_name = reverse_map.get(lang_code, lang_code)
        
        return f"Detected language: {language_name.title()} ({lang_code})"
        
    except Exception as e:
        logging.error(f"Language detection error: {e}")
        return f"Could not detect language. Error: {str(e)}"


# Quick test
if __name__ == "__main__":
    print("Testing translation...")
    
    # Test 1: English to Spanish
    result = translate_text.invoke({"text": "Hello, how are you?", "target_language": "Spanish"})
    print(f"Test 1: {result}")
    
    # Test 2: Detect language
    result = detect_language.invoke({"text": "Bonjour"})
    print(f"Test 2: {result}")
    
    # Test 3: Japanese translation
    result = translate_text.invoke({"text": "Thank you", "target_language": "Japanese"})
    print(f"Test 3: {result}")
