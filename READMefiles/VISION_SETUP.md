# 👁️ Vision Module Setup Guide

## 🎯 What You Get
- **Ask "What do you see?"** → Jarvis analyzes your screen
- **"Describe this image"** → Analyzes any image file
- **Free & Fast** → MiniCPM-V model on Colab GPU (2-3s per analysis)
- **Safe & Isolated** → Separate files, won't break main Jarvis

---

## ⚡ Quick Setup (5 minutes)

### **Step 1: Add to Colab Notebook**

Open `jarvis_colab_python312.ipynb` and add these cells at the end:

1. Copy **Cell 10-13** from `VISION_COLAB_CELLS.py`
2. Paste them after your existing Cell 9 (ngrok setup)
3. Run Cell 10 → Installs vision dependencies (~1 min)
4. Run Cell 11 → Loads MiniCPM-V model (~3-5 min first time)
5. Run Cell 12 → Adds vision endpoint to Flask
6. Run Cell 13 → Tests the vision system

### **Step 2: Get Vision URL**

The vision endpoint shares the same Flask server as TTS!

```python
# Your ngrok URL from Cell 9 is ALREADY the vision URL
# Example: https://7b86d3ce40d7.ngrok-free.app
```

### **Step 3: Set Environment Variable**

```powershell
$env:VISION_URL="https://YOUR-TTS-URL.ngrok-free.app"
# Same URL as TTS_URL!
```

### **Step 4: Install Dependencies**

```powershell
pip install Pillow
```

### **Step 5: Test It!**

```powershell
python test_vision.py
```

---

## 🎮 Usage Examples

### **Standalone Test:**
```powershell
python test_vision.py
```

Interactive menu to:
1. Analyze your current screen
2. Ask custom questions
3. Analyze image files

### **In Main Jarvis (Optional Integration):**

To add vision to main Jarvis voice commands, edit `main_text_elevenlabs.py`:

```python
# Add at top
from tools.vision import analyze_screen

# In conversation loop, add voice commands like:
if "what do you see" in user_input.lower():
    result = analyze_screen.invoke({"question": user_input})
    speak_text(result)
```

---

## 📊 Performance

| Task | Speed | Model |
|------|-------|-------|
| Screen capture | <0.5s | Native |
| AI vision analysis | 2-3s | MiniCPM-V (GPU) |
| **Total response** | **~3s** | ⚡ Fast! |

---

## 🎯 What It Can Do

✅ **Describe what's on screen**
- "What do you see?"
- "What app is open?"
- "Read the text on my screen"

✅ **Analyze images**
- "What's in this photo?"
- "Describe this screenshot"
- "What does this diagram show?"

✅ **Answer questions about visuals**
- "What color is the button?"
- "How many windows are open?"
- "What's the title of this page?"

---

## 🔧 Troubleshooting

**Vision URL not set:**
- Use your TTS_URL! Both endpoints share the same Flask server

**"Vision system unavailable":**
- Make sure Colab Cells 10-13 are running
- Check that Cell 12 added the `/vision` endpoint
- Test: `curl YOUR-URL/health` should return 200

**Slow first response:**
- First vision call loads the model (~5-10s)
- Subsequent calls are fast (2-3s)

**Import error:**
- Run: `pip install Pillow`

---

## 🚀 Advanced: Voice Commands

Add these patterns to recognize vision requests:

```python
vision_triggers = [
    "what do you see",
    "describe the screen",
    "what's on my screen",
    "analyze this",
    "look at this"
]

if any(trigger in user_input.lower() for trigger in vision_triggers):
    # Use vision tool
    result = analyze_screen.invoke({"question": user_input})
    speak_text(result)
```

---

## 💡 Pro Tips

1. **Screen analysis is instant** - No need to save screenshots first
2. **Works with multiple monitors** - Captures all screens
3. **Questions matter** - Be specific: "What's the error message?" vs "What do you see?"
4. **Model is smart** - Can read text, identify apps, describe layouts

---

## 📁 Files Created

```
jarvis/
├── vision_remote.py          # Vision client (connects to Colab)
├── tools/vision.py            # LangChain tool wrapper
├── test_vision.py             # Standalone test script
├── VISION_COLAB_CELLS.py      # Colab cells to add
└── VISION_SETUP.md            # This guide
```

**Safe & Isolated** - If vision breaks, main Jarvis still works! ✅

---

**Ready to see the world! 👁️**
