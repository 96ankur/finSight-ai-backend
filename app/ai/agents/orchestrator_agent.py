from .planner_agent import PlannerAgent
from .executor_agent import ExecutorAgent
from ..tools.tool_registry import ToolRegistry


class Orchestrator:
    def __init__(self, llm):
        self.planner = PlannerAgent(llm)
        self.llm = llm

    async def run(self, query: str, user_id: str):

        registry = ToolRegistry.for_user(user_id)
        executor = ExecutorAgent(self.llm, registry)

        tools_description = registry.get_tool_descriptions()

        # 1. PLAN
        try:
            plan = await self.planner.create_plan(query, tools_description)
        except Exception as e:
            return {
                "error": "Failed to generate plan",
                "details": str(e)
            }

        # 2. EXECUTE
        results = await executor.execute(plan, user_id)

        # 3. FINAL ANSWER (simple for now)
        return {
            "plan": plan.model_dump(),
            "execution": results
        }