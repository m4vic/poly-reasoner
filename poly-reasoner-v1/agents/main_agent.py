# agents/main_agent.py

from llm import get_llm


class MainAgent:
    name = "main"

    system_prompt = """
You are a routing engine.
You DO NOT chat.
You DO NOT explain.
You ONLY output valid JSON.
"""

    def run(self, user_input: str) -> str:
        llm = get_llm()

        prompt = f"""
<System>
{self.system_prompt}
</System>

<User>
Classify the input below and output ONLY JSON.
No markdown. No text. No explanations.

User input:
"{user_input}"

JSON schema:
{{
  "type": "chat" | "ideas" | "decision",
  "agents": ["security","risk","business","finance","longterm","shortterm"]
}}
</User>

<Assistant>
"""
        out = llm(
            prompt,
            max_tokens=120,
            temperature=0.0,
            stop=["</Assistant>", "</Human>"],  # 🔑 IMPORTANT
        )

        return out["choices"][0]["text"].strip()
