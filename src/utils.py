import json
from typing import Dict, Any


def format_json_response(data: Dict[str, Any]) -> str:
    """Format the response as a pretty-printed JSON string."""
    return json.dumps(data, indent=2, ensure_ascii=False)


def save_example(user_input: str, response: Dict[str, Any], filename: str) -> None:
    """Save an example input-output pair to a file."""
    example = {"input": user_input, "output": response}

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(example, f, indent=2, ensure_ascii=False)
