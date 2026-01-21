
import os
import time
from langchain_community.llms import Ollama

class JarvisLLM:
    def __init__(self):
        # Default to 'llama3', but allow env override
        self.model_name = os.getenv("OLLAMA_MODEL", "llama3")
        self.use_local_llm = False
        
        try:
            base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            print(f"Initializing Ollama with model: {self.model_name} at {base_url}...")
            self.llm = Ollama(model=self.model_name, base_url=base_url)
            # Simple check to see if we can reach the server (optional, but good for debugging)
            # self.llm.invoke("Hi") 
            self.use_local_llm = True
            print("Ollama initialized successfully!")
        except Exception as e:
            print(f"Failed to connect to Ollama: {e}")
            self.use_local_llm = False
        
    def generate_response(self, query, context=""):
        if self.use_local_llm:
            try:
                prompt = f"Context: {context}\nUser: {query}\nAssistant:"
                return self.llm.invoke(prompt)
            except Exception as e:
                return f"Error communicating with Ollama: {e}. Is it running?"
        else:
            # Mock behavior fallback
            time.sleep(1) 
            return f"Thinking... (Mock Mode - Ollama failed to connect)\n\nI heard you say: '{query}'.\n\nContext used: {context}"
