async def retry_with_correction(chain, inputs, parser, max_retries=2):
    last_error = None

    for attempt in range(max_retries):
        response = await chain.ainvoke(inputs)

        try:
            return parser(response.content)

        except Exception as e:
            last_error = str(e)

            # self-correction instruction
            inputs["input"] += f"""

IMPORTANT:
Your previous output was invalid.

Error:
{last_error}

Fix your JSON and strictly follow the schema.
"""

    raise ValueError(f"Planner failed after retries: {last_error}")