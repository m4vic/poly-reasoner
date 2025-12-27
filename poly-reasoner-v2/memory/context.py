from typing import List, Dict, Optional
from datetime import datetime

class ConversationContext:
    """Tracks conversation state and history"""
    
    def __init__(self):
        self.history: List[Dict] = []
        self.current_topic: Optional[str] = None
        self.current_state: str = "idle"  # idle, active, closing
        self.last_intent: Optional[str] = None
    
    def add_turn(self, user_input: str, ai_response: str, intent: str):
        """Add conversation turn"""
        self.history.append({
            "timestamp": datetime.now().isoformat(),
            "user": user_input,
            "ai": ai_response,
            "intent": intent
        })
        self.last_intent = intent
        
        # Update state
        if intent == "chat" and any(word in user_input.lower() for word in ["thanks", "thank", "ok", "got it"]):
            self.current_state = "closing"
            self.current_topic = None
        elif intent == "analyze":
            self.current_state = "active"
        elif intent == "chat" and user_input.lower() in ["hi", "hello", "hey"]:
            if self.current_state == "closing":
                self.current_state = "idle"  # Reset
    
    def get_state_summary(self) -> str:
        """Get current conversation state as string"""
        if self.current_state == "idle":
            return "New conversation, no active topic"
        elif self.current_state == "active":
            return f"Active discussion about: {self.current_topic or 'ongoing topic'}"
        elif self.current_state == "closing":
            return "User acknowledged response, topic closed"
        return "Unknown state"
    
    def get_recent_context(self, n=3) -> str:
        """Get last n conversation turns as context"""
        if not self.history:
            return "No previous conversation"
        
        recent = self.history[-n:]
        formatted = []
        for turn in recent:
            formatted.append(f"User: {turn['user']}")
            formatted.append(f"AI: {turn['ai'][:100]}...")  # Truncate AI response
        
        return "\n".join(formatted)
    
    def should_use_perspectives(self) -> bool:
        """Determine if we should activate perspective agents"""
        # Don't use perspectives if just closed a topic
        if self.current_state == "closing":
            return False
        
        # Don't use for simple greetings
        if self.last_intent == "chat":
            return False
        
        return True