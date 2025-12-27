from agents.base import BaseAgent


class ShortTermAgent(BaseAgent):
    name = "shortterm"
    system_prompt = "Evaluate short-term feasibility and speed."
