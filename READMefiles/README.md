# 🧠 Jarvis – AI Voice Assistant

Hybrid cloud-local AI assistant powered by **Phi LLM** (Colab GPU) + **BLIP-2 Vision** (Colab GPU) + **Azure TTS** with LangChain tool-calling.

---

## ⚡ Quick Start

### **1. Install Dependencies**

```bash
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### **2. Setup Google Colab Backend**

1. Open `jarvis_colab_simple_setup.ipynb` in Google Colab
2. Set Runtime → Change runtime type → **GPU (T4)**
3. Run all cells in order (takes ~5 minutes first time)
4. After Cell 7, copy the Flask ngrok URL (e.g., `https://abc123.ngrok-free.app`)

### **3. Configure Environment**

Create a `.env` file (copy from `env.example`):

```bash
# Use the ngrok URL from Colab
OLLAMA_HOST=https://YOUR-NGROK-URL/proxy_ollama
VISION_URL=https://YOUR-NGROK-URL

# Get Azure Speech key from: https://portal.azure.com
AZURE_SPEECH_KEY=your_key_here
AZURE_REGION=southafricanorth
AZURE_VOICE=en-US-JennyNeural
```

### **4. Run Jarvis**

```bash
# Activate venv if not already activated
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Run Jarvis (choose mode interactively)
python -m main.runner

# Or directly run specific mode
python -m main.main_text   # Text input mode
python -m main.main_voice  # Voice input mode
```

**What you get:**
- ✅ Text or voice input modes
- ✅ LLM responses via Colab GPU (free)
- ✅ AI vision analysis (BLIP-2)
- ✅ Azure TTS (high quality) with PowerShell fallback
- ✅ Faster Whisper STT (local, offline)
- ✅ 7+ powerful tools

---

## 💬 Usage

```
💬 You: jarvis
🤖 Jarvis: Yes sir, how can I help you?

💬 You: what time is it in Tokyo?
🤖 Jarvis: The current time in Tokyo is 3:45 PM (Friday, November 06, 2025)

💬 You: search for latest AI news
💬 You: take a screenshot
💬 You: what do you see on the screen?
💬 You: activate matrix mode
💬 You: exit
```

---

## 🔧 Features

| Feature | Details |
|---------|---------|
| 🧠 **LLM** | Phi (1.7B) via Ollama on Colab T4 GPU |
| 👁️ **Vision** | BLIP-2 (2.7B) on Colab T4 GPU |
| 🎙️ **TTS** | Azure Speech Services + PowerShell fallback |
| 🎤 **STT** | Faster Whisper (local, CPU) with Google fallback |
| 🌐 **Backend** | Google Colab (free T4 GPU) + ngrok tunnels |
| 🛠️ **Tools** | 7 tools via LangChain agent |
| 💰 **Cost** | ~$1/month (Azure TTS only) |
| 🔒 **Privacy** | Speech local, LLM/Vision on your Colab |

---

## 🛠️ Available Tools

| Tool | Description | Example |
|------|-------------|---------|
| **Time Zones** | Get time in 60+ cities worldwide | "What time is it in Paris?" |
| **Web Search** | DuckDuckGo search | "Search for latest AI news" |
| **Screenshot** | Capture screen to Pictures/Jarvis/ | "Take a screenshot" |
| **OCR** | Extract text from screenshots | "Read the screen" |
| **Vision** | AI analysis of screen/images | "What do you see?" |
| **ARP Scan** | Show network devices | "Scan my network" |
| **Matrix Mode** | Cool terminal effects | "Enter matrix mode" |

---

## 📊 Architecture

```
┌─────────────────────────────────────────────────────┐
│  YOUR COMPUTER (Windows/Linux/Mac)                  │
│  ┌────────────┐  ┌──────────┐  ┌────────────┐     │
│  │ Microphone │  │ Keyboard │  │  Speakers  │     │
│  └─────┬──────┘  └─────┬────┘  └─────▲──────┘     │
│        │               │              │            │
│  ┌─────▼───────────────▼──────────────┴─────────┐  │
│  │         JARVIS (Python)                      │  │
│  │  - Faster Whisper STT (local)                │  │
│  │  - LangChain Agent                           │  │
│  │  - Azure TTS / PowerShell fallback           │  │
│  └───────┬──────────────────────────┬───────────┘  │
│          │ HTTP/HTTPS               │ HTTP         │
└──────────┼──────────────────────────┼──────────────┘
           │                          │
    ┌──────▼──────────┐      ┌────────▼─────────┐
    │  GOOGLE COLAB   │      │  AZURE CLOUD     │
    │  (Free T4 GPU)  │      │                  │
    │  ┌────────────┐ │      │  ┌────────────┐  │
    │  │ Phi LLM    │ │      │  │ Speech TTS │  │
    │  │ (Ollama)   │ │      │  └────────────┘  │
    │  ├────────────┤ │      └──────────────────┘
    │  │ BLIP-2     │ │      Cost: ~$1/month
    │  │ Vision     │ │
    │  └────────────┘ │
    │  Flask + ngrok  │
    └─────────────────┘
    Cost: FREE
```

