"""
Test script for Jarvis Vision System
Tests the remote vision endpoint (BLIP-2 on Colab)
"""
import logging
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from vision_remote import RemoteVision

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def main():
    print("=" * 60)
    print("🧪 JARVIS VISION TEST")
    print("=" * 60)
    
    # Initialize vision client
    print("\n1️⃣ Initializing Vision Client...")
    vision = RemoteVision()
    
    if not vision.available:
        print("❌ Vision system is not available!")
        print("\nPlease ensure:")
        print("  1. Colab notebook is running (jarvis_colab_simple_setup.ipynb)")
        print("  2. VISION_URL environment variable is set")
        print(f"     Current VISION_URL: {os.getenv('VISION_URL', 'NOT SET')}")
        print("  3. Flask server is accessible")
        return 1
    
    print("✅ Vision client connected!")
    
    # Interactive menu
    while True:
        print("\n" + "=" * 60)
        print("Choose a test:")
        print("  1. Analyze current screen")
        print("  2. Analyze screen with custom question")
        print("  3. Analyze webcam")
        print("  4. Analyze image file")
        print("  5. Exit")
        print("=" * 60)
        
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice == "1":
            print("\n📸 Capturing and analyzing screen...")
            result = vision.analyze_screen("What do you see on this screen?")
            print(f"\n👁️ Answer: {result}\n")
        
        elif choice == "2":
            question = input("\n❓ Enter your question: ").strip()
            if question:
                print(f"\n📸 Capturing screen and answering: {question}")
                result = vision.analyze_screen(question)
                print(f"\n👁️ Answer: {result}\n")
        
        elif choice == "3":
            print("\n📷 Capturing from webcam...")
            result = vision.analyze_camera("What do you see?")
            print(f"\n👁️ Answer: {result}\n")
        
        elif choice == "4":
            image_path = input("\n📁 Enter image file path: ").strip()
            if image_path and os.path.exists(image_path):
                question = input("❓ Enter your question (or press Enter for default): ").strip()
                if not question:
                    question = "What's in this image?"
                print(f"\n🖼️ Analyzing image: {image_path}")
                result = vision.analyze_image_file(image_path, question)
                print(f"\n👁️ Answer: {result}\n")
            else:
                print("❌ Image file not found!")
        
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

