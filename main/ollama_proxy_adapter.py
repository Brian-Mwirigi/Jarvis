"""
Adapter to make Flask /proxy_ollama work with LangChain ChatOllama
"""
import requests
import json
from typing import Any, List, Optional, Dict
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage, SystemMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.callbacks import CallbackManagerForLLMRun
from pydantic import Field


class OllamaProxyAdapter(BaseChatModel):
    """
    Custom adapter for Flask /proxy_ollama endpoint that mimics ChatOllama API.
    This allows us to use a custom proxy endpoint with LangChain.
    """
    
    proxy_url: str = Field(...)
    model: str = Field(default="phi")
    temperature: float = Field(default=0.0)
    
    class Config:
        """Pydantic config."""
        arbitrary_types_allowed = True
    
    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        """Generate response from Ollama proxy."""
        
        # Convert LangChain messages to Ollama format
        ollama_messages = []
        for msg in messages:
            if isinstance(msg, HumanMessage):
                ollama_messages.append({"role": "user", "content": msg.content})
            elif isinstance(msg, AIMessage):
                ollama_messages.append({"role": "assistant", "content": msg.content})
            elif isinstance(msg, SystemMessage):
                ollama_messages.append({"role": "system", "content": msg.content})
        
        # Make request to proxy
        payload = {
            "model": self.model,
            "messages": ollama_messages,
            "stream": False,
            "options": {
                "temperature": self.temperature
            }
        }
        
        headers = {
            "ngrok-skip-browser-warning": "true",
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/json"
        }
        
        try:
            # Increase timeout for vision operations which take longer
            response = requests.post(
                self.proxy_url,
                json=payload,
                headers=headers,
                timeout=120  # 2 minutes for vision operations
            )
            
            if response.status_code != 200:
                raise Exception(f"Proxy returned {response.status_code}: {response.text}")
            
            # Parse response
            result = response.json()
            content = result.get("message", {}).get("content", "")
            
            # Create ChatResult
            message = AIMessage(content=content)
            generation = ChatGeneration(message=message)
            
            return ChatResult(generations=[generation])
            
        except Exception as e:
            raise Exception(f"Error calling Ollama proxy: {e}")
    
    @property
    def _llm_type(self) -> str:
        """Return type of llm."""
        return "ollama-proxy"
    
    def bind_tools(self, tools, **kwargs):
        """
        Bind tools to the model.
        Note: Tool calling through the proxy requires the Ollama model to support it.
        This is a pass-through implementation - the actual tool calling logic
        is handled by LangChain's agent framework using the model's responses.
        """
        # Store tools for potential future use
        if not hasattr(self, '_bound_tools'):
            self._bound_tools = []
        self._bound_tools.extend(tools)
        
        # Return a new instance of self (required for LangChain agents)
        return self.__class__(
            proxy_url=self.proxy_url,
            model=self.model,
            temperature=self.temperature
        )
    
    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """Get identifying parameters."""
        return {
            "model": self.model,
            "proxy_url": self.proxy_url,
            "temperature": self.temperature
        }
