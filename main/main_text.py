"""
Jarvis Text Input Mode - Complete Implementation
"""
import sys
import os
import logging
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from main.llm import init_llm, llm, ollama_client, OLLAMA_MODEL
from main.vision import VISION_AVAILABLE, vision
from main.tts import speak_local, speak_text
from main.utils import choose_best_sentence, is_refusal

# Import tools
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
MEMORY_AVAILABLE = False
try:
    from tools.memory import remember_fact, recall_memory, store_conversation, get_conversation_context, MEMORY_AVAILABLE
except ImportError as e:
    logging.warning(f"⚠️ Memory tools not available: {e}")
except Exception as e:
    logging.warning(f"⚠️ Memory tools error: {e}")

# Journal system
JOURNAL_AVAILABLE = False
try:
    from tools.journal import log_project_day, get_project_day, get_day_accomplishments, get_today_summary, get_project_summary
    JOURNAL_AVAILABLE = True
except ImportError as e:
    logging.warning(f"⚠️ Journal tools not available: {e}")
except Exception as e:
    logging.warning(f"⚠️ Journal tools error: {e}")

# System control
try:
    from tools.system_control import set_volume, lock_computer, shutdown_computer, cancel_shutdown, restart_computer
    SYSTEM_CONTROL_AVAILABLE = True
except ImportError:
    SYSTEM_CONTROL_AVAILABLE = False
    logging.warning("⚠️ System control tools not available")

# Clipboard
try:
    from tools.clipboard import read_clipboard, write_clipboard, clear_clipboard
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False
    logging.warning("⚠️ Clipboard tools not available (install pyperclip)")

# Weather
try:
    from tools.weather import get_weather, get_detailed_weather
    WEATHER_AVAILABLE = True
except ImportError:
    WEATHER_AVAILABLE = False
    logging.warning("⚠️ Weather tools not available")

# Reminders & Timers
try:
    from tools.reminders import set_reminder, set_timer, quick_timer
    REMINDERS_AVAILABLE = True
except ImportError:
    REMINDERS_AVAILABLE = False
    logging.warning("⚠️ Reminder tools not available")

# YouTube
try:
    from tools.youtube import search_youtube, play_youtube, open_youtube_video, youtube_music
    YOUTUBE_AVAILABLE = True
except ImportError:
    YOUTUBE_AVAILABLE = False
    logging.warning("⚠️ YouTube tools not available")

# Translation
try:
    from tools.translate import translate_text, detect_language
    TRANSLATE_AVAILABLE = True
except ImportError:
    TRANSLATE_AVAILABLE = False
    logging.warning("⚠️ Translation tools not available (install deep-translator langdetect)")

# Email
try:
    from tools.email_tool import send_email, read_latest_emails, check_unread_count
    EMAIL_AVAILABLE = True
except ImportError:
    EMAIL_AVAILABLE = False
    logging.warning("⚠️ Email tools not available")

# Calendar
try:
    from tools.calendar_tool import add_calendar_event, check_schedule, list_upcoming_events, delete_calendar_event
    CALENDAR_AVAILABLE = True
except ImportError:
    CALENDAR_AVAILABLE = False
    logging.warning("⚠️ Calendar tools not available")

# Music Control
try:
    from tools.music_control import play_spotify_song, control_music_playback, get_current_track, set_music_volume
    MUSIC_AVAILABLE = True
except ImportError:
    MUSIC_AVAILABLE = False
    logging.warning("⚠️ Music control tools not available")

# Code Execution
try:
    from tools.code_exec import execute_python_code, calculate_expression, run_python_script, create_data_visualization
    CODE_EXEC_AVAILABLE = True
except ImportError:
    CODE_EXEC_AVAILABLE = False
    logging.warning("⚠️ Code execution tools not available")

# Document Analysis
try:
    from tools.document_analysis import read_pdf_document, read_word_document, read_text_document, analyze_document
    DOCUMENT_ANALYSIS_AVAILABLE = True
except ImportError:
    DOCUMENT_ANALYSIS_AVAILABLE = False
    logging.warning("⚠️ Document analysis tools not available (install PyPDF2 python-docx)")

