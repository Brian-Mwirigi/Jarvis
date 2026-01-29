import os
import logging
import subprocess
import azure.cognitiveservices.speech as speechsdk

AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY", "YOUR_KEY")
AZURE_REGION = os.getenv("AZURE_REGION", "southafricanorth")
AZURE_VOICE = os.getenv("AZURE_VOICE", "en-US-JennyNeural")

# Initialize Azure Speech if key is configured
azure_available = AZURE_SPEECH_KEY and AZURE_SPEECH_KEY != "YOUR_KEY"
if azure_available:
    try:
        speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_REGION)
        speech_config.speech_synthesis_voice_name = AZURE_VOICE
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
        logging.info(f"✅ Azure TTS initialized ({AZURE_VOICE})")
    except Exception as e:
        logging.warning(f"⚠️ Azure TTS initialization failed: {e}")
        azure_available = False
        speech_synthesizer = None
else:
    speech_synthesizer = None
    logging.info("ℹ️ Azure TTS not configured, will use local fallback")

# Quick acknowledgments that use local TTS
QUICK_RESPONSES = {
    "yes sir",
    "yes sir?",
    "yes sir, how can i help you?",
    "goodbye sir",
    "one moment sir",
    "certainly sir",
    "right away sir",
    "understood sir",
}

def speak_local(text: str):
    """
    Local PowerShell TTS for quick acknowledgments.
    Fast, synchronous, used for greetings and confirmations.
    """
    try:
        logging.info(f"🗣️ Local TTS (quick): {text}")
        print(f"🔊 Speaking: {text}")
        
        # Escape quotes in text
        safe_text = text.replace('"', '`"')
        
        ps_command = f'''
Add-Type -AssemblyName System.Speech
$speak = New-Object System.Speech.Synthesis.SpeechSynthesizer
$speak.Rate = 0
$speak.Volume = 100
$speak.Speak("{safe_text}")
'''
        # Run synchronously for quick responses (wait for completion)
        subprocess.run(
            ["powershell", "-Command", ps_command],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0,
            timeout=5
        )
        logging.info("✅ Local TTS complete")
    except Exception as e:
        logging.error(f"❌ Local TTS error: {e}")

def speak_text(text: str):
    """
    Azure TTS for full responses. High quality, natural voice.
    Falls back to local TTS if Azure is not configured.
    """
    # Check if this is a quick acknowledgment
    if text.lower().strip() in QUICK_RESPONSES:
        logging.info("Using local TTS for quick acknowledgment")
        speak_local(text)
        return
    
    # Try Azure first for full responses
    if azure_available and speech_synthesizer:
        try:
            logging.info(f"🗣️ Azure TTS: {text[:50]}...")
            print(f"🔊 Speaking (Azure): {text}")
            
            # Use synchronous call for Azure TTS
            result = speech_synthesizer.speak_text(text)
            
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                logging.info("✅ Azure TTS complete")
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation = result.cancellation_details
                logging.error(f"❌ Azure TTS canceled: {cancellation.reason}")
                if cancellation.reason == speechsdk.CancellationReason.Error:
                    logging.error(f"Error details: {cancellation.error_details}")
                # Fallback to local
                speak_local(text)
        except Exception as e:
            logging.error(f"❌ Azure TTS error: {e}")
            # Fallback to local
            speak_local(text)
    else:
        # Use local TTS as fallback
        logging.info("Using local TTS (Azure not configured)")
        speak_local(text)
