from llama_cpp import Llama
from config import MODEL_PATH, MODEL_CONFIG

class LLMWrapper:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        print("🔵 Loading model...")
        self.llm = Llama(model_path=MODEL_PATH, verbose=False, **MODEL_CONFIG)
        self._initialized = True
        print("✅ Model ready")
    
    def generate(self, prompt: str, max_tokens=256, temperature=0.3, stop=None):
        """Generate completion"""
        response = self.llm(
            prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            stop=stop or [],
        )
        return response["choices"][0]["text"].strip()

# Global accessor
def get_llm():
    return LLMWrapper()