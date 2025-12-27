# router.py

import numpy as np
from sentence_transformers import SentenceTransformer, util

# lightweight + fast
_model = SentenceTransformer("all-MiniLM-L6-v2")

INTENT_ANCHORS = {
    "ideas": [
        "suggest ideas",
        "give me ideas",
        "what can I build",
        "startup ideas",
        "tool ideas",
        "product ideas",
    ],
    "decision": [
        "should I build",
        "is it worth building",
        "should I do this",
        "pros and cons",
        "evaluate this idea",
        "is this a good idea",
    ],
}

# precompute anchor embeddings ONCE
ANCHOR_EMBEDDINGS = {
    intent: _model.encode(texts, normalize_embeddings=True)
    for intent, texts in INTENT_ANCHORS.items()
}


def embedding_route(user_input: str, threshold: float = 0.35) -> str:
    """
    Returns: 'ideas' | 'decision' | 'chat'
    """
    query_emb = _model.encode(user_input, normalize_embeddings=True)

    scores = {}
    for intent, emb in ANCHOR_EMBEDDINGS.items():
        sim = util.cos_sim(query_emb, emb).max().item()
        scores[intent] = sim

    best_intent = max(scores, key=scores.get)
    best_score = scores[best_intent]

    if best_score < threshold:
        return "chat"

    return best_intent
