import json
class VerificationAgent:
    def __init__(self, llm):
        self.llm = llm

    def verify(self, query: str, answer: str, context: str):
        prompt = f"""
            You are a strict financial verifier.

            Query:
            {query}

            Answer:
            {answer}

            Context:
            {context}

            Check:
            1. Is answer supported by context?
            2. Any hallucination?
            3. Any incorrect claim?

            Return JSON:
            {{
            "valid": true/false,
            "reason": "...",
            "confidence": 0.0-1.0
            }}
        """

        response = self.llm.invoke(prompt)

        try:
            return json.loads(response.content)
        except:
            return {"valid": False, "confidence": 0.0}