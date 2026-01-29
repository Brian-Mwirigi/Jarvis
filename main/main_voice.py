import sys
import time
import os
import logging
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import ChatPromptTemplate
import main.llm as llm_module
from main.llm import init_llm, OLLAMA_MODEL
from main.vision import VISION_AVAILABLE, vision
from main.tts import speak_local, speak_text
from main.utils import choose_best_sentence, is_refusal
from main.input import listen_for_speech


from tools.time import get_time
from tools.duckduckgo import duckduckgo_search_tool
from tools.screenshot import take_screenshot
from tools.OCR import read_text_from_latest_image
from tools.arp_scan import arp_scan_terminal
from tools.matrix import matrix_mode
from tools.file_operations import (
    create_file,
    read_file as fo_read_file,
    write_file as fo_write_file,
    delete_path as fo_delete_path,
    list_dir as fo_list_dir,
    open_application as fo_open_application,
)

# Memory system
try:
    from tools.memory import remember_fact, recall_memory, store_conversation, get_conversation_context, MEMORY_AVAILABLE
except ImportError:
    MEMORY_AVAILABLE = False
    logging.warning("[Warning] Memory tools not available")

# Journal system
try:
    from tools.journal import log_project_day, get_project_day, get_day_accomplishments, get_today_summary, get_project_summary
    JOURNAL_AVAILABLE = True
except ImportError:
    JOURNAL_AVAILABLE = False
    logging.warning("[Warning] Journal tools not available")

