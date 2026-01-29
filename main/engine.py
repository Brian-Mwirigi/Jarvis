import os
import logging
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from main.llm import init_llm, llm, ollama_client, OLLAMA_MODEL
from main.vision import VISION_AVAILABLE
from main.tts import speak_local
from main.utils import is_refusal, choose_best_sentence

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
except ImportError:
    pass

# Journal system
JOURNAL_AVAILABLE = False
try:
    from tools.journal import log_project_day, get_project_day, get_day_accomplishments, get_today_summary, get_project_summary
    JOURNAL_AVAILABLE = True
except ImportError:
    pass

# System control
SYSTEM_CONTROL_AVAILABLE = False
try:
    from tools.system_control import set_volume, lock_computer, shutdown_computer, cancel_shutdown, restart_computer
    SYSTEM_CONTROL_AVAILABLE = True
except ImportError:
    pass

# Clipboard
CLIPBOARD_AVAILABLE = False
try:
    from tools.clipboard import read_clipboard, write_clipboard, clear_clipboard
    CLIPBOARD_AVAILABLE = True
except ImportError:
    pass

# Weather
WEATHER_AVAILABLE = False
try:
    from tools.weather import get_weather, get_detailed_weather
    WEATHER_AVAILABLE = True
except ImportError:
    pass

# Reminders & Timers
REMINDERS_AVAILABLE = False
try:
    from tools.reminders import set_reminder, set_timer, quick_timer
    REMINDERS_AVAILABLE = True
except ImportError:
    pass

# YouTube
YOUTUBE_AVAILABLE = False
try:
    from tools.youtube import search_youtube, play_youtube, open_youtube_video, youtube_music
    YOUTUBE_AVAILABLE = True
except ImportError:
    pass

# Translation
TRANSLATE_AVAILABLE = False
try:
    from tools.translate import translate_text, detect_language
    TRANSLATE_AVAILABLE = True
except ImportError:
    pass

# Email
EMAIL_AVAILABLE = False
try:
    from tools.email_tool import send_email, read_latest_emails, check_unread_count
    EMAIL_AVAILABLE = True
except ImportError:
    pass

# Calendar
CALENDAR_AVAILABLE = False
try:
    from tools.calendar_tool import add_calendar_event, check_schedule, list_upcoming_events, delete_calendar_event
    CALENDAR_AVAILABLE = True
except ImportError:
    pass

# Music Control
MUSIC_AVAILABLE = False
try:
    from tools.music_control import play_spotify_song, control_music_playback, get_current_track, set_music_volume
    MUSIC_AVAILABLE = True
except ImportError:
    pass

# Code Execution
CODE_EXEC_AVAILABLE = False
try:
    from tools.code_exec import execute_python_code, calculate_expression, run_python_script, create_data_visualization
    CODE_EXEC_AVAILABLE = True
except ImportError:
    pass

# Document Analysis
DOCUMENT_ANALYSIS_AVAILABLE = False
try:
    from tools.document_analysis import read_pdf_document, read_word_document, read_text_document, analyze_document
    DOCUMENT_ANALYSIS_AVAILABLE = True
except ImportError:
    pass

# Vision
if VISION_AVAILABLE:
    from tools.vision import analyze_screen, analyze_image

