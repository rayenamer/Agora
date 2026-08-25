"""Load and validate game_data.json."""

import json
import os
from typing import Any, Dict


def load_game_data(filepath: str) -> Dict[str, Any]:
    """Load game_data.json and validate its top-level structure.

    Raises FileNotFoundError if the file is missing, and ValueError if
    required keys or cross-references are missing.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Game data file not found: {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    for key in ("rounds", "endings", "sketches"):
        if key not in data:
            raise ValueError(f"game_data.json missing required key: '{key}'")

    # Normalize round keys to int for easy lookup by GameState.
    data["rounds"] = {int(k): v for k, v in data["rounds"].items()}

    _validate_references(data)
    return data


def _validate_references(data: Dict[str, Any]) -> None:
    """Check that every choice points to a real round or ending, and that
    every sketch_key referenced by a round actually exists."""
    round_numbers = set(data["rounds"].keys())
    ending_keys = set(data["endings"].keys())
    sketch_keys = set(data["sketches"].keys())

    for round_num, round_data in data["rounds"].items():
        sketch_key = round_data.get("sketch_key")
        if sketch_key not in sketch_keys:
            raise ValueError(
                f"Round {round_num} references missing sketch '{sketch_key}'"
            )

        for choice_letter, choice in round_data["choices"].items():
            leads_to = choice["leads_to"]
            if leads_to.startswith("round_"):
                target = int(leads_to.split("_")[1])
                if target not in round_numbers:
                    raise ValueError(
                        f"Round {round_num} choice {choice_letter} leads to "
                        f"missing round {target}"
                    )
            elif leads_to not in ending_keys:
                raise ValueError(
                    f"Round {round_num} choice {choice_letter} leads to "
                    f"missing ending '{leads_to}'"
                )