# Conditionally import vision tools
if VISION_AVAILABLE:
    from tools.vision import analyze_screen, analyze_camera, analyze_image

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def main():
    """Voice-based interaction loop"""
    
    # Initialize LLM
    init_llm()
    
    # Check if LLM initialization succeeded
    if llm_module.llm is None and llm_module.ollama_client is None:
        print("\n" + "="*60)
        print("[ERROR] ERROR: Could not connect to LLM backend")
        print("="*60)
        print("\n[Search] Troubleshooting steps:")
        print("\n1. Check your .env file exists and has:")
        print("   OLLAMA_HOST=https://YOUR-NGROK-URL/proxy_ollama")
        print("   VISION_URL=https://YOUR-NGROK-URL")
        print("\n2. Verify your Colab notebook is running:")
        print("   • Open: jarvis_colab_simple_setup.ipynb")
        print("   • Check Cell 7 output for ngrok URLs")
        print("   • Update .env with current URLs")
        print("\n3. Test the connection:")
        print("   python test_all.py")
        print("\n" + "="*60)
        sys.exit(1)
    
    # Prepare tools
    tools = [
        get_time,
        duckduckgo_search_tool,
        take_screenshot,
        read_text_from_latest_image,
        arp_scan_terminal,
        matrix_mode,
    ]
    # File system operations
    tools.extend([
        create_file,
        fo_read_file,
        fo_write_file,
        fo_delete_path,
        fo_list_dir,
        fo_open_application,
    ])
    
    # Add vision tools if available
    if VISION_AVAILABLE:
        tools.extend([analyze_screen, analyze_camera, analyze_image])
        logging.info("[OK] Vision tools loaded (screen + camera + image)")
    else:
        logging.info("ℹ️ Vision tools not available")
    
    # Create agent prompt
    vision_instructions = ""
    if VISION_AVAILABLE:
        vision_instructions = """

VISION CAPABILITIES:
- analyze_screen: See what's on the user's screen
- analyze_camera: Capture from webcam to see what user is holding or showing
- analyze_image: Analyze image files
- When user asks "what am I holding" - use analyze_camera tool!
- When user asks "what's on my screen" - use analyze_screen tool!
- You CAN see - use the appropriate vision tool!"""
    
    # ReAct prompt template for models without native function calling
    react_prompt = """Answer the following question using this exact format:

Thought: I should use a tool to answer this
Action: tool_name
Action Input: input for tool
Observation: [result will appear here]
... (repeat Thought/Action/Observation as needed)
Thought: I now know the final answer
Final Answer: your response to the user

AVAILABLE TOOLS:
{tools}

TOOL NAMES: {tool_names}

CRITICAL RULES:
- "what am I holding?" → Action: analyze_camera, Action Input: What is the person holding?
- "what do you see?" → Action: analyze_camera, Action Input: What do you see?
- "what's on screen?" → Action: analyze_screen, Action Input: What's on the screen?
- ALWAYS use tools for visual questions!
- Keep Final Answer brief and natural

Question: {input}
{agent_scratchpad}"""
    
    from langchain.prompts import PromptTemplate
    prompt = PromptTemplate.from_template(react_prompt)
    
    # Create agent
    try:
        agent = create_react_agent(llm_module.llm, tools, prompt)
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=False,
            handle_parsing_errors=True,
            max_iterations=5,
            max_execution_time=120,
            return_intermediate_steps=False
        )
        logging.info("[OK] ReAct agent created successfully")
    except Exception as e:
        logging.error(f"Error creating agent: {e}")
        print("\n" + "="*60)
        print("[ERROR] ERROR: Could not create agent")
        print("="*60)
        print(f"\nError details: {e}")
        print("\n[Info] This usually means:")
        print("   • LLM connection is not working properly")
        print("   • The model doesn't support tool calling")
        print("\nPlease run: python test_all.py")
        print("="*60 + "\n")
        sys.exit(1)
    

    conversation_mode = False
    last_interaction_time = None
    
    print("\n" + "="*60)
    print(" JARVIS - Voice Input Mode")
    print("="*60)
    print("[Speaking] Testing local TTS...")
    speak_local("System ready")
    print("[Info] Say 'hello' or 'jarvis' to activate conversation mode")
    print("[Info] Press Ctrl+C to exit")
    print("[Info] In conversation mode, just speak your commands")
    print("="*60 + "\n")
    
    # Main interaction loop
    try:
        while True:
            try:
                # Listen for speech
                if conversation_mode:
                    print("[MIC] Listening...")
                    user_input = listen_for_speech(timeout=10)
                else:
                    print("[MIC] (Listening for activation...)")
                    user_input = listen_for_speech(timeout=5)
                
                if not user_input or user_input == "":
                    # Auto-deactivate after 30 seconds of silence
                    if conversation_mode and last_interaction_time:
                        if time.time() - last_interaction_time > 30:
                            print("💤 Conversation mode deactivated (timeout)")
                            conversation_mode = False
                    continue
                
                print(f"[You] You said: {user_input}")
                
                # Check for exit commands
                if any(word in user_input.lower() for word in ['exit', 'quit', 'goodbye', 'shut down']):
                    print(" Goodbye!")
                    speak_local("Goodbye sir")
                    break
                
                # Check for activation
                lower_input = user_input.lower()
                if not conversation_mode and any(word in lower_input for word in ['hello', 'hi', 'hey', 'jarvis']):
                    conversation_mode = True
                    last_interaction_time = time.time()
                    response = "Yes sir, how can I help you?"
                    print(f"[Jarvis] Jarvis: {response}")
                    speak_local(response)  # Use local TTS for quick greeting
                    continue
                
                # If not in conversation mode, just listen
                if not conversation_mode:
                    continue
                
                # Update last interaction time
                last_interaction_time = time.time()
                
                # Direct journal queries (project tracking) - Works offline!
                if JOURNAL_AVAILABLE:
                    # Check for "what day are we on" variations (very flexible)
                    if 'day' in lower_input and any(word in lower_input for word in ['are', 'is', 'we on', 'today']):
                        # But exclude "what did" queries
                        if 'did' not in lower_input and 'do' not in lower_input:
                            print("[Calendar] Checking project day...")
                            try:
                                result = get_project_day.invoke({})
                                print(f"[Jarvis] Jarvis: {result}")
                                speak_text(result)
                                continue
                            except Exception as e:
                                logging.error(f"Error getting project day: {e}")
                    
                    # Check for "what did we/you do today" variations (very flexible)
                    if 'did' in lower_input and 'today' in lower_input:
                        print("[Journal] Checking today's accomplishments...")
                        try:
                            result = get_today_summary.invoke({})
                            print(f"[Jarvis] Jarvis: {result}")
                            speak_text(result)
                            continue
                        except Exception as e:
                            logging.error(f"Error getting today summary: {e}")
                    
                    # Also catch "do today" variations
                    if 'do today' in lower_input or 'you today' in lower_input:
                        print("[Journal] Checking today's accomplishments...")
                        try:
                            result = get_today_summary.invoke({})
                            print(f"[Jarvis] Jarvis: {result}")
                            speak_text(result)
                            continue
                        except Exception as e:
                            logging.error(f"Error getting today summary: {e}")
                
                # Direct time queries - Works offline!
                time_keywords = ['what time', 'current time', 'time in', 'time is it']
                if any(keyword in lower_input for keyword in time_keywords):
                    print("[Time] Checking time...")
                    try:
                        city = "local"
                        if " in " in lower_input:
                            city = lower_input.split(" in ")[-1].strip("?.,!").title()
                        
                        result = get_time.invoke({"city": city})
                        print(f"[Jarvis] Jarvis: {result}")
                        speak_text(result)
                        continue
                    except Exception as e:
                        logging.error(f"Time query error: {e}")
                
                # Direct vision processing (bypass agent - BLIP-2 only!)
                vision_keywords = [
                    'what am i holding', 'what do you see', 'what are you seeing',
                    'look at me', 'analyze camera', 'use camera', 'take a look',
                    'what is this', 'describe what you see', 'what am i showing'
                ]
                
                if VISION_AVAILABLE and any(keyword in lower_input for keyword in vision_keywords):
                    print("[Camera] Capturing from camera...")
                    try:
                        result = analyze_camera.invoke({"question": user_input})
                        print(f"[Jarvis] Jarvis: {result}")
                        speak_text(result)
                        continue
                    except Exception as e:
                        logging.error(f"Vision error: {e}")
                        print(f"[Jarvis] Jarvis: Camera error: {e}")
                        speak_text("I couldn't access the camera.")
                        continue
                
                # Process query with agent (requires Colab)
                # Skip agent if it contains offline error indicators
                try:
                    logging.info(f"Processing: {user_input}")
                    
                    # Quick check if backend is likely offline
                    import requests
                    ollama_host = os.getenv("OLLAMA_HOST", "")
                    if ollama_host and "ngrok" in ollama_host:
                        try:
                            # Quick HEAD request with 2 second timeout
                            test_url = ollama_host.replace("/proxy_ollama", "/health")
                            requests.head(test_url, timeout=2, headers={"ngrok-skip-browser-warning": "true"})
                        except:
                            # Backend is offline, give quick response
                            response = "Backend is offline. Only local features available."
                            print(f"[Jarvis] Jarvis: {response}")
                            speak_text(response)
                            continue
                    
                    result = agent_executor.invoke({"input": user_input})
                    response = result.get("output", "I'm not sure how to help with that.")
                    
                    # Choose best sentence for TTS
                    tts_response = choose_best_sentence(response)
                    
                    print(f"[Jarvis] Jarvis: {response}")
                    speak_text(tts_response)  # Use Azure TTS for full responses
                    
                except Exception as e:
                    # Don't log full HTML errors
                    error_msg = str(e)
                    if "ngrok" in error_msg or "404" in error_msg:
                        response = "Backend offline. Use local commands."
                        logging.error("Backend connection failed")
                    else:
                        response = "I encountered an error."
                        logging.error(f"Agent error: {error_msg[:100]}")
                    
                    print(f"[Jarvis] Jarvis: {response}")
                    speak_text(response)
                    
            except KeyboardInterrupt:
                print("\n\n Goodbye!")
                speak_local("Goodbye sir")
                break
            except Exception as e:
                logging.error(f"Error in main loop: {e}")
                print(f"[ERROR] Error: {e}")
                continue
                
    except KeyboardInterrupt:
        print("\n\n Goodbye!")
        speak_local("Goodbye sir")


if __name__ == "__main__":
    main()
