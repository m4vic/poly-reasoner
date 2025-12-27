from core.router import Router
from core.synthesizer import Synthesizer
from memory.context import ConversationContext
from agents.agents import AGENTS
from config import COMPLEXITY_THRESHOLD, CONFIDENCE_THRESHOLD
from typing import Dict, List


class PolyReasoner:
    """Main orchestrator for multi-agent reasoning"""
    
    def __init__(self):
        self.router = Router()
        self.synthesizer = Synthesizer()
        self.context = ConversationContext()
    
    def process(self, user_input: str) -> str:
        """Main processing pipeline"""
        
        chat_response = self._handle_chat(user_input)
        if chat_response:
            self.context.add_turn(user_input, chat_response, "chat")

            return chat_response
        
        response = self._handle_analysis_simple(user_input)
        self.context.add_turn(user_input, response, "analyze")
        return response
    
    def _handle_chat(self, user_input: str) -> str:
        text = user_input.lower().strip()
    
    # Expand chat phrases
        chat_phrases = [
        "hi", "hello", "hey", "thanks", "thank you", "ok", "bye", "got it",
        "how are you", "what's up", "sup", "howdy"
        ]
    
        if text in chat_phrases:
            if text in ["hi", "hello", "hey", "how are you", "what's up", "sup", "howdy"]:
                return "I'm doing well, thanks! What would you like to explore?"
            else:
                return "You're welcome! Feel free to ask anything else."
    
        return None
    
    
    def _handle_research(self, user_input: str) -> str:
        """Handle research queries (RAG/web search)"""
        # Placeholder for RAG integration
        return f"Research mode for: '{user_input}' (coming soon - will use RAG + web search)"
    
    def _format_analysis_output(self, synthesis: Dict, perspectives: List[Dict]) -> str:
        """Format the final analysis output - SIMPLE VERSION"""
        return synthesis["response"]  # Just return the synthesis, nothing else
    
    def _handle_analysis_simple(self, user_input: str) -> str:
        """Simplified analysis without complexity"""
    
        # 1. SELECT RELEVANT AGENTS
        print("\n🔍 Analyzing query...")
        agent_scores = self.router.select_agents(user_input)

        if not agent_scores:
            agent_scores = {"business": 0.7, "shortterm": 0.6}
        print(f"✓ Activated {len(agent_scores)} perspective agents")
    
    # 2. GET WEIGHTS FIRST
        weights = self.synthesizer.get_dynamic_weights(user_input)
    
    # 3. GATHER PERSPECTIVES
        perspectives = []
    
        for agent_name, relevance in agent_scores.items():
            print(f"  [{agent_name}] relevance: {relevance:.2f}")
            agent = AGENTS[agent_name]
            output = agent.analyze(user_input)
        
            perspectives.append({
            "agent": agent_name,
            "output": output,
            "weight": weights.get(agent_name, 0.5) * relevance
            })
    
    # 4. SYNTHESIZE
        print("🔄 Synthesizing perspectives...\n")
        result = self.synthesizer.synthesize(perspectives, user_input)
    
    # 5. RETURN SIMPLE OUTPUT
        return result["response"]
    

   













def main():
    """Main CLI loop"""
    print("\n🚀 Multi-Agent Poly-Reasoner")
    print("Type 'quit' to exit\n")
    
    reasoner = PolyReasoner()
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ["quit", "exit", "bye"]:
                print("Goodbye!")
                break
            
            response = reasoner.process(user_input)
            print(f"\nAI:\n{response}\n")
        
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    main()