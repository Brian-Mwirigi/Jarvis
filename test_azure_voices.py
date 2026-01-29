"""
Test different Azure TTS voices to find the perfect J.A.R.V.I.S. sound
"""
import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

import os
from dotenv import load_dotenv
load_dotenv()


# Test voices - Deep, mature voices like Jamie on macOS
voices = {
    "1. Andrew (Deep US Male)": "en-US-AndrewNeural",
    "2. Eric (Deep Mature)": "en-US-EricNeural",
    "3. Roger (Deep Calm)": "en-US-RogerNeural",
    "4. Steffan (Deep Relaxed)": "en-US-SteffanNeural",
    "5. Thomas (Deep British)": "en-GB-ThomasNeural",
    "6. Guy (Professional)": "en-US-GuyNeural",
    "7. Ryan (British)": "en-GB-RyanNeural",
    "8. Davis (Warm)": "en-US-DavisNeural",
}

test_phrase = "Good evening, sir. All systems operational. How may I assist you today?"

print("="*60)
print("🎤 AZURE VOICE TESTER")
print("="*60)
print("\nTesting voices for J.A.R.V.I.S.-like quality:")
print("Listen and choose your favorite!\n")

# Import Azure Speech SDK directly for testing
import azure.cognitiveservices.speech as speechsdk

AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_REGION = os.getenv("AZURE_REGION", "southafricanorth")

if not AZURE_SPEECH_KEY:
    print("\n❌ Error: AZURE_SPEECH_KEY not found in .env file")
    print("Please set up Azure TTS first!")
    exit(1)

for name, voice_name in voices.items():
    print(f"\n{name}")
    print(f"   Voice: {voice_name}")
    print(f"   Speaking: \"{test_phrase}\"")
    
    try:
        # Create speech config for this voice
        speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_REGION)
        speech_config.speech_synthesis_voice_name = voice_name
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
        
        # Speak
        result = speech_synthesizer.speak_text(test_phrase)
        
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("   ✅ Playing...")
        else:
            print(f"   ❌ Failed: {result.reason}")
        
        input("   Press Enter for next voice...")
    except Exception as e:
        print(f"   Error: {e}")

print("\n" + "="*60)
print("✅ Voice test complete!")
print("\nTo change permanently, update your .env file:")
print("   AZURE_VOICE=en-GB-RyanNeural")
print("\nMy recommendations:")
print("   ⭐ en-GB-RyanNeural - Most J.A.R.V.I.S.-like")
print("   ⭐ en-US-GuyNeural - Professional US male")
print("="*60)

