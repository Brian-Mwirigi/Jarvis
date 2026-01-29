"""
Comprehensive test script for all Jarvis components
Quick diagnostic to check what's working and what needs configuration
"""
import logging
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

logging.basicConfig(level=logging.WARNING)  # Suppress info logs for cleaner output

def check_imports():
    """Check if all required modules can be imported"""
    print("🔍 Checking Python imports...")
    issues = []
    
    try:
        import langchain
        print("  ✅ langchain")
    except ImportError:
        print("  ❌ langchain - pip install langchain")
        issues.append("langchain")
    
    try:
        import langchain_ollama
        print("  ✅ langchain_ollama")
    except ImportError:
        print("  ❌ langchain_ollama - pip install langchain-ollama")
        issues.append("langchain_ollama")
    
    try:
        import azure.cognitiveservices.speech
        print("  ✅ azure.cognitiveservices.speech")
    except ImportError:
        print("  ❌ azure-cognitiveservices-speech - pip install azure-cognitiveservices-speech")
        issues.append("azure-cognitiveservices-speech")
    
    try:
        import faster_whisper
        print("  ✅ faster-whisper")
    except ImportError:
        print("  ⚠️  faster-whisper (optional) - pip install faster-whisper")
    
    try:
        import mss
        print("  ✅ mss")
    except ImportError:
        print("  ❌ mss - pip install mss")
        issues.append("mss")
    
    try:
        import pytesseract
        print("  ✅ pytesseract")
    except ImportError:
        print("  ❌ pytesseract - pip install pytesseract")
        issues.append("pytesseract")
    
    try:
        from duckduckgo_search import DDGS
        print("  ✅ duckduckgo-search")
    except ImportError:
        print("  ❌ duckduckgo-search - pip install duckduckgo-search")
        issues.append("duckduckgo-search")
    
    return issues

def check_environment():
    """Check environment variables"""
    print("\n🔍 Checking environment variables...")
    
    ollama_host = os.getenv("OLLAMA_HOST") or os.getenv("OLLAMA_URL")
    vision_url = os.getenv("VISION_URL")
    azure_key = os.getenv("AZURE_SPEECH_KEY", "YOUR_KEY")
    
    if ollama_host:
        print(f"  ✅ OLLAMA_HOST: {ollama_host[:50]}...")
    else:
        print("  ⚠️  OLLAMA_HOST not set (LLM will not work)")
    
    if vision_url:
        print(f"  ✅ VISION_URL: {vision_url[:50]}...")
    else:
        print("  ⚠️  VISION_URL not set (Vision features disabled)")
    
    if azure_key and azure_key != "YOUR_KEY":
        print(f"  ✅ AZURE_SPEECH_KEY: {azure_key[:10]}...")
    else:
        print("  ⚠️  AZURE_SPEECH_KEY not set (Will use local TTS fallback)")

def test_llm():
    """Test LLM connectivity"""
    print("\n🔍 Testing LLM connectivity...")
    try:
        from main.llm import init_llm, ollama_client
        init_llm()
        if ollama_client:
            print("  ✅ LLM client initialized")
        else:
            print("  ❌ LLM client failed to initialize")
    except Exception as e:
        print(f"  ❌ LLM error: {e}")

def test_vision():
    """Test vision connectivity"""
    print("\n🔍 Testing vision connectivity...")
    try:
        from main.vision import VISION_AVAILABLE
        if VISION_AVAILABLE:
            print("  ✅ Vision system available")
        else:
            print("  ⚠️  Vision system not available")
    except Exception as e:
        print(f"  ❌ Vision error: {e}")

def test_tools():
    """Test tool imports"""
    print("\n🔍 Testing tools...")
    
    tools = [
        ("Time", "tools.time", "get_time"),
        ("DuckDuckGo Search", "tools.duckduckgo", "duckduckgo_search_tool"),
        ("Screenshot", "tools.screenshot", "take_screenshot"),
        ("OCR", "tools.OCR", "read_text_from_latest_image"),
        ("ARP Scan", "tools.arp_scan", "arp_scan_terminal"),
        ("Matrix Mode", "tools.matrix", "matrix_mode"),
    ]
    
    for name, module, func in tools:
        try:
            mod = __import__(module, fromlist=[func])
            getattr(mod, func)
            print(f"  ✅ {name}")
        except Exception as e:
            print(f"  ❌ {name}: {e}")

def main():
    print("=" * 60)
    print("🧪 JARVIS COMPREHENSIVE DIAGNOSTIC")
    print("=" * 60)
    
    # Run all checks
    import_issues = check_imports()
    check_environment()
    test_llm()
    test_vision()
    test_tools()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    
    if import_issues:
        print(f"\n⚠️  Missing {len(import_issues)} required package(s):")
        for pkg in import_issues:
            print(f"    - {pkg}")
        print("\nInstall missing packages:")
        print(f"    pip install {' '.join(import_issues)}")
    else:
        print("\n✅ All required packages are installed!")
    
    print("\n💡 Next steps:")
    print("  1. Configure environment variables (see env.example)")
    print("  2. Start Colab notebook (jarvis_colab_simple_setup.ipynb)")
    print("  3. Run Jarvis: python -m main.runner")
    print("\n" + "=" * 60)
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n👋 Test interrupted. Goodbye!")
        sys.exit(0)

