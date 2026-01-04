# Polyreasoner

Polyreasoner is an idea evaluation and decision-support system that analyzes existing ideas from multiple independent perspectives.

Instead of generating new ideas or producing a single fluent answer, Polyreasoner evaluates an idea across perspectives such as security, risk, business value, feasibility, and long-term impact, then synthesizes trade-offs, disagreements, and confidence signals.

Polyreasoner does **not** make decisions for you.  
It helps you think better before making them.

## ℹ️ Note
This project explores system design and implementation patterns using AI-assisted development.
It prioritizes clarity of architecture and ideas over production guarantees.

---

## What Polyreasoner Is

- An **idea evaluator**
- A **multi-perspective reasoning system**
- A **realistic LLM application** designed for security testing
- A testbed for **PromptShield** (defense) and **Rapture** (red-team attacks)

## What Polyreasoner Is Not

- Not a chatbot  
- Not an idea generator  
- Not an auto yes/no decision engine  

---

## Architecture (V1)

- MainAgent (routing + orchestration)
- Perspective agents (security, risk, business, finance, etc.)
- Lightweight RAG (ideas / context)
- Deterministic synthesis (confidence + disagreement)
- Local-first LLM inference using `llama.cpp`

---

## Requirements

Python **3.10+** recommended.

Install dependencies:

```bash
pip install -r requirements.txt
```
Model Setup (Important)

Polyreasoner uses local GGUF models via llama-cpp-python.

1. Download a model (examples)

You can use any instruct-style GGUF model. Recommended options:

Qwen 2.5 1.5B Instruct (Q4)
https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF

Mistral 7B Instruct v0.2 (Q4)
https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF

Download a .gguf file, for example:

qwen2.5-1.5b-instruct-q4_k_m.gguf


or

mistral-7b-instruct-v0.2.Q4_K_M.gguf

2. Place the model in the project

Recommended structure:
```
polyreasoner/
│
├── app.py
├── llm.py
├── agents/
├── models/
│   ├── qwen2.5-1.5b-instruct-q4_k_m.gguf
│   # or
│   ├── mistral-7b-instruct-v0.2.Q4_K_M.gguf
```
3. Set the model path

Open llm.py and update the path:
```
MODEL_PATH = "polyreasoner/models/qwen2.5-1.5b-instruct-q4_k_m.gguf"

```
or
```
MODEL_PATH = "polyreasoner/models/mistral-7b-instruct-v0.2.Q4_K_M.gguf"
```

Only one model is loaded and shared across all agents.
```
Running Polyreasoner
python app.py
```


One-line summary
Polyreasoner evaluates ideas by reasoning across multiple perspectives instead of producing single, fluent answers.

