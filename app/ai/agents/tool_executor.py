class ToolExecutor:
    def __init__(self, registry):
        self.registry = registry

    def execute(self, tool_name: str, tool_input: dict):
        tool_entry = self.registry.get_tool(tool_name)

        if not tool_entry:
            raise ValueError(f"Tool {tool_name} not found")

        tool = tool_entry["tool"]
        input_model = tool_entry["input_model"]

        structured_input = input_model(**tool_input)
        output = tool.run(structured_input)

        return output.result