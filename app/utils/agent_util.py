import json

def parse_agent_output(text: str):
    try:
        return json.loads(text)
    except:
        return {"tool": None, "input": text}