import json
from pydantic import ValidationError
from ...schemas.planner_schema import Plan


def parse_plan(text: str) -> Plan:
    try:
        data = json.loads(text)
        return Plan(**data)
    except (json.JSONDecodeError, ValidationError):
        raise ValueError(f"Invalid planner output: {text}")