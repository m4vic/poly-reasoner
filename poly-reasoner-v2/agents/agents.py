from core.llm import get_llm

class BaseAgent:
    """Base class for all perspective agents"""
    name = "base"
    expertise = "general analysis"
    
    def analyze(self, user_query: str) -> str:
        """Generate perspective-specific analysis"""
        llm = get_llm()
        
        prompt = f"""You are the {self.name.upper()} expert.
Your expertise: {self.expertise}

User query: "{user_query}"

Analyze from ONLY your {self.name} perspective:
- Key considerations (2-3 points)
- Main risk or opportunity
- Specific recommendation

Keep response under 100 words. Be direct and actionable.

Analysis:"""
        
        return llm.generate(prompt, max_tokens=150, temperature=0.4)


class SecurityAgent(BaseAgent):
    name = "security"
    expertise = "cybersecurity risks, vulnerabilities, threat modeling, data protection, compliance"


class RiskAgent(BaseAgent):
    name = "risk"
    expertise = "operational risks, failure modes, mitigation strategies, contingency planning"


class BusinessAgent(BaseAgent):
    name = "business"
    expertise = "market viability, competitive positioning, scalability, business model strategy"


class FinanceAgent(BaseAgent):
    name = "finance"
    expertise = "cost structure, ROI analysis, revenue potential, financial sustainability"


class LongTermAgent(BaseAgent):
    name = "longterm"
    expertise = "strategic vision, future-proofing, long-term sustainability, evolution planning"


class ShortTermAgent(BaseAgent):
    name = "shortterm"
    expertise = "immediate execution, MVP feasibility, quick wins, time-to-market optimization"


# Agent registry
AGENTS = {
    "security": SecurityAgent(),
    "risk": RiskAgent(),
    "business": BusinessAgent(),
    "finance": FinanceAgent(),
    "longterm": LongTermAgent(),
    "shortterm": ShortTermAgent(),
}