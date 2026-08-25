"""Main game window: layout, round display, and event handling."""

import json
import os
import tkinter as tk
from tkinter import messagebox
from typing import Any, Dict

from game_state import GameState
from ui.modals import show_ending_modal, show_term_modal
from ui.sketches import render_sketch
from ui.widgets import ChoiceButton
from utils import colors, fonts

CHOICE_LETTERS = ["A", "B", "C"]
SAVE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "saves", "game.json")


class MainWindow(tk.Frame):
    def __init__(self, root: tk.Tk, game_state: GameState, game_data: Dict[str, Any]):
        super().__init__(root, bg=colors.BG)
        self.root = root
        self.state_obj = game_state
        self.data = game_data

        self.pack(fill=tk.BOTH, expand=True)
        self._setup_ui()
        self.display_round()

    # ------------------------------------------------------------------ #
    # Layout
    # ------------------------------------------------------------------ #
    def _setup_ui(self) -> None:
        self.header = tk.Label(
            self,
            text="ISLAND ECONOMY — THE GAME",
            font=fonts.TITLE,
            fg=colors.ACCENT_GREEN,
            bg=colors.BG,
        )
        self.header.pack(pady=(14, 4))

        self.info = tk.Label(self, text="", font=fonts.SUBTITLE, fg=colors.TEXT_SECONDARY, bg=colors.BG)
        self.info.pack(pady=(0, 10))

        self.sketch = tk.Canvas(
            self,
            width=460,
            height=220,
            bg=colors.BG_PANEL,
            highlightthickness=1,
            highlightbackground=colors.BORDER,
        )
        self.sketch.pack(pady=(0, 10))

        self.narrative = tk.Label(
            self,
            text="",
            font=fonts.NARRATIVE,
            fg=colors.TEXT_PRIMARY,
            bg=colors.BG,
            wraplength=680,
            justify=tk.LEFT,
        )
        self.narrative.pack(pady=(0, 14), padx=24)

        self.choices_frame = tk.Frame(self, bg=colors.BG)
        self.choices_frame.pack(pady=(0, 10), fill=tk.X, padx=40)

        self.choice_buttons = {}
        for letter in CHOICE_LETTERS:
            btn = ChoiceButton(
                self.choices_frame,
                text="",
                choice=letter,
                command=lambda c=letter: self.on_choice(c),
            )
            self.choice_buttons[letter] = btn

        self.footer = tk.Frame(self, bg=colors.BG)
        self.footer.pack(side=tk.BOTTOM, pady=14)

        tk.Button(
            self.footer, text="Save Game", command=self.save_game, font=fonts.BUTTON,
            bg=colors.BUTTON_BG, fg=colors.TEXT_PRIMARY, relief=tk.FLAT, padx=10, pady=4, cursor="hand2",
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            self.footer, text="Load Game", command=self.load_game, font=fonts.BUTTON,
            bg=colors.BUTTON_BG, fg=colors.TEXT_PRIMARY, relief=tk.FLAT, padx=10, pady=4, cursor="hand2",
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            self.footer, text="Quit", command=self.root.quit, font=fonts.BUTTON,
            bg=colors.ACCENT_RED, fg=colors.TEXT_PRIMARY, relief=tk.FLAT, padx=10, pady=4, cursor="hand2",
        ).pack(side=tk.LEFT, padx=5)

    # ------------------------------------------------------------------ #
    # Round display
    # ------------------------------------------------------------------ #
    def display_round(self) -> None:
        if self.state_obj.game_over:
            self.show_ending()
            return

        round_data = self.data["rounds"][self.state_obj.current_round]

        self.info.config(
            text=(
                f"Round {self.state_obj.current_round} of 9  |  "
                f"Population: {self.state_obj.population}  |  Year: {self.state_obj.year}"
            )
        )

        self.sketch.delete("all")
        render_sketch(self.sketch, round_data["sketch_key"], self.data)

        narrative_text = f"{round_data['scenario']}\n\n{round_data['narrative']}"
        self.narrative.config(text=narrative_text)

        active_letters = list(round_data["choices"].keys())
        for letter in CHOICE_LETTERS:
            btn = self.choice_buttons[letter]
            if letter in active_letters:
                choice_data = round_data["choices"][letter]
                btn.set_label(letter, choice_data["text"])
                btn.config(state=tk.NORMAL)
                btn.pack(anchor=tk.W, pady=6, fill=tk.X)
            else:
                btn.pack_forget()

    def on_choice(self, choice: str) -> None:
        for btn in self.choice_buttons.values():
            btn.config(state=tk.DISABLED)

        round_data = self.data["rounds"][self.state_obj.current_round]
        choice_data = round_data["choices"][choice]
        term_index = choice_data["term_index"]

        if term_index is not None:
            term_data = round_data["economic_terms"][term_index]
            show_term_modal(self.root, term_data)

        self.state_obj.make_choice(choice, self.data)

        if self.state_obj.game_over:
            self.show_ending()
        else:
            self.display_round()

    def show_ending(self) -> None:
        ending_data = self.data["endings"][self.state_obj.current_ending]
        show_ending_modal(self.root, ending_data, self.state_obj, self)

    # ------------------------------------------------------------------ #
    # Save / Load
    # ------------------------------------------------------------------ #
    def save_game(self) -> None:
        os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
        with open(SAVE_PATH, "w", encoding="utf-8") as f:
            json.dump(self.state_obj.to_dict(), f)
        messagebox.showinfo("Saved", "Game saved.")

    def load_game(self) -> None:
        try:
            with open(SAVE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            messagebox.showwarning("No Save Found", "No save file found.")
            return
        except (json.JSONDecodeError, KeyError):
            messagebox.showerror("Load Failed", "The save file is corrupted.")
            return

        self.state_obj = GameState.from_dict(data)
        self.display_round()
