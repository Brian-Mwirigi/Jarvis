import os
import logging
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from ollama import Client as OllamaClient

# Load environment variables from .env file
load_dotenv()

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")  # Optional; do not require
# Support both OLLAMA_URL and OLLAMA_HOST for endpoint
OLLAMA_HOST = os.getenv("OLLAMA_URL") or os.getenv("OLLAMA_HOST") or "http://localhost:11434"
PROXY_OLLAMA = "/proxy_ollama" in OLLAMA_HOST

llm = None
ollama_client = None

# Import custom adapter for proxy_ollama
try:
    from main.ollama_proxy_adapter import OllamaProxyAdapter
    ADAPTER_AVAILABLE = True
except ImportError:
    ADAPTER_AVAILABLE = False
    logging.warning("[Warning] OllamaProxyAdapter not available")

def init_llm():
    global llm, ollama_client
    
    # ChatOllama requires standard Ollama API endpoints (/api/chat, /api/generate, etc.)
    # Your Colab has TWO ngrok tunnels:
    # 1. Direct Ollama tunnel (port 11434) - standard Ollama API
    # 2. Flask tunnel with /proxy_ollama - custom proxy
    
    # For ChatOllama, we should use the direct Ollama tunnel
    # Check if user provided the direct Ollama URL or the Flask proxy URL
    
    if PROXY_OLLAMA:
        # User provided Flask proxy URL - use custom adapter
        logging.info("🔧 Detected /proxy_ollama endpoint, using custom adapter")
        
        if ADAPTER_AVAILABLE:
            try:
                model_name = OLLAMA_MODEL or "phi"
                llm = OllamaProxyAdapter(
                    proxy_url=OLLAMA_HOST,
                    model=model_name,
                    temperature=0.0
                )
                logging.info(f"✅ [OK] Proxy adapter initialized ({model_name}) at {OLLAMA_HOST}")
                
                # Test bind_tools
                test_bound = llm.bind_tools([])
                logging.info(f"✅ [OK] bind_tools() test passed: {test_bound is not None}")
                
            except Exception as e:
                llm = None
                logging.error(f"❌ [ERROR] Failed to initialize proxy adapter: {e}")
                import traceback
                logging.error(traceback.format_exc())
        else:
            logging.error("❌ [ERROR] OllamaProxyAdapter not available")
            llm = None
    else:
        # Direct Ollama connection - should work
        try:
            model_name = OLLAMA_MODEL or "phi"
            
            # Configure client with ngrok bypass headers
            client_config = {
                "headers": {
                    "ngrok-skip-browser-warning": "true",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                }
            }
            
            # Add headers to bypass ngrok warning page
            llm = ChatOllama(
                model=model_name,
                temperature=0.0,
                base_url=OLLAMA_HOST,
                client_kwargs=client_config,
                sync_client_kwargs=client_config,
                async_client_kwargs=client_config
            )
            
            logging.info(f"[OK] LLM initialized ({model_name}) at {OLLAMA_HOST}")
        except Exception as e:
            llm = None
            logging.error(f"[ERROR] Failed to initialize ChatOllama: {e}")
    
    # Initialize Ollama HTTP client
    try:
        default_ollama_headers = {
            "ngrok-skip-browser-warning": "true",
            "User-Agent": "Mozilla/5.0",
        }
        ollama_client = OllamaClient(host=OLLAMA_HOST, headers=default_ollama_headers)
        logging.info("[OK] Ollama HTTP client initialized")
    except Exception as e:
        ollama_client = None
        logging.warning(f"[Warning] Could not initialize Ollama client: {e}")
    
    return llm, ollama_client
