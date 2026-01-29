# 🔧 FIX COLAB FLASK TIMEOUT

## The Problem
The Flask proxy on Colab has a 30-second timeout, but some operations take longer.

## The Solution
Update the timeout in your Colab notebook from 30 to 120 seconds.

---

## 📝 STEPS:

### 1. Open Colab
Go to: `jarvis_colab_simple_setup.ipynb`

### 2. Find Cell 6 (Flask Setup)
Look for this line:
```python
resp = requests.post('http://localhost:11434/api/chat', data=raw_body, headers=forward_headers, timeout=30)
```

### 3. Change timeout
Replace `timeout=30` with `timeout=120`:
```python
resp = requests.post('http://localhost:11434/api/chat', data=raw_body, headers=forward_headers, timeout=120)
```

### 4. Restart
- Click: `Runtime` → `Restart runtime`
- Re-run all cells
- Get new ngrok URLs from Cell 7
- Update `.env` with new URLs

---

## ⚡ WHY THIS HELPS

With the new keyword-based routing, most queries bypass the slow agent and work instantly. But for complex queries that need the agent, the 120-second timeout prevents errors.

---

**This is optional but recommended for complex agent queries!**

