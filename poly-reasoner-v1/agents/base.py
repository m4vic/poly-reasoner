from llm import get_llm


class BaseAgent:
    name = "base"
    system_prompt = ""

    def run(self, user_input: str) -> str:
        llm = get_llm()

        prompt = f"""
<System>
{self.system_prompt}
</System>

<User>
{user_input}
</User>

<Assistant>
"""
        out = llm(prompt, max_tokens=256, temperature=0.0)
        return out["choices"][0]["text"].strip()
