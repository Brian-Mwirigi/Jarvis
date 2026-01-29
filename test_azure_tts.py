"""
Test script for Jarvis Azure TTS
Tests both Azure Speech and local PowerShell TTS fallback
"""
import logging
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from main.tts import speak_text, speak_local

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def main():
    print("=" * 60)
    print("🧪 JARVIS TTS TEST")
    print("=" * 60)
    
    # Check Azure configuration
    azure_key = os.getenv("AZURE_SPEECH_KEY", "YOUR_KEY")
    azure_region = os.getenv("AZURE_REGION", "southafricanorth")
    azure_voice = os.getenv("AZURE_VOICE", "en-US-JennyNeural")
    
    print("\n📋 Configuration:")
    print(f"  Azure Speech Key: {'✅ Set' if azure_key != 'YOUR_KEY' else '❌ Not set'}")
    print(f"  Azure Region: {azure_region}")
    print(f"  Azure Voice: {azure_voice}")
    
    # Interactive menu
    while True:
        print("\n" + "=" * 60)
        print("Choose a test:")
        print("  1. Test Azure TTS")
        print("  2. Test Local PowerShell TTS")
        print("  3. Test custom text (Azure)")
        print("  4. Test custom text (Local)")
        print("  5. Exit")
        print("=" * 60)
        
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice == "1":
            print("\n🔊 Testing Azure TTS...")
            if azure_key == "YOUR_KEY":
                print("⚠️ Warning: AZURE_SPEECH_KEY not configured!")
            speak_text("Hello sir, this is Azure text to speech. How can I help you today?")
            print("✅ Azure TTS test complete")
        
        elif choice == "2":
            print("\n🔊 Testing Local PowerShell TTS...")
            speak_local("Hello sir, this is local PowerShell text to speech. This is the fallback option.")
            print("✅ Local TTS test complete")
        
        elif choice == "3":
            text = input("\n💬 Enter text to speak (Azure): ").strip()
            if text:
                print(f"\n🔊 Speaking with Azure TTS: {text}")
                speak_text(text)
                print("✅ Done")
        
        elif choice == "4":
            text = input("\n💬 Enter text to speak (Local): ").strip()
            if text:
                print(f"\n🔊 Speaking with Local TTS: {text}")
                speak_local(text)
                print("✅ Done")
        
        elif choice == "5":
            print("\n👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice!")
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n👋 Test interrupted. Goodbye!")
        sys.exit(0)

