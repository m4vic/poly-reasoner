from agents.base import BaseAgent


class SecurityAgent(BaseAgent):
    name = "security"
    system_prompt = "Analyze security risks, misuse, abuse, and trust issues."
