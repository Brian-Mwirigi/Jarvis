# 🎤 AZURE VOICE OPTIONS FOR JARVIS

Perfect voices to make Jarvis sound more natural and sophisticated!

---

## 🎯 **TOP RECOMMENDATIONS (J.A.R.V.I.S.-like)**

### **1. en-US-GuyNeural** ⭐⭐⭐⭐⭐
- **Style:** Professional, mature, clear
- **Tone:** Calm, intelligent, sophisticated
- **Best for:** J.A.R.V.I.S.-style assistant
- **Perfect match!**

### **2. en-GB-RyanNeural** ⭐⭐⭐⭐⭐
- **Style:** British, sophisticated, refined
- **Tone:** Polite, professional, authoritative
- **Best for:** Classic butler/assistant vibe
- **Very J.A.R.V.I.S.-like with British accent!**

### **3. en-US-DavisNeural** ⭐⭐⭐⭐
- **Style:** Warm, natural, conversational
- **Tone:** Friendly but professional
- **Best for:** Modern AI assistant

### **4. en-GB-ThomasNeural** ⭐⭐⭐⭐
- **Style:** Deep, authoritative, mature
- **Tone:** Serious, professional
- **Best for:** Commanding presence

---

## 🎬 **SPECIAL STYLES (Advanced)**

Some voices support special styles:

### **en-US-GuyNeural** with styles:
- `newscast` - Professional news anchor
- `angry` - Intense/urgent
- `cheerful` - Upbeat
- `sad` - Subdued
- `excited` - Energetic
- `friendly` - Warm

### **en-GB-RyanNeural** with styles:
- `chat` - Casual conversation
- `cheerful` - Upbeat British
- `sad` - Subdued British

---

## 🔧 **HOW TO CHANGE**

### **Option 1: Update .env file**
```bash
# Open .env
notepad .env

# Change this line:
AZURE_VOICE=en-US-JennyNeural

# To one of these:
AZURE_VOICE=en-US-GuyNeural        # ⭐ Best for J.A.R.V.I.S.
AZURE_VOICE=en-GB-RyanNeural       # ⭐ British sophistication
AZURE_VOICE=en-US-DavisNeural      # Natural male
AZURE_VOICE=en-GB-ThomasNeural     # Deep authoritative
```

### **Option 2: Test voices interactively**

Run this to hear different voices:

```powershell
python test_azure_voices.py
```

---

## 🎮 **TEST A VOICE NOW**

```powershell
# Windows PowerShell
$env:AZURE_VOICE="en-US-GuyNeural"
python test_azure_tts.py
```

Or create a quick test script:

```python
from main.tts import speak_text
import os

# Set voice
os.environ['AZURE_VOICE'] = 'en-US-GuyNeural'

# Test
speak_text("Good evening, sir. All systems online.")
```

---

## 🌍 **OTHER LANGUAGES**

### **British English:**
- `en-GB-RyanNeural` - Professional British
- `en-GB-ThomasNeural` - Deep British
- `en-GB-AlfieNeural` - Young British

### **Australian English:**
- `en-AU-WilliamNeural` - Australian male

### **Canadian English:**
- `en-CA-LiamNeural` - Canadian male

---

## 💡 **MY RECOMMENDATION**

**For the best J.A.R.V.I.S. experience:**

```bash
AZURE_VOICE=en-GB-RyanNeural
```

This gives you:
✅ British sophistication
✅ Professional tone
✅ Clear articulation
✅ J.A.R.V.I.S.-like quality

---

## 🎨 **ADVANCED: Voice with Style**

You can also specify speaking style in code:

```python
# In main/tts.py, update synthesizer:
voice_config = f"""
<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>
    <voice name='en-US-GuyNeural'>
        <prosody rate='0%' pitch='0%'>
            <mstts:express-as style='newscast'>
                {text}
            </mstts:express-as>
        </prosody>
    </voice>
</speak>
"""
```

---

## 🧪 **COMPARISON**

| Voice | Accent | Tone | J.A.R.V.I.S. Match |
|-------|--------|------|-------------------|
| GuyNeural | US | Professional | ⭐⭐⭐⭐⭐ |
| RyanNeural | British | Sophisticated | ⭐⭐⭐⭐⭐ |
| DavisNeural | US | Warm | ⭐⭐⭐⭐ |
| ThomasNeural | British | Deep | ⭐⭐⭐⭐ |
| JennyNeural | US | Friendly Female | ⭐⭐ |

---

## 🚀 **QUICK CHANGE**

Update your `.env` right now:

```powershell
# Open .env
notepad .env

# Change to:
AZURE_VOICE=en-GB-RyanNeural

# Save and test:
python -m main.runner
```

---

**Try `en-GB-RyanNeural` or `en-US-GuyNeural` for the perfect J.A.R.V.I.S. voice!** 🎤✨