---

## 🎯 Why This Setup?

✅ **Near-Zero Cost** - Only Azure TTS (~$1/month), rest is free  
✅ **GPU Acceleration** - Free T4 GPU from Google Colab  
✅ **Private** - Speech processing is local, LLM on your Colab  
✅ **Flexible** - Works on Windows, Linux, Mac  
✅ **Powerful** - Multimodal (text + vision) with tools  
✅ **Graceful Fallback** - Each component has offline alternatives

---

## 🔧 Testing

We've included comprehensive test scripts:

```bash
# Test all components at once
python test_all.py

# Test vision specifically
python test_vision.py

# Test TTS specifically
python test_azure_tts.py
```

---

## 🐛 Troubleshooting

### **"Could not initialize LLM"**
- Ensure Colab notebook is running (`jarvis_colab_simple_setup.ipynb`)
- Check `OLLAMA_HOST` in `.env` matches your ngrok URL
- Verify ngrok tunnel is active in Colab

### **"Vision system unavailable"**
- Same Colab notebook hosts both LLM and Vision
- Check `VISION_URL` in `.env`
- Test: Visit `https://YOUR-NGROK-URL/health` in browser

### **Azure TTS not working**
- Verify `AZURE_SPEECH_KEY` is correct
- Check region matches your Azure resource
- Fallback: PowerShell TTS works automatically on Windows

### **Faster Whisper not working**
- STT automatically falls back to Google Speech API
- For offline: Ensure `faster-whisper` is installed
- Check microphone permissions

### **Import errors**
```bash
pip install -r requirements.txt --upgrade
```

---

## 📁 Project Structure

```
jarvis/
├── main/
│   ├── runner.py          # Entry point (mode selection)
│   ├── main_text.py       # Text input mode
│   ├── main_voice.py      # Voice input mode
│   ├── llm.py             # Ollama/Phi LLM client
│   ├── vision.py          # Vision system loader
│   ├── tts.py             # Azure + PowerShell TTS
│   ├── input.py           # Faster Whisper STT
│   └── utils.py           # Helper functions
├── tools/
│   ├── time.py            # Time zones (60+ cities)
│   ├── duckduckgo.py      # Web search
│   ├── screenshot.py      # Screen capture
│   ├── OCR.py             # Text extraction
│   ├── vision.py          # AI vision analysis
│   ├── arp_scan.py        # Network scan
│   └── matrix.py          # Matrix effect
├── vision_remote.py       # Remote vision client
├── jarvis_colab_simple_setup.ipynb  # Colab backend
├── requirements.txt       # Python dependencies
├── env.example            # Environment template
├── test_all.py            # Comprehensive tests
├── test_vision.py         # Vision tests
└── test_azure_tts.py      # TTS tests
```

---

## 🎨 Customization

### **Change TTS Voice**

Edit `.env`:
```bash
AZURE_VOICE=en-GB-RyanNeural  # British male
# AZURE_VOICE=en-US-JennyNeural  # American female
# AZURE_VOICE=en-IN-NeerjaNeural  # Indian female
```

[Full voice list](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=tts)

### **Change LLM Model**

Edit Colab Cell 4:
```python
subprocess.run(['ollama', 'pull', 'llama2'], check=True)  # Instead of phi
```

Then update `.env`:
```bash
OLLAMA_MODEL=llama2
```

### **Add More Cities**

Edit `tools/time.py` and add to `CITY_TIMEZONES` dict.

### **Customize Agent Prompt**

Edit the system prompt in `main/main_text.py` or `main/main_voice.py`:
```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are Jarvis, a helpful AI assistant..."),
    ...
])
```

---

## 🚀 Advanced

### **Run Without Colab (Local Ollama)**

If you have Ollama installed locally:

```bash
ollama serve
ollama pull phi

# Update .env
OLLAMA_HOST=http://localhost:11434
```

### **Multiple Monitors Screenshot**

Edit `tools/screenshot.py`:
```python
monitor = sct.monitors[0]  # [0] = all monitors, [1] = main, [2] = second
```

### **Offline Mode**

- ✅ STT: Faster Whisper works offline
- ✅ TTS: PowerShell TTS works offline  
- ❌ LLM: Requires Colab or local Ollama
- ❌ Vision: Requires Colab or local BLIP-2
- ❌ Web Search: Requires internet

---

## 📝 License

MIT License - Feel free to use, modify, and distribute!

---

## 🙏 Credits

- **LLM**: [Ollama](https://ollama.ai/) + [Phi](https://huggingface.co/microsoft/phi-2)
- **Vision**: [BLIP-2](https://huggingface.co/Salesforce/blip2-opt-2.7b) by Salesforce
- **Framework**: [LangChain](https://python.langchain.com/)
- **TTS**: [Azure Speech Services](https://azure.microsoft.com/en-us/services/cognitive-services/speech-services/)
- **STT**: [Faster Whisper](https://github.com/guillaumekln/faster-whisper)

---

**Ready to go! Run `python -m main.runner` and say "Jarvis" 🎤**

