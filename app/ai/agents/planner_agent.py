from ...utils.parsing.planner_parser import parse_plan
from ...utils.retry import retry_with_correction
from ..prompts.planner_prompt import planner_prompt

class PlannerAgent:
    def __init__(self, llm):
        self.chain = planner_prompt | llm

    async def create_plan(self, query: str, tools: str):

        plan = await retry_with_correction(
            self.chain,
            {
                "input": query,
                "tools": tools
            },
            parse_plan,
        )

        # ✅ Extra validation: empty plan fallback
        if not plan.steps:
            raise ValueError("Planner returned empty steps")

        return plan