from pydantic import ValidationError
from ...schemas.tool_schema import ToolResult


class ToolExecutor:
    def __init__(self, registry):
        self.registry = registry

    def execute(self, tool_name: str, tool_input: dict) -> ToolResult:
        tool_entry = self.registry.get_tool(tool_name)

        if not tool_entry:
            return ToolResult(
                success=False,
                error=f"Tool {tool_name} not found"
            )

        tool = tool_entry["tool"]
        input_model = tool_entry["input_model"]

        # STEP 1: Validate Input
        try:
            structured_input = input_model(**tool_input)
        except ValidationError as e:
            return ToolResult(
                success=False,
                error=f"Invalid input for {tool_name}: {str(e)}"
            )

        # STEP 2: Safe Execution
        try:
            output = tool.run(structured_input)

            # STEP 3: Validate Output
            if not hasattr(output, "result"):
                return ToolResult(
                    success=False,
                    error=f"{tool_name} returned invalid output format"
                )

            return ToolResult(
                success=True,
                data=output.result
            )

        except Exception as e:
            return ToolResult(
                success=False,
                error=f"{tool_name} execution failed: {str(e)}"
            )
        
    def execute_with_retry(self, tool_name: str, tool_input: dict, retries=1) -> ToolResult:
        for attempt in range(retries + 1):
            result = self.execute(tool_name, tool_input)

            if result.success:
                return result

        return result