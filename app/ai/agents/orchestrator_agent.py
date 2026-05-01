from .planner_agent import PlannerAgent
from .executor_agent import ExecutorAgent
from ..tools.tool_registry import ToolRegistry
from ..memory.memory_manager import MemoryManager


class Orchestrator:
    def __init__(self, llm):
        self.llm = llm
        self.planner = PlannerAgent(llm)
        self.memory = MemoryManager(llm)

    async def run(self, query: str, user_id: str):

        registry = ToolRegistry.for_user(user_id)
        executor = ExecutorAgent(self.llm, registry)

        tools_description = registry.get_tool_descriptions()

        # 1. PLAN
        try:
            memory_context = await self.memory.build_context(
                user_id,
                query
            )

            enhanced_query = f"""
                User Query:
                {query}

                Memory Context:
                {memory_context}
            """
            plan = await self.planner.create_plan(enhanced_query, tools_description)

        except Exception as e:
            return {
                "error": "Failed to generate plan",
                "details": str(e)
            }

        # 2. EXECUTE
        results = await executor.execute(plan, user_id)

        final_answer = str(results)

        await self.memory.update_memory(
            user_id,
            query,
            final_answer
)

        # 3. FINAL ANSWER (simple for now)
        return {
            "plan": plan.model_dump(),
            "execution": results
        }