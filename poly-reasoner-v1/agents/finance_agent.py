from agents.base import BaseAgent


class FinanceAgent(BaseAgent):
    name = "finance"
    system_prompt = "Analyze cost, ROI, and monetization."
