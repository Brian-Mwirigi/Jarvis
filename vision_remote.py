"""
Remote Vision Client - connects to Colab GPU for vision/image analysis
Uses BLIP-2 model (fast, free, multimodal)
"""
import logging
import requests
import base64
import os
from PIL import ImageGrab, Image
import io
import cv2
import numpy as np


class RemoteVision:
    def __init__(self, server_url: str = None):
        """
        Initialize remote vision client
        
        Args:
            server_url: URL of vision server (from Colab ngrok)
                       Falls back to env var VISION_URL
        """
        self.server_url = server_url or os.getenv("VISION_URL")
        self.available = self._check_server()
        
    def _check_server(self) -> bool:
        """Check if vision server is reachable"""
        if not self.server_url:
            logging.warning("⚠️ VISION_URL not set")
            return False
        try:
            headers = {"ngrok-skip-browser-warning": "true"}
            r = requests.get(f"{self.server_url}/health", headers=headers, timeout=5)
            if r.status_code == 200:
                logging.info("✅ Remote Vision connected")
                return True
        except Exception as e:
            logging.warning(f"⚠️ Remote Vision unavailable: {e}")
        return False
    
    def capture_screenshot(self) -> bytes:
        """Capture current screen and return as bytes"""
        try:
            screenshot = ImageGrab.grab()
            img_byte_arr = io.BytesIO()
            screenshot.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            return img_byte_arr.getvalue()
        except Exception as e:
            logging.error(f"❌ Screenshot error: {e}")
            return None
    
    def capture_camera(self) -> bytes:
        """Capture image from webcam and return as bytes"""
        try:
            logging.info("📷 Opening camera...")
            cap = cv2.VideoCapture(0)  # 0 = default camera
            
            if not cap.isOpened():
                logging.error("❌ Could not open camera")
                return None
            
            # Read frame
            ret, frame = cap.read()
            cap.release()
            
            if not ret:
                logging.error("❌ Could not read from camera")
                return None
            
            # Convert BGR to RGB (OpenCV uses BGR, PIL uses RGB)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Convert to PIL Image
            image = Image.fromarray(frame_rgb)
            
            # Convert to bytes
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            
            logging.info("✅ Camera capture successful")
            return img_byte_arr.getvalue()
            
        except Exception as e:
            logging.error(f"❌ Camera error: {e}")
            return None
    
    def analyze_screen(self, question: str = "What do you see?") -> str:
        """
        Analyze current screen with AI vision
        
        Args:
            question: What to ask about the image
            
        Returns:
            str: AI description/answer
        """
        if not self.available:
            return "Vision system unavailable"
        
        try:
            # Capture screen
            logging.info("📸 Capturing screen...")
            img_bytes = self.capture_screenshot()
            if not img_bytes:
                return "Failed to capture screen"
            
            # Encode to base64
            img_base64 = base64.b64encode(img_bytes).decode('utf-8')
            
            # Send to vision API
            logging.info("👁️ Analyzing with AI vision...")
            headers = {"ngrok-skip-browser-warning": "true"}
            response = requests.post(
                f"{self.server_url}/vision",
                json={
                    "image": img_base64,
                    "question": question
                },
                headers=headers,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                answer = result.get('answer', 'No response')
                logging.info("✅ Vision analysis complete")
                return answer
            else:
                logging.error(f"❌ Vision failed: {response.status_code}")
                return "Vision analysis failed"
                
        except Exception as e:
            logging.error(f"❌ Vision error: {e}")
            return f"Vision error: {str(e)}"
    
    def analyze_camera(self, question: str = "What do you see?") -> str:
        """
        Analyze webcam view with AI vision
        
        Args:
            question: What to ask about the image
            
        Returns:
            str: AI description/answer
        """
        if not self.available:
            return "Vision system unavailable"
        
        try:
            # Capture from camera
            logging.info("📷 Capturing from camera...")
            img_bytes = self.capture_camera()
            if not img_bytes:
                return "Failed to capture from camera"
            
            # Encode to base64
            img_base64 = base64.b64encode(img_bytes).decode('utf-8')
            
            # Send to vision API
            logging.info("👁️ Analyzing with AI vision...")
            headers = {"ngrok-skip-browser-warning": "true"}
            response = requests.post(
                f"{self.server_url}/vision",
                json={
                    "image": img_base64,
                    "question": question
                },
                headers=headers,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                answer = result.get('answer', 'No response')
                logging.info("✅ Vision analysis complete")
                return answer
            else:
                logging.error(f"❌ Vision failed: {response.status_code}")
                return "Vision analysis failed"
                
        except Exception as e:
            logging.error(f"❌ Vision error: {e}")
            return f"Vision error: {str(e)}"
    
    def analyze_image_file(self, image_path: str, question: str = "What's in this image?") -> str:
        """
        Analyze an image file with AI vision
        
        Args:
            image_path: Path to image file
            question: What to ask about the image
            
        Returns:
            str: AI description/answer
        """
        if not self.available:
            return "Vision system unavailable"
        
        try:
            # Read image file
            with open(image_path, 'rb') as f:
                img_bytes = f.read()
            
            # Encode to base64
            img_base64 = base64.b64encode(img_bytes).decode('utf-8')
            
            # Send to vision API
            logging.info(f"👁️ Analyzing image: {image_path}")
            headers = {"ngrok-skip-browser-warning": "true"}
            response = requests.post(
                f"{self.server_url}/vision",
                json={
                    "image": img_base64,
                    "question": question
                },
                headers=headers,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                answer = result.get('answer', 'No response')
                logging.info("✅ Vision analysis complete")
                return answer
            else:
                logging.error(f"❌ Vision failed: {response.status_code}")
                return "Vision analysis failed"
                
        except Exception as e:
            logging.error(f"❌ Vision error: {e}")
            return f"Vision error: {str(e)}"


# Quick test
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    vision = RemoteVision()
    
    if vision.available:
        print("\n🎥 Vision Test:")
        print("Analyzing current screen...")
        result = vision.analyze_screen("What do you see on this screen?")
        print(f"\n👁️ Answer: {result}")
    else:
        print("⚠️ Vision server not available. Set VISION_URL environment variable.")
