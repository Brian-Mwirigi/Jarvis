"""
Memory Tool for Jarvis - Remember conversations and user preferences
Uses ChromaDB for persistent vector storage
"""
from langchain.tools import tool
import chromadb
from chromadb.config import Settings
import os
from datetime import datetime
import logging

# Initialize ChromaDB client
MEMORY_DIR = os.path.join(os.path.expanduser("~"), ".jarvis", "memory")
os.makedirs(MEMORY_DIR, exist_ok=True)

try:
    client = chromadb.PersistentClient(path=MEMORY_DIR)
    # Create or get collections
    memories = client.get_or_create_collection(
        name="memories",
        metadata={"description": "User facts and preferences"}
    )
    conversations = client.get_or_create_collection(
        name="conversations",
        metadata={"description": "Conversation history"}
    )
    MEMORY_AVAILABLE = True
    logging.info("✅ Memory system initialized")
except Exception as e:
    MEMORY_AVAILABLE = False
    logging.warning(f"⚠️ Memory system unavailable: {e}")


@tool
def remember_fact(fact: str, category: str = "general") -> str:
    """
    Store a fact or preference about the user for long-term memory.
    Use this when the user tells you something about themselves that you should remember.
    
    Args:
        fact: The information to remember (e.g., "User's favorite color is blue")
        category: Category of the memory (e.g., "preference", "personal", "work")
    
    Examples:
        - User says: "My birthday is June 15" → remember_fact("User's birthday is June 15", "personal")
        - User says: "I love pizza" → remember_fact("User loves pizza", "preference")
        - User says: "I work as a developer" → remember_fact("User works as a developer", "work")
    
    Returns:
        Confirmation message
    """
    if not MEMORY_AVAILABLE:
        return "Memory system is not available."
    
    try:
        memory_id = f"fact_{datetime.now().timestamp()}"
        memories.add(
            documents=[fact],
            metadatas=[{
                "category": category,
                "timestamp": datetime.now().isoformat(),
                "type": "fact"
            }],
            ids=[memory_id]
        )
        return f"I'll remember that: {fact}"
    except Exception as e:
        logging.error(f"Memory storage error: {e}")
        return f"I had trouble remembering that: {e}"


@tool
def recall_memory(query: str, limit: int = 3) -> str:
    """
    Search memories for relevant information about the user.
    Use this when you need to recall something the user told you before.
    
    Args:
        query: What to search for (e.g., "birthday", "favorite color", "work")
        limit: Maximum number of memories to retrieve (default: 3)
    
    Examples:
        - User asks: "What's my birthday?" → recall_memory("birthday")
        - User asks: "What did I tell you about my job?" → recall_memory("work job")
        - User asks: "Do you remember my favorite food?" → recall_memory("favorite food")
    
    Returns:
        Retrieved memories or message if nothing found
    """
    if not MEMORY_AVAILABLE:
        return "Memory system is not available."
    
    try:
        results = memories.query(
            query_texts=[query],
            n_results=limit
        )
        
        if not results['documents'][0]:
            return "I don't have any memories about that."
        
        # Format the memories
        retrieved = results['documents'][0]
        if len(retrieved) == 1:
            return f"I remember: {retrieved[0]}"
        else:
            memory_list = "\n".join([f"• {mem}" for mem in retrieved])
            return f"Here's what I remember:\n{memory_list}"
            
    except Exception as e:
        logging.error(f"Memory recall error: {e}")
        return f"I had trouble recalling that: {e}"


@tool
def store_conversation(user_message: str, assistant_response: str) -> str:
    """
    Store a conversation exchange for context.
    This is called automatically to maintain conversation history.
    
    Args:
        user_message: What the user said
        assistant_response: What Jarvis responded
    
    Returns:
        Confirmation
    """
    if not MEMORY_AVAILABLE:
        return "Memory system is not available."
    
    try:
        convo_id = f"convo_{datetime.now().timestamp()}"
        conversations.add(
            documents=[f"User: {user_message}\nJarvis: {assistant_response}"],
            metadatas=[{
                "timestamp": datetime.now().isoformat(),
                "type": "conversation"
            }],
            ids=[convo_id]
        )
        return "Conversation stored"
    except Exception as e:
        logging.error(f"Conversation storage error: {e}")
        return f"Error storing conversation: {e}"


@tool
def get_conversation_context(query: str, limit: int = 5) -> str:
    """
    Retrieve relevant past conversations for context.
    Use this when you need to reference previous conversations.
    
    Args:
        query: What conversation to search for
        limit: Number of conversations to retrieve (default: 5)
    
    Examples:
        - "What did we talk about yesterday?"
        - "Did I ask about this before?"
    
    Returns:
        Retrieved conversation snippets
    """
    if not MEMORY_AVAILABLE:
        return "Memory system is not available."
    
    try:
        results = conversations.query(
            query_texts=[query],
            n_results=limit
        )
        
        if not results['documents'][0]:
            return "I don't recall that conversation."
        
        # Format the conversations
        convos = results['documents'][0]
        if len(convos) == 1:
            return f"Here's what we discussed:\n{convos[0]}"
        else:
            convo_list = "\n\n".join([f"{i+1}. {conv}" for i, conv in enumerate(convos)])
            return f"Here are our past conversations:\n\n{convo_list}"
            
    except Exception as e:
        logging.error(f"Context retrieval error: {e}")
        return f"I had trouble finding that conversation: {e}"


def clear_all_memories():
    """Admin function to clear all memories (use with caution!)"""
    if not MEMORY_AVAILABLE:
        return "Memory system is not available."
    
    try:
        client.delete_collection("memories")
        client.delete_collection("conversations")
        client.get_or_create_collection("memories")
        client.get_or_create_collection("conversations")
        return "All memories cleared"
    except Exception as e:
        return f"Error clearing memories: {e}"


# Quick test
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("\n🧪 Testing Memory System:")
    
    if MEMORY_AVAILABLE:
        print("\n1. Storing a fact...")
        result = remember_fact.invoke({
            "fact": "User's favorite color is blue",
            "category": "preference"
        })
        print(f"   {result}")
        
        print("\n2. Recalling the fact...")
        result = recall_memory.invoke({"query": "favorite color"})
        print(f"   {result}")
        
        print("\n3. Storing a conversation...")
        result = store_conversation.invoke({
            "user_message": "What's the weather today?",
            "assistant_response": "It's sunny and 75 degrees."
        })
        print(f"   {result}")
        
        print("\n✅ Memory system working!")
    else:
        print("❌ Memory system not available")

