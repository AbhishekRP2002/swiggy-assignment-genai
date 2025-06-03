import json
import os
from typing import Dict, Any


def format_json_response(data: Dict[str, Any]) -> str:
    """Format the response as a pretty-printed JSON string."""
    return json.dumps(data, indent=2, ensure_ascii=False)


def save_example(user_input: str, response: Dict[str, Any], filename: str) -> None:
    """Save an example input-output pair to a JSON file."""
    example = {"input": user_input, "output": response}

    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    examples_dir = os.path.join(root_dir, "examples")
    os.makedirs(examples_dir, exist_ok=True)

    file_path = os.path.join(examples_dir, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(example, f, indent=2, ensure_ascii=False)
