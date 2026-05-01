from ..tools.tool_executor import ToolExecutor
from ..prompts.react_prompt import react_prompt
from ...utils.parsing.output_parser import parse_agent_output
from ...utils.retry import retry_with_correction
from ...schemas.planner_schema import Plan
from ..tools.tool_ranker import ToolRanker

class ExecutorAgent:
    def __init__(self, llm, registry):
        self.llm = llm
        self.registry = registry
        self.tool_executor = ToolExecutor(registry)
        self.react_chain = react_prompt | llm
        self.tool_ranker = ToolRanker(llm, registry)

    async def execute(self, plan: Plan, user_id: str):

        results = []
        context_memory = []   # stores observations across steps

        MAX_RETRY_PER_STEP = 2

        for step_index, step in enumerate(plan.steps):

            original_tool = step.action
            tool_input = step.input or {}

            # Tool Ranking Layer
            ranked_tools = self.tool_ranker.rank_tools(
                step.description if hasattr(step, "description") else str(step),
                context_memory
            )

            # Ensure original tool is included
            tool_candidates = [original_tool]

            for t in ranked_tools:
                if t["tool"] not in tool_candidates:
                    tool_candidates.append(t["tool"])

            #  Decision Logic
            success = False

            for candidate_tool in tool_candidates:

                tool_name = candidate_tool
                retry_count = 0

                while retry_count <= MAX_RETRY_PER_STEP:

                    print(f"\n[Tool Attempt] Trying: {tool_name}")

                    decision = await retry_with_correction(
                        self.react_chain,
                        {
                            "input": f"""
                                You are executing a planned step.

                                Tool: {tool_name}

                                Rules:
                                - You MUST use this tool
                                - You may ONLY adjust input

                                Input:
                                {tool_input}

                                Previous Observations:
                                {context_memory}

                                Return JSON.
                            """,
                            "tools": self.registry.get_tool_descriptions(),
                        },
                        parse_agent_output,
                    )

                    updated_input = decision.input or tool_input

                    tool_result = self.tool_executor.execute_with_retry(
                        tool_name,
                        updated_input,
                        retries=1
                    )

                    if not tool_result.success:
                        retry_count += 1

                        context_memory.append(
                            f"Tool {tool_name} FAILED: {tool_result.error}"
                        )

                        if retry_count > MAX_RETRY_PER_STEP:
                            break  # try next tool

                        continue

                    # SUCCESS
                    context_memory.append(
                        f"Tool {tool_name} SUCCESS: {tool_result.data}"
                    )

                    results.append({
                        "step": step_index,
                        "tool": tool_name,
                        "success": True,
                        "data": tool_result.data
                    })

                    success = True
                    break  # stop retry loop

                if success:
                    break  # stop tool fallback loop
        
            if not success:
                results.append({
                    "step": step_index,
                    "tool": original_tool,
                    "success": False,
                    "error": "All tool attempts failed"
                })

        return {
            "execution": results,
            "context": context_memory
        }