# Conditionally import vision tools
if VISION_AVAILABLE:
    from tools.vision import analyze_screen, analyze_image

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def main_text():
    """Text-based interaction loop"""
    
    # Set UTF-8 encoding for Windows console
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except:
            pass
    
    # Initialize LLM
    init_llm()
    
    # Re-import llm after initialization to get the updated global variable
    from main.llm import llm
    logging.info(f"🔧 LLM after init: {llm}")
    logging.info(f"🔧 LLM type: {type(llm)}")
    
    # Prepare tools
    tools = [
        get_time,
        duckduckgo_search_tool,
        take_screenshot,
        read_text_from_latest_image,
        arp_scan_terminal,
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
    
    # Add memory tools if available
    if MEMORY_AVAILABLE:
        tools.extend([remember_fact, recall_memory, store_conversation, get_conversation_context])
        logging.info("✅ Memory tools loaded")
    else:
        logging.info("ℹ️ Memory tools not available")
    
    # Add journal tools if available
    if JOURNAL_AVAILABLE:
        tools.extend([log_project_day, get_project_day, get_day_accomplishments, get_today_summary, get_project_summary])
        logging.info("✅ Journal tools loaded")
    else:
        logging.info("ℹ️ Journal tools not available")
    
    # Add vision tools if available
    if VISION_AVAILABLE:
        tools.extend([analyze_screen, analyze_image])
        logging.info("✅ Vision tools loaded")
    else:
        logging.info("ℹ️ Vision tools not available")
    
    # Add system control tools
    if SYSTEM_CONTROL_AVAILABLE:
        tools.extend([set_volume, lock_computer, shutdown_computer, cancel_shutdown, restart_computer])
        logging.info("✅ System control tools loaded")
    
    # Add clipboard tools
    if CLIPBOARD_AVAILABLE:
        tools.extend([read_clipboard, write_clipboard, clear_clipboard])
        logging.info("✅ Clipboard tools loaded")
    
    # Add weather tools
    if WEATHER_AVAILABLE:
        tools.extend([get_weather, get_detailed_weather])
        logging.info("✅ Weather tools loaded")
    
    # Add reminder tools
    if REMINDERS_AVAILABLE:
        tools.extend([set_reminder, set_timer, quick_timer])
        logging.info("✅ Reminder tools loaded")
    
    # Add YouTube tools
    if YOUTUBE_AVAILABLE:
        tools.extend([search_youtube, play_youtube, open_youtube_video, youtube_music])
        logging.info("✅ YouTube tools loaded")
    
    # Add translation tools
    if TRANSLATE_AVAILABLE:
        tools.extend([translate_text, detect_language])
        logging.info("✅ Translation tools loaded")
    
    # Add email tools
    if EMAIL_AVAILABLE:
        tools.extend([send_email, read_latest_emails, check_unread_count])
        logging.info("✅ Email tools loaded")
    
    # Add calendar tools
    if CALENDAR_AVAILABLE:
        tools.extend([add_calendar_event, check_schedule, list_upcoming_events, delete_calendar_event])
        logging.info("✅ Calendar tools loaded")
    
    # Add music control tools
    if MUSIC_AVAILABLE:
        tools.extend([play_spotify_song, control_music_playback, get_current_track, set_music_volume])
        logging.info("✅ Music control tools loaded")
    
    # Add code execution tools
    if CODE_EXEC_AVAILABLE:
        tools.extend([execute_python_code, calculate_expression, run_python_script, create_data_visualization])
        logging.info("✅ Code execution tools loaded")
    
    # Add document analysis tools
    if DOCUMENT_ANALYSIS_AVAILABLE:
        tools.extend([read_pdf_document, read_word_document, read_text_document, analyze_document])
        logging.info("✅ Document analysis tools loaded")
    
    # Create agent prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are Jarvis, a helpful AI assistant. You have access to various tools to help users.
        
When the user greets you (hello, hi, hey, jarvis), respond briefly and warmly.
Always be concise and helpful. Use tools when needed to answer questions accurately.
If you need to search the web, take screenshots, or check time zones, use the appropriate tools.

Important: Keep responses conversational and natural."""),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])
    
    # Create agent
    try:
        logging.info(f"🔧 Creating agent with LLM: {llm}")
        logging.info(f"🔧 LLM type: {type(llm)}")
        logging.info(f"🔧 Has bind_tools: {hasattr(llm, 'bind_tools')}")
        
        # Check if using phi model (fast but simple)
        model_name = os.getenv('OLLAMA_MODEL', 'phi')
        use_simple_mode = 'phi' in model_name.lower()
        
        if use_simple_mode:
            logging.info("🔧 Using SIMPLE mode for phi (fast responses, limited tool use)")
            # For phi, we'll skip the complex agent and use direct LLM calls
            agent_executor = None  # Will handle manually in the loop
        elif not hasattr(llm, 'bind_tools') or 'OllamaProxyAdapter' in str(type(llm)):
            logging.info("🔧 Using ReAct agent (bind_tools not available)")
            from langchain.agents import create_react_agent, AgentExecutor as ReactAgentExecutor
            from langchain import hub
            
            # Get ReAct prompt
            react_prompt = hub.pull("hwchase17/react")
            agent = create_react_agent(llm, tools, react_prompt)
            agent_executor = ReactAgentExecutor(
                agent=agent,
                tools=tools,
                verbose=True,
                handle_parsing_errors=True,
                max_iterations=15
            )
        else:
            # Use tool calling agent for modern LLMs
            agent = create_tool_calling_agent(llm, tools, prompt)
            agent_executor = AgentExecutor(
                agent=agent,
                tools=tools,
                verbose=True,
                handle_parsing_errors=True,
                max_iterations=15
            )
        
        logging.info("✅ Agent created successfully")
    except Exception as e:
        logging.error(f"❌ Could not create agent: {e}")
        import traceback
        logging.error(traceback.format_exc())
        logging.error(f"❌ Could not create agent: {e}")
        logging.info("ℹ️ Running in OFFLINE MODE - limited features available")
        agent_executor = None
    
    # Print header
    print("\n" + "="*60)
    print("🧠 JARVIS - Text Input Mode")
    print("="*60)
    if agent_executor:
        print("✅ Full mode - All features available")
    else:
        print("⚠️  OFFLINE MODE - LLM unavailable (Colab down)")
        offline_features = ["time", "screenshot", "read screen", "matrix", "network scan"]
        if MEMORY_AVAILABLE:
            offline_features.append("memory")
        if JOURNAL_AVAILABLE:
            offline_features.append("journal")
        print(f"📋 Available: {', '.join(offline_features)}")
    print("\n💡 Type 'hello' or 'jarvis' to start")
    print("💡 Type 'help' for available commands")
    print("💡 Type 'exit' or 'quit' to exit")
    print("💡 Press Ctrl+C to force quit")
    print("="*60 + "\n")

    # Main interaction loop - always accept text input in this mode
    try:
        while True:
            try:
                # Prompt the user for input (always accept text input in this mode)
                user_input = input("💬 You: ").strip()

            except EOFError:
                # If input stream is closed, wait briefly and continue
                logging.info("EOF on input stream; retrying...")
                print("(No input received. Type 'exit' to quit.)")
                continue
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                try:
                    speak_local("Goodbye sir")
                except Exception:
                    pass
                break

            # Skip empty input
            if not user_input:
                continue

            # Check for exit commands
            if user_input.lower() in ['exit', 'quit', 'bye', 'goodbye']:
                print("👋 Goodbye!")
                try:
                    speak_local("Goodbye sir")
                except Exception:
                    pass
                break

            # Activation greeting (optional) - respond and continue
            lower_input = user_input.lower()
            if any(word in lower_input for word in ['hello', 'hi', 'hey', 'jarvis']):
                response = "Yes sir, how can I help you?"
                print(f"🤖 Jarvis: {response}")
                try:
                    speak_local(response)
                except Exception:
                    pass
                continue

            # Process query with agent if available
            if agent_executor:
                try:
                    logging.info(f"Processing: {user_input}")
                    # Use invoke method (modern LangChain API)
                    result = agent_executor.invoke({"input": user_input})
                    
                    # Extract response from result dictionary
                    if isinstance(result, dict):
                        response = result.get('output') or result.get('result') or str(result)
                    else:
                        response = str(result)
                    
                    if not response:
                        response = "I processed your request but didn't generate a response."
                except Exception as e:
                    logging.error(f"Agent error: {e}")
                    import traceback
                    logging.error(traceback.format_exc())
                    response = "I encountered an error processing that request."
            else:
                # Simple mode - direct LLM call (fast, for phi)
                try:
                    from langchain_core.messages import HumanMessage, SystemMessage
                    messages = [
                        SystemMessage(content="You are Jarvis, a helpful AI assistant. Answer concisely in 1-2 sentences."),
                        HumanMessage(content=user_input)
                    ]
                    result = llm.invoke(messages)
                    response = result.content if hasattr(result, 'content') else str(result)
                except Exception as e:
                    logging.error(f"LLM error: {e}")
                    response = "I encountered an error processing that request."
            
            # Display and speak response
            if response:
                print(f"🤖 Jarvis: {response}")
                
                # Choose best sentence for TTS
                tts_response = choose_best_sentence(response)
                try:
                    speak_local(tts_response)
                except Exception:
                    # If TTS fails, still continue
                    logging.debug("TTS failed for response")
            else:
                # Offline mode - handle specific queries without LLM
                lower_input = user_input.lower()
                
                # Memory commands (offline) - Check FIRST
                if MEMORY_AVAILABLE:
                    if "remember" in lower_input:
                        try:
                            # Extract what to remember (everything after "remember")
                            fact = user_input.split("remember", 1)[1].strip()
                            if fact:
                                response = remember_fact.invoke({"fact": fact, "category": "general"})
                                print(f"🤖 Jarvis: {response}")
                                speak_local("Memory stored sir")
                                continue
                        except Exception as e:
                            logging.error(f"Memory error: {e}")
                    
                    elif ("recall" in lower_input or "do you remember" in lower_input or "what do you know about" in lower_input):
                        try:
                            # Extract query
                            if "recall" in lower_input:
                                query = user_input.split("recall", 1)[1].strip()
                            elif "do you remember" in lower_input:
                                query = user_input.split("do you remember", 1)[1].strip()
                            else:
                                query = user_input.split("what do you know about", 1)[1].strip()
                            
                            if query:
                                response = recall_memory.invoke({"query": query})
                                print(f"🤖 Jarvis: {response}")
                                speak_text(response)
                                continue
                        except Exception as e:
                            logging.error(f"Recall error: {e}")
                
                # Journal commands (offline)
                if JOURNAL_AVAILABLE:
                    if "what day" in lower_input and ("are we" in lower_input or "is it" in lower_input):
                        try:
                            response = get_project_day.invoke({})
                            print(f"🤖 Jarvis: {response}")
                            speak_text(response)
                            continue
                        except Exception as e:
                            logging.error(f"Journal error: {e}")
                    
                    elif "today" in lower_input and ("what did" in lower_input or "summary" in lower_input):
                        try:
                            response = get_today_summary.invoke({})
                            print(f"🤖 Jarvis: {response}")
                            speak_text(response)
                            continue
                        except Exception as e:
                            logging.error(f"Journal error: {e}")
                
                # Time queries (offline)
                if "time" in lower_input:
                    try:
                        if " in " in lower_input:
                            city = lower_input.split(" in ")[-1].strip("?.,!").title()
                            response = get_time.invoke({"city": city})
                        else:
                            response = get_time.invoke({"city": "local"})
                        print(f"🤖 Jarvis: {response}")
                        speak_text(response)
                        continue
                    except Exception as e:
                        logging.error(f"Time query error: {e}")
                
                # OCR (offline) - Check BEFORE screenshot since it contains "screenshot"
                elif ("read" in lower_input or "extract" in lower_input or "ocr" in lower_input) and ("screen" in lower_input or "text" in lower_input or "image" in lower_input):
                    try:
                        response = read_text_from_latest_image.invoke({})
                        print(f"🤖 Jarvis: {response}")
                        if len(response) < 200:
                            speak_text(response)
                        else:
                            speak_local("Text extracted sir")
                        continue
                    except Exception as e:
                        logging.error(f"OCR error: {e}")
                
                # Screenshot (offline)
                elif "screenshot" in lower_input or ("capture" in lower_input and "screen" in lower_input):
                    try:
                        response = take_screenshot.invoke({})
                        print(f"🤖 Jarvis: {response}")
                        speak_local("Screenshot captured sir")
                        continue
                    except Exception as e:
                        logging.error(f"Screenshot error: {e}")
                
                # Matrix mode (offline)
                elif "matrix" in lower_input:
                    try:
                        response = matrix_mode.invoke({})
                        print(f"🤖 Jarvis: {response}")
                        speak_local("Matrix mode activated")
                        continue
                    except Exception as e:
                        logging.error(f"Matrix error: {e}")
                
                # Network scan (offline)
                elif "network" in lower_input or "arp" in lower_input or ("scan" in lower_input and "network" not in lower_input):
                    try:
                        response = arp_scan_terminal.invoke({})
                        print(f"🤖 Jarvis: {response}")
                        speak_local("Network scan complete")
                        continue
                    except Exception as e:
                        logging.error(f"Network scan error: {e}")
                
                # Help command
                elif "help" in lower_input or "commands" in lower_input:
                    help_text = """Offline commands available:
• "time" or "time in [city]" - Get current time
• "screenshot" - Capture screen
• "read screen" or "read text" - OCR from latest screenshot
• "matrix" - Matrix mode effect
• "network scan" - Show network devices"""
                    
                    if MEMORY_AVAILABLE:
                        help_text += "\n• \"remember [fact]\" - Store memory"
                        help_text += "\n• \"recall [query]\" - Retrieve memory"
                    
                    if JOURNAL_AVAILABLE:
                        help_text += "\n• \"what day are we on\" - Project day"
                        help_text += "\n• \"what did we do today\" - Today's summary"
                    
                    help_text += "\n• Start Colab for full LLM features"
                    
                    print(f"🤖 Jarvis: {help_text}")
                    speak_local("Showing available commands")
                    continue
                
                # Default - explain offline mode
                response = "LLM backend unavailable. Offline commands available: time, screenshot, read screen, matrix, network scan. Or start Colab for full features."
                print(f"🤖 Jarvis: {response}")
                try:
                    speak_local("LLM backend unavailable")
                except Exception:
                    pass

    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        try:
            speak_local("Goodbye sir")
        except Exception:
            pass


if __name__ == "__main__":
    main_text()
