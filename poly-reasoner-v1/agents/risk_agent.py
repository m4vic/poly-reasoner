from agents.base import BaseAgent


class RiskAgent(BaseAgent):
    name = "risk"
    system_prompt = "Identify failure modes, uncertainty, and risks."
