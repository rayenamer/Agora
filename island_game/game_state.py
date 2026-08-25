"""Game state and decision-tree logic for Island Economy."""

from __future__ import annotations

from typing import Any, Dict, List, Optional


class GameState:
    """Tracks the player's progress through the decision tree."""

    def __init__(self) -> None:
        self.current_round: int = 1
        self.population: int = 3
        self.year: int = 1
        self.decision_path: List[str] = []
        self.game_over: bool = False
        self.current_ending: Optional[str] = None

    def make_choice(self, choice: str, game_data: Dict[str, Any]) -> str:
        """Apply a choice letter for the current round, update state, and
        return the resulting node ('round_N' or an ending key like 'E1')."""
        round_data = game_data["rounds"][self.current_round]
        choice_data = round_data["choices"][choice]
        self.decision_path.append(choice)

        next_node = choice_data["leads_to"]
        if next_node.startswith("E"):
            self.game_over = True
            self.current_ending = next_node
        else:
            next_round = int(next_node.split("_")[1])
            self.current_round = next_round
            next_round_data = game_data["rounds"][next_round]
            self.year = next_round_data["year"]
            self.population = next_round_data["population"]

        return next_node

    def reset(self) -> None:
        """Start a new game."""
        self.current_round = 1
        self.population = 3
        self.year = 1
        self.decision_path = []
        self.game_over = False
        self.current_ending = None

    def to_dict(self) -> Dict[str, Any]:
        """Serialize for a save file."""
        return {
            "round": self.current_round,
            "population": self.population,
            "year": self.year,
            "path": self.decision_path,
            "game_over": self.game_over,
            "current_ending": self.current_ending,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "GameState":
        """Deserialize from a save file."""
        state = GameState()
        state.current_round = data["round"]
        state.population = data["population"]
        state.year = data["year"]
        state.decision_path = data["path"]
        state.game_over = data.get("game_over", False)
        state.current_ending = data.get("current_ending")
        return state
