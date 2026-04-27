from langchain_core.messages import AIMessage
from ..tools.tool_executor import ToolExecutor
from ..prompts.react_prompt import react_prompt
from ...utils.parsing.output_parser import parse_agent_output
from ...utils.retry import retry_with_correction


class ExecutorAgent:
    def __init__(self, llm, registry):
        self.llm = llm
        self.registry = registry
        self.executor = ToolExecutor(registry)
        self.react_chain = react_prompt | llm

    async def execute(self, plan, user_id: str):

        results = []
        context_memory = []   # stores observations across steps

        MAX_RETRY_PER_STEP = 2

        for step_index, step in enumerate(plan.steps):

            tool_name = step.action
            tool_input = step.input or {}

            retry_count = 0

            while retry_count <= MAX_RETRY_PER_STEP:

                # Controlled reasoning (STRICT to current step)
                decision = await retry_with_correction(
                    self.react_chain,
                    {
                        "input": f"""
You are executing a planned step.

STRICT INSTRUCTION:
- You MUST use this tool: {tool_name}
- You are NOT allowed to change the tool
- You may ONLY adjust the input if needed

Current Step:
Tool: {tool_name}
Input: {tool_input}

Previous Observations:
{context_memory}

If input is wrong → fix it
If correct → proceed

Return JSON.
""",
                        "tools": self.registry.get_tool_descriptions(),
                    },
                    parse_agent_output,
                )

                updated_input = decision.input or tool_input

                # Inject user_id if needed
                if tool_name == "document_search":
                    updated_input["user_id"] = user_id

                # 🛠 Execute tool
                tool_result = self.executor.execute_with_retry(
                    tool_name,
                    updated_input,
                    retries=1
                )

                #  If tool failed → retry with corrected input
                if not tool_result.success:
                    retry_count += 1

                    context_memory.append(
                        f"""
Step {step_index} FAILED
Tool: {tool_name}
Error: {tool_result.error}
"""
                    )

                    if retry_count > MAX_RETRY_PER_STEP:
                        results.append({
                            "step": step_index,
                            "tool": tool_name,
                            "success": False,
                            "error": tool_result.error
                        })
                        break

                    continue

                #  Success
                context_memory.append(
                    f"""
                        Step {step_index} SUCCESS
                        Tool: {tool_name}
                        Result: {tool_result.data}
                    """
                )

                results.append({
                    "step": step_index,
                    "tool": tool_name,
                    "success": True,
                    "data": tool_result.data
                })

                break  # move to next step

        return {
            "execution": results,
            "context": context_memory
        }