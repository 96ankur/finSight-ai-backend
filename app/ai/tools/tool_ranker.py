import json


class ToolRanker:
    def __init__(self, llm, registry):
        self.llm = llm
        self.registry = registry

    def rank_tools(self, step_description: str, context: str):
        tools = self.registry.get_all_tools()

        tool_descriptions = "\n".join([
            f"{tool.name}: {tool.description}"
            for tool in tools
        ])

        prompt = f"""
Select the TOP 3 most relevant tools for the task.

Step:
{step_description}

Context:
{context}

Available Tools:
{tool_descriptions}

Return STRICT JSON:
[
  {{"tool": "name", "score": 0.0-1.0}},
  {{"tool": "name", "score": 0.0-1.0}},
  {{"tool": "name", "score": 0.0-1.0}}
]
"""

        response = self.llm.invoke(prompt)

        try:
            ranked = json.loads(response.content)
            return ranked
        except:
            return []