# app.py

import json
from typing import Dict, List

from agents.main_agent import MainAgent
from agents.security_agent import SecurityAgent
from agents.risk_agent import RiskAgent
from agents.business_agent import BusinessAgent
from agents.finance_agent import FinanceAgent
from agents.longterm_agent import LongTermAgent
from agents.shortterm_agent import ShortTermAgent

from rag import retrieve_ideas
from synthesis import synthesize
from router import embedding_route


# -----------------------------
# Agent registry
# -----------------------------
AGENTS = {
    "security": SecurityAgent(),
    "risk": RiskAgent(),
    "business": BusinessAgent(),
    "finance": FinanceAgent(),
    "longterm": LongTermAgent(),
    "shortterm": ShortTermAgent(),
}


# -----------------------------
# Hard rule routing (always first)
# -----------------------------
def rule_route(text: str):
    t = text.lower().strip()

    if t in ["hi", "hello", "hey"]:
        return "chat"

    if len(t.split()) <= 3:
        return "chat"

    return None


# -----------------------------
# Dynamic weighting
# -----------------------------
def get_dynamic_weights(user_input: str) -> Dict[str, float]:
    text = user_input.lower()

    default = {
        "security": 0.15,
        "risk": 0.15,
        "business": 0.2,
        "finance": 0.1,
        "longterm": 0.2,
        "shortterm": 0.2,
    }

    rules = [
        (["security", "attack", "defense"], {
            "security": 0.4,
            "risk": 0.3,
            "business": 0.15,
            "finance": 0.05,
            "longterm": 0.05,
            "shortterm": 0.05,
        }),
        (["startup", "saas"], {
            "business": 0.35,
            "finance": 0.25,
            "risk": 0.2,
            "longterm": 0.15,
            "security": 0.05,
            "shortterm": 0.0,
        }),
        (["quick", "mvp"], {
            "shortterm": 0.4,
            "risk": 0.25,
            "business": 0.2,
            "longterm": 0.1,
            "security": 0.05,
            "finance": 0.0,
        }),
    ]

    for keywords, weights in rules:
        if any(k in text for k in keywords):
            return weights

    return default


# -----------------------------
# Run decision path
# -----------------------------
def run_decision(decision: Dict, user_input: str):
    results: List[Dict] = []

    for agent_name in decision.get("agents", []):
        agent = AGENTS.get(agent_name)
        if agent:
            results.append({
                "agent": agent_name,
                "output": agent.run(user_input)
            })

    weights = get_dynamic_weights(user_input)
    final = synthesize(results, weights=weights)

    print("\n--- Polyreasoner ---")
    for item in final["summary"]:
        print(f"[{item['agent']} | {item['sentiment']}] {item['output']}")

    print("\nConfidence:", final["confidence"])

    if final["weighted_score"] is not None:
        print("Weighted score:", final["weighted_score"])

    if final["disagreement"]:
        print("\n⚠️ Disagreement detected between perspectives.")

    print("\nNote:", final["note"])
    print("-------------------\n")


# -----------------------------
# Main loop
# -----------------------------
def main():
    main_agent = MainAgent()

    while True:
        user_input = input(">> ").strip()
        if not user_input:
            continue

        # 1. hard rules
        rule = rule_route(user_input)
        if rule == "chat":
            print("\n[MainAgent] Hello. What are you thinking about?\n")
            continue

        # 2. embedding-based intent routing
        intent = embedding_route(user_input)

        # 3. ideas → RAG
        if intent == "ideas":
            ideas = retrieve_ideas(user_input)
            print("\n--- Ideas (RAG) ---")
            if not ideas:
                print("No relevant ideas found.")
            else:
                for idea in ideas:
                    print("-", idea["text"])
            print("------------------\n")
            continue

        # 4. decision → MainAgent (agent selection only)
        if intent == "decision":
            decision_raw = main_agent.run(user_input)

            try:
                decision = json.loads(decision_raw)
            except Exception:
                print("\n[MainAgent]")
                print(decision_raw)
                print()
                continue

            run_decision(decision, user_input)
            continue

        # fallback
        print("\n[MainAgent] Tell me more.\n")


if __name__ == "__main__":
    main()
