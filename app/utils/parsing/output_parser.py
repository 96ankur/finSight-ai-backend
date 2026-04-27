import json
from pydantic import ValidationError
from app.core.logging import get_logger
from ...schemas.AgentDecision import AgentDecision

logger = get_logger("access")

def parse_agent_output(text: str):
    try:
        logger.info(f"Parsing agent output: {text}")
        data = json.loads(text)
        return AgentDecision(**data)
    except (json.JSONDecodeError, ValidationError) as e:
        logger.error(f"Agent output parsing failed with error: {e}")
        raise ValueError(f"Invalid LLM output: {text}")