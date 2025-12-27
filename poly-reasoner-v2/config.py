# Model configuration
MODEL_PATH = r"E:\SecurePrompt\models\mistral-7b-instruct-v0.2.Q4_K_M.gguf"
MODEL_CONFIG = {
    "n_ctx": 4096,
    "n_threads": 6,
    "n_batch": 512,
    "n_gpu_layers": 35,
}

# Agent expertise definitions
AGENT_PROFILES = {
    "security": "cybersecurity risks, vulnerabilities, threat modeling, data protection, compliance requirements",
    "risk": "operational risks, failure modes, mitigation strategies, contingency planning, risk-reward analysis",
    "business": "market viability, competitive positioning, scalability, business model, customer acquisition",
    "finance": "cost structure, revenue potential, ROI, funding requirements, financial sustainability",
    "longterm": "strategic vision, future-proofing, sustainability, evolution roadmap, technical debt prevention",
    "shortterm": "immediate execution, MVP feasibility, quick wins, resource efficiency, time-to-market",
}

# Dynamic weight rules (keyword → weight distribution)
WEIGHT_RULES = [
    {
        "keywords": ["security", "attack", "breach", "vulnerability", "exploit"],
        "weights": {"security": 0.40, "risk": 0.30, "business": 0.15, "finance": 0.05, "longterm": 0.05, "shortterm": 0.05}
    },
    {
        "keywords": ["startup", "saas", "product", "market"],
        "weights": {"business": 0.35, "finance": 0.25, "risk": 0.20, "longterm": 0.15, "shortterm": 0.05, "security": 0.00}
    },
    {
        "keywords": ["quick", "mvp", "fast", "immediate", "urgent"],
        "weights": {"shortterm": 0.40, "risk": 0.25, "business": 0.20, "longterm": 0.10, "security": 0.05, "finance": 0.00}
    },
    {
        "keywords": ["cost", "budget", "price", "funding", "investment"],
        "weights": {"finance": 0.40, "business": 0.25, "risk": 0.20, "longterm": 0.10, "shortterm": 0.05, "security": 0.00}
    },
]

# Routing thresholds
RELEVANCE_THRESHOLD = 0.4  # Min score to activate an agent
COMPLEXITY_THRESHOLD = 5   # Word count below = simple chat
CONFIDENCE_THRESHOLD = 0.7  # Min confidence to show result