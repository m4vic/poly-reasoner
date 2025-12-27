from llama_cpp import Llama

MODEL_PATH = r"paste the model path here"
_llm = None


def get_llm():
    global _llm
    if _llm is None:
        print("🔵 Loading model once...")
        _llm = Llama(
            model_path=MODEL_PATH,
            n_ctx=4096,
            n_threads=8,
            n_batch=1024,
            n_gpu_layers=35,
            verbose=False,
        )
        print("✅ Model loaded")
    return _llm

