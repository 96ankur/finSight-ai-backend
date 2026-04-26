async def get_valid_decision(chain, inputs, parser, max_retries=2):
    for attempt in range(max_retries):
        response = await chain.ainvoke(inputs)

        try:
            return parser(response.content)

        except Exception:
            # Force correction
            inputs["input"] += "\n\nIMPORTANT: Fix your JSON. Follow schema strictly."

    raise ValueError("Failed to get valid structured output")