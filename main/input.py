import speech_recognition as sr
import os
import tempfile
import logging
import wave

# Azure Speech SDK for STT
try:
    import azure.cognitiveservices.speech as speechsdk
    AZURE_STT_AVAILABLE = True
    
    # Initialize Azure Speech Config
    AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
    AZURE_REGION = os.getenv("AZURE_REGION", "southafricanorth")
    
    if AZURE_SPEECH_KEY:
        azure_speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_REGION)
        azure_speech_config.speech_recognition_language = "en-US"
        logging.info("[OK] Azure STT initialized")
    else:
        AZURE_STT_AVAILABLE = False
        logging.warning("[Warning] Azure STT not configured")
except ImportError:
    AZURE_STT_AVAILABLE = False
    logging.warning("[Warning] Azure Speech SDK not available")

# Fallback: Try to import Faster Whisper
try:
    from faster_whisper import WhisperModel
    FASTER_WHISPER_AVAILABLE = True
except ImportError:
    FASTER_WHISPER_AVAILABLE = False
    logging.warning("[Warning] faster-whisper not available")

# Initialize Faster Whisper model (lazy loading)
_whisper_model = None

def get_whisper_model():
    """Lazy load the Whisper model"""
    global _whisper_model
    if _whisper_model is None and FASTER_WHISPER_AVAILABLE:
        try:
            _whisper_model = WhisperModel("base", device="cpu", compute_type="int8")
            logging.info("[OK] Faster Whisper model loaded")
        except Exception as e:
            logging.error(f"[ERROR] Failed to load Faster Whisper: {e}")
    return _whisper_model

def listen_for_speech(timeout=5, use_local_stt=True):
    """
    Listen for speech and transcribe using Azure STT (best for accents!).
    Falls back to Google, then Faster Whisper if Azure unavailable.
    
    Args:
        timeout: Maximum seconds to wait for speech
        use_local_stt: If True, can use local Faster Whisper as last resort
    
    Returns:
        str: Transcribed text or None if no speech detected
    """
    recognizer = sr.Recognizer()
    # Lower energy threshold for better sensitivity
    recognizer.energy_threshold = 300  # Lower = more sensitive
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.8  # Shorter pause = faster response
    
    try:
        with sr.Microphone() as source:
            print("[MIC] Listening...", end='', flush=True)
            # Shorter ambient noise adjustment for faster startup
            recognizer.adjust_for_ambient_noise(source, duration=0.3)
            # Listen with more lenient settings
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=15)
            print("\r" + " " * 20 + "\r", end='', flush=True)
            
            # Priority 1: Azure Speech-to-Text (Best for accents!)
            if AZURE_STT_AVAILABLE:
                try:
                    # Save audio to temporary WAV file for Azure
                    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                        wav_path = f.name
                        wav_file = wave.open(wav_path, 'wb')
                        wav_file.setnchannels(1)
                        wav_file.setsampwidth(audio.sample_width)
                        wav_file.setframerate(audio.sample_rate)
                        wav_file.writeframes(audio.get_wav_data())
                        wav_file.close()
                    
                    # Use Azure Speech SDK
                    audio_config = speechsdk.audio.AudioConfig(filename=wav_path)
                    speech_recognizer = speechsdk.SpeechRecognizer(
                        speech_config=azure_speech_config,
                        audio_config=audio_config
                    )
                    
                    result = speech_recognizer.recognize_once()
                    
                    # Cleanup temp file
                    try:
                        os.remove(wav_path)
                    except:
                        pass
                    
                    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                        return result.text.strip()
                    elif result.reason == speechsdk.ResultReason.NoMatch:
                        logging.warning("[Warning] Azure: No speech recognized")
                    else:
                        logging.warning(f"[Warning] Azure STT failed: {result.reason}")
                        
                except Exception as azure_error:
                    logging.warning(f"[Warning] Azure STT error, falling back: {azure_error}")
            
            # Priority 2: Google Speech API (Good fallback)
            try:
                text = recognizer.recognize_google(audio, language="en-US")
                logging.info("🔄 Using Google STT (Azure unavailable)")
                return text.strip()
            except Exception as google_error:
                logging.warning(f"[Warning] Google STT failed: {google_error}")
                
                # Priority 3: Faster Whisper (Last resort)
                if use_local_stt and FASTER_WHISPER_AVAILABLE:
                    try:
                        model = get_whisper_model()
                        if model:
                            # Save audio to temporary WAV file
                            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                                wav_path = f.name
                                wav_file = wave.open(wav_path, 'wb')
                                wav_file.setnchannels(1)
                                wav_file.setsampwidth(audio.sample_width)
                                wav_file.setframerate(audio.sample_rate)
                                wav_file.writeframes(audio.get_wav_data())
                                wav_file.close()
                            
                            # Transcribe with Faster Whisper
                            segments, info = model.transcribe(wav_path, language="en", beam_size=5)
                            text = " ".join([segment.text for segment in segments]).strip()
                            
                            # Cleanup temp file
                            try:
                                os.remove(wav_path)
                            except:
                                pass
                            
                            if text:
                                logging.info("🔄 Using Faster Whisper (Azure & Google unavailable)")
                                return text
                    except Exception as e:
                        logging.error(f"[ERROR] All STT methods failed: {e}")
                
                raise google_error
            
    except sr.WaitTimeoutError:
        print("\r" + " " * 20 + "\r", end='', flush=True)
        return None
    except sr.UnknownValueError:
        print("❓ Could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"[ERROR] Speech recognition error: {e}")
        return None
    except Exception as e:
        print(f"[ERROR] Microphone error: {e}")
        return None
