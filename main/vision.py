import os
import logging
import requests
from dotenv import load_dotenv

load_dotenv()
VISION_URL = os.getenv('VISION_URL')
VISION_AVAILABLE = False
vision = None

if VISION_URL:
    logging.info(f"🖼️ Detected VISION_URL: {VISION_URL} — checking /health...")
    try:
        health_resp = requests.get(VISION_URL.rstrip('/') + '/health', timeout=5)
        if health_resp.status_code == 200:
            logging.info("🟢 Vision /health reachable — initializing RemoteVision")
            try:
                from vision_remote import RemoteVision
                vision = RemoteVision()
                VISION_AVAILABLE = getattr(vision, 'available', True)
            except Exception as e:
                logging.warning(f"⚠️ Could not initialize RemoteVision: {e}")
                vision = None
                VISION_AVAILABLE = False
        else:
            logging.warning(f"⚠️ Vision /health returned {health_resp.status_code}; will not initialize vision")
            VISION_AVAILABLE = False
    except Exception as e:
        logging.warning(f"⚠️ Could not reach Vision URL ({VISION_URL}): {e}")
        VISION_AVAILABLE = False
else:
    logging.info("ℹ️ No VISION_URL set; vision features disabled")
