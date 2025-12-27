# rag.py

IDEAS = [
    {"id": 1, "text": "Prompt injection testing CLI tool", "tag": "security"},
    {"id": 2, "text": "LLM firewall for enterprise apps", "tag": "security"},
    {"id": 3, "text": "AI red-team simulation framework", "tag": "security"},
    {"id": 4, "text": "Startup idea validation tool", "tag": "business"},
    {"id": 5, "text": "Cost estimation engine for SaaS", "tag": "finance"},
]


def retrieve_ideas(query: str, limit: int = 3):
    q = query.lower()
    results = []

    for idea in IDEAS:
        if any(word in idea["text"].lower() for word in q.split()):
            results.append(idea)

    return results[:limit]
