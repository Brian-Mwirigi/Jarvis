# 🧠 MEMORY SYSTEM SETUP GUIDE

Jarvis now has a persistent memory system using ChromaDB!

---

## 📦 **Installation**

```powershell
pip install chromadb
```

That's it! The memory system will automatically initialize on first run.

---

## 🎯 **What Can Jarvis Remember?**

### **1. Personal Facts**
```
You: Remember that my birthday is June 15
Jarvis: I'll remember that: my birthday is June 15

You: What's my birthday?
Jarvis: I remember: my birthday is June 15
```

### **2. Preferences**
```
You: I love pizza
Jarvis: I'll remember that: I love pizza

You: My favorite color is blue
Jarvis: I'll remember that: My favorite color is blue
```

### **3. Work Info**
```
You: I work as a software developer
Jarvis: I'll remember that: I work as a software developer

You: Do you remember what I do for work?
Jarvis: I remember: I work as a software developer
```

### **4. Conversation History**
All conversations are automatically stored for context!

---

## 💬 **How to Use Memory**

### **Store a Memory:**
Use any of these phrases:
- "Remember that [fact]"
- "Remember this: [fact]"
- "Don't forget that [fact]"
- "Keep in mind that [fact]"
- "My name is..."
- "My birthday is..."
- "I love..."
- "I work as..."

### **Recall a Memory:**
Use any of these phrases:
- "Do you remember [what]?"
- "What did I tell you about [topic]?"
- "What do you know about me?"
- "What's my [thing]?"

---

## 📂 **Where Are Memories Stored?**

Memories are stored locally in:
```
~/.jarvis/memory/
```

On Windows:
```
C:\Users\YourName\.jarvis\memory\
```

This folder contains:
- `chroma.sqlite3` - Database file
- Collection data - Vector embeddings

---

## 🔍 **Memory Categories**

Memories are automatically categorized:
- **general** - Miscellaneous facts
- **preference** - Likes/dislikes
- **personal** - Birthday, name, etc.
- **work** - Job, projects, etc.
- **conversation** - Chat history

---

## 🧪 **Test the Memory System**

```powershell
python -c "from tools.memory import *; print(remember_fact.invoke({'fact': 'Test memory', 'category': 'test'})); print(recall_memory.invoke({'query': 'test'}))"
```

---

## 🎮 **Example Conversations**

### **Building Context:**
```
You: Hello
Jarvis: Yes sir, how can I help you?

You: Remember that my name is Alex
Jarvis: I'll remember that: my name is Alex

You: My favorite drink is coffee
Jarvis: I'll remember that: My favorite drink is coffee

You: I'm a Python developer
Jarvis: I'll remember that: I'm a Python developer
```

### **Using Context:**
```
You: What's my name?
Jarvis: I remember: my name is Alex

You: Do you know what I do?
Jarvis: I remember: I'm a Python developer

You: What do you know about me?
Jarvis: Here's what I remember:
• my name is Alex
• My favorite drink is coffee
• I'm a Python developer
```

---

## 🛠️ **Advanced Features**

### **Clear All Memories (Use with Caution!):**
```python
from tools.memory import clear_all_memories
clear_all_memories()
```

### **View Memory Database:**
```python
from tools.memory import memories, conversations

# Count memories
print(f"Total memories: {memories.count()}")
print(f"Total conversations: {conversations.count()}")

# Get all memories
all_memories = memories.get()
print(all_memories)
```

---

## 🔧 **Troubleshooting**

### **Error: "Memory system is not available"**
```powershell
pip install chromadb
```

### **Memories Not Persisting:**
Check that the directory exists and is writable:
```powershell
# Windows
dir ~\.jarvis\memory

# Create if missing
mkdir ~\.jarvis\memory
```

### **Reset Memory System:**
Delete the memory folder:
```powershell
# Windows
Remove-Item -Recurse ~\.jarvis\memory
```

Next run will create a fresh database.

---

## 🚀 **Next Steps**

The memory system is just the beginning! Future improvements:
- **Auto-categorization** - Smarter classification
- **Time-based recall** - "What did we talk about yesterday?"
- **Contextual responses** - Use memories in all responses
- **Memory pruning** - Clean up old/irrelevant memories
- **Export/import** - Backup your memories

---

**Your Jarvis now has a brain!** 🧠✨

