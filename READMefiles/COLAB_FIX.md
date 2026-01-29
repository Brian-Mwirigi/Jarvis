# 🔧 FIX COLAB TIMEOUT ISSUE

## Problem
The Flask `/proxy_ollama` endpoint has a 30-second timeout, which is too short for vision operations.

## Solution
Update the timeout in your Colab notebook.

---

## 📝 STEPS TO FIX:

### 1. Open your Colab notebook
`jarvis_colab_simple_setup.ipynb`

### 2. Find Cell 6 (Flask App Setup)
Look for this line (around line 621):
```python
resp = requests.post('http://localhost:11434/api/chat', data=raw_body, headers=forward_headers, timeout=30)
```

### 3. Change timeout from 30 to 120
```python
resp = requests.post('http://localhost:11434/api/chat', data=raw_body, headers=forward_headers, timeout=120)
```

### 4. Restart the Colab runtime
- Click: `Runtime` → `Restart runtime`
- Re-run all cells (Cell 1 through Cell 9)
- Get new ngrok URLs from Cell 7 output
- Update your `.env` with new URLs

---

## 🎯 QUICK FIX (Alternative)

If you can't edit the notebook right now, you can temporarily work around this by:

1. Using shorter, simpler questions that don't timeout
2. Or just using text-only mode without vision until you update Colab

---

## ✅ After Fix

Once updated, these commands will work:
```
what am I holding?
what do you see?
analyze the camera
```

The timeout will now be 120 seconds instead of 30, giving vision operations enough time to complete.

---

## 📊 What Changed in Your Local Code

I already updated your local `ollama_proxy_adapter.py` to have a 120-second timeout on the client side, but the Colab Flask proxy also needs to match this timeout.

**Both need to be 120 seconds:**
- ✅ Local client: `ollama_proxy_adapter.py` (already fixed)
- ⚠️ Colab Flask: `proxy_ollama` endpoint (needs manual fix)