class JarvisEngine:
    def __init__(self):
        self.agent_executor = None
        self.llm = None
        self.tools = []
        self.initialize()

    def initialize(self):
        # Initialize LLM
        init_llm()
        from main.llm import llm as initialized_llm
        self.llm = initialized_llm
        
        # Prepare tools
        self.tools = [
            get_time,
            duckduckgo_search_tool,
            take_screenshot,
            read_text_from_latest_image,
            arp_scan_terminal,
        ]
        
        self.tools.extend([
            create_file,
            fo_read_file,
            fo_write_file,
            fo_delete_path,
            fo_list_dir,
            fo_open_application,
        ])
        
        if MEMORY_AVAILABLE:
            self.tools.extend([remember_fact, recall_memory, store_conversation, get_conversation_context])
        
        if JOURNAL_AVAILABLE:
            self.tools.extend([log_project_day, get_project_day, get_day_accomplishments, get_today_summary, get_project_summary])
            
        if VISION_AVAILABLE:
            self.tools.extend([analyze_screen, analyze_image])
            
        if SYSTEM_CONTROL_AVAILABLE:
            self.tools.extend([set_volume, lock_computer, shutdown_computer, cancel_shutdown, restart_computer])
            
        if CLIPBOARD_AVAILABLE:
            self.tools.extend([read_clipboard, write_clipboard, clear_clipboard])
            
        if WEATHER_AVAILABLE:
            self.tools.extend([get_weather, get_detailed_weather])
            
        if REMINDERS_AVAILABLE:
            self.tools.extend([set_reminder, set_timer, quick_timer])
            
        if YOUTUBE_AVAILABLE:
            self.tools.extend([search_youtube, play_youtube, open_youtube_video, youtube_music])
            
        if TRANSLATE_AVAILABLE:
            self.tools.extend([translate_text, detect_language])
            
        if EMAIL_AVAILABLE:
            self.tools.extend([send_email, read_latest_emails, check_unread_count])
            
        if CALENDAR_AVAILABLE:
            self.tools.extend([add_calendar_event, check_schedule, list_upcoming_events, delete_calendar_event])
            
        if MUSIC_AVAILABLE:
            self.tools.extend([play_spotify_song, control_music_playback, get_current_track, set_music_volume])
            
        if CODE_EXEC_AVAILABLE:
            self.tools.extend([execute_python_code, calculate_expression, run_python_script, create_data_visualization])
            
        if DOCUMENT_ANALYSIS_AVAILABLE:
            self.tools.extend([read_pdf_document, read_word_document, read_text_document, analyze_document])

        # Create agent
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are Jarvis, a helpful AI assistant. You have access to various tools to help users.
            
When the user greets you (hello, hi, hey, jarvis), respond briefly and warmly.
Always be concise and helpful. Use tools when needed to answer questions accurately.
If you need to search the web, take screenshots, or check time zones, use the appropriate tools.

Important: Keep responses conversational and natural."""),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ])

        try:
            if self.llm:
                # Check if using phi model (fast but simple)
                model_name = os.getenv('OLLAMA_MODEL', 'phi')
                use_simple_mode = 'phi' in model_name.lower()
                
                if use_simple_mode:
                    self.agent_executor = None
                elif not hasattr(self.llm, 'bind_tools') or 'OllamaProxyAdapter' in str(type(self.llm)):
                    from langchain.agents import create_react_agent, AgentExecutor as ReactAgentExecutor
                    from langchain import hub
                    react_prompt = hub.pull("hwchase17/react")
                    agent = create_react_agent(self.llm, self.tools, react_prompt)
                    self.agent_executor = ReactAgentExecutor(
                        agent=agent,
                        tools=self.tools,
                        verbose=True,
                        handle_parsing_errors=True,
                        max_iterations=15
                    )
                else:
                    agent = create_tool_calling_agent(self.llm, self.tools, prompt)
                    self.agent_executor = AgentExecutor(
                        agent=agent,
                        tools=self.tools,
                        verbose=True,
                        handle_parsing_errors=True,
                        max_iterations=15
                    )
        except Exception as e:
            logging.error(f"Could not create agent: {e}")
            self.agent_executor = None

    def process_message(self, message: str) -> str:
        if not message:
            return ""
            
        # Basic greetings
        lower_input = message.lower()
        if any(word in lower_input for word in ['hello', 'hi', 'hey', 'jarvis']) and len(message.split()) < 5:
            return "Yes sir, how can I help you?"

        if self.agent_executor:
            try:
                result = self.agent_executor.invoke({"input": message})
                if isinstance(result, dict):
                    return result.get('output') or result.get('result') or str(result)
                return str(result)
            except Exception as e:
                logging.error(f"Agent error: {e}")
                return f"I encountered an error: {str(e)}"
        elif self.llm:
            # Simple mode
            try:
                from langchain_core.messages import HumanMessage, SystemMessage
                messages = [
                    SystemMessage(content="You are Jarvis, a helpful AI assistant. Answer concisely in 1-2 sentences."),
                    HumanMessage(content=message)
                ]
                result = self.llm.invoke(messages)
                return result.content if hasattr(result, 'content') else str(result)
            except Exception as e:
                return f"Error: {str(e)}"
        else:
            return "I am currently offline or unable to access my brain."
