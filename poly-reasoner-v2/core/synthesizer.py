from typing import List, Dict
from urllib import response
from core.llm import get_llm
from config import WEIGHT_RULES

class Synthesizer:
    """Combines multiple agent perspectives into coherent response"""
    
    def __init__(self):
        self.llm = get_llm()
    
    def synthesize(self, perspectives: List[Dict], user_query: str) -> Dict:
        """
        Synthesize agent outputs
        perspectives: [{"agent": "security", "output": "...", "weight": 0.3}]
        Returns: {
            "response": str,
            "confidence": float,
            "disagreements": List[str],
            "consensus": bool
        }
        """
        if not perspectives:
            return {
                "response": "No perspectives available",
                "confidence": 0.0,
                "disagreements": [],
                "consensus": False
            }
        
        # Format perspectives for synthesis
        formatted = self._format_perspectives(perspectives)
        
        prompt = f"""Synthesize these expert perspectives into ONE coherent response.

User asked: "{user_query}"

Expert Perspectives:
{formatted}

Your synthesis should:
1. Highlight key consensus points
2. Note any conflicts/trade-offs explicitly
3. Give prioritized recommendations
4. Be actionable and concise (under 200 words)

Also output:
- Confidence (0.0-1.0): How aligned are the perspectives?
- Disagreements: List any conflicting viewpoints

Format:
RESPONSE: [your synthesis]
CONFIDENCE: [0.0-1.0]
DISAGREEMENTS: [comma-separated list or "none"]

Begin:"""
        
        result = self.llm.generate(prompt, max_tokens=400, temperature=0.5)
        
        # Parse structured output
        return self._parse_synthesis(result)
    
    def _format_perspectives(self, perspectives: List[Dict]) -> str:
        """Format agent outputs with weights"""
        lines = []
        for p in perspectives:
            weight_pct = int(p.get("weight", 0.5) * 100)
            lines.append(f"[{p['agent'].upper()} - {weight_pct}% weight]\n{p['output']}\n")
        return "\n".join(lines)
    def get_dynamic_weights(self, user_input: str) -> Dict[str, float]:
        """Get agent weights based on query keywords"""
        from config import WEIGHT_RULES
    
        text = user_input.lower()
    
    # Check keyword rules
        for rule in WEIGHT_RULES:
            if any(kw in text for kw in rule["keywords"]):
                return rule["weights"]
    
    # Default: equal weights
        return {
            "security": 0.166,
        "risk": 0.166,
        "business": 0.166,
        "finance": 0.166,
        "longterm": 0.166,
        "shortterm": 0.166
        }
    def _parse_synthesis(self, raw: str) -> Dict:
        """Extract structured data from synthesis"""
        response = ""
        confidence = 0.5
        disagreements = []
    
    # Split by lines
        lines = raw.split("\n")
    
    # Find RESPONSE line
        for i, line in enumerate(lines):
            if line.strip().startswith("RESPONSE:"):
            # Get text after RESPONSE: until CONFIDENCE or end
                response_text = line.replace("RESPONSE:", "").strip()
            
            # Continue reading until next marker
                for j in range(i+1, len(lines)):
                    if lines[j].strip().startswith("CONFIDENCE:") or lines[j].strip().startswith("DISAGREEMENTS:"):
                        break
                    response_text += " " + lines[j].strip()
            
                response = response_text.strip()
                break
    
    # Find CONFIDENCE
        for line in lines:
            if line.strip().startswith("CONFIDENCE:"):
                try:
                    conf_str = line.replace("CONFIDENCE:", "").strip()
                    confidence = float(conf_str)
                except:
                    confidence = 0.5
    
    # Find DISAGREEMENTS
        for line in lines:
            if line.strip().startswith("DISAGREEMENTS:"):
                dis = line.replace("DISAGREEMENTS:", "").strip()
                if dis.lower() not in ["none", ""]:
                    disagreements = [d.strip() for d in dis.split(",")]
    
    # Fallback: if no RESPONSE found, use first paragraph
        if not response:
            response = raw.split("\n\n")[0] if raw else "Unable to synthesize response"
    
        return {
            "response": response,
            "confidence": confidence,
            "disagreements": disagreements,
            "consensus": len(disagreements) == 0
        }