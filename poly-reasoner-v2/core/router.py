from typing import Dict
from config import RELEVANCE_THRESHOLD

class Router:
    """Simple keyword-based router"""
    
    def select_agents(self, user_input: str) -> Dict[str, float]:
        """Select relevant agents using keywords"""
        text = user_input.lower()
        scores = {
            "security": 0.0,
            "risk": 0.0,
            "business": 0.0,
            "finance": 0.0,
            "longterm": 0.0,
            "shortterm": 0.0
        }
        
        # Security keywords
        if any(w in text for w in ["security", "hack", "breach", "attack", "privacy", "compliance", "vulnerability"]):
            scores["security"] = 0.9
            scores["risk"] = 0.7
        
        # Business/Product keywords
        if any(w in text for w in ["business", "startup", "saas", "product", "market", "customer", "idea", "project"]):
            scores["business"] = 0.9
            scores["finance"] = 0.6
            scores["shortterm"] = 0.6
        
        # Finance keywords
        if any(w in text for w in ["cost", "price", "funding", "revenue", "investment", "budget", "money", "roi"]):
            scores["finance"] = 0.9
            scores["business"] = 0.7
        
        # Risk keywords
        if any(w in text for w in ["risk", "danger", "problem", "issue", "concern", "threat"]):
            scores["risk"] = 0.9
            scores["security"] = 0.6
        
        # Time-based keywords
        if any(w in text for w in ["quick", "fast", "mvp", "immediate", "now", "short"]):
            scores["shortterm"] = 0.9
        if any(w in text for w in ["future", "longterm", "long-term", "sustainable", "scale", "growth"]):
            scores["longterm"] = 0.9
        
        # If no keywords matched, activate business + shortterm (default for ideas)
        if max(scores.values()) == 0.0:
            scores["business"] = 0.7
            scores["shortterm"] = 0.6
        
        # Filter by threshold
        return {k: v for k, v in scores.items() if v >= RELEVANCE_THRESHOLD}