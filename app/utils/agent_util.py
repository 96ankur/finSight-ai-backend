import json
import re
from app.core.logging import get_logger

logger = get_logger("access")

def parse_agent_output(text: str):
    try:
        # Extract json object between { and }
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        return json.loads(text)
    except Exception as e:
        logger.error(f"Error in parse_agent_output: {e}")
        return {"tool": None, "input": text}


