"""Reusable custom widgets."""

import tkinter as tk
from typing import Callable

from utils import colors, fonts


class ChoiceButton(tk.Button):
    """A large, left-aligned button used for round choices."""

    def __init__(self, master: tk.Widget, text: str, choice: str, command: Callable, **kwargs):
        self.choice = choice
        super().__init__(
            master,
            text=text,
            command=command,
            font=fonts.BUTTON,
            bg=colors.BUTTON_BG,
            fg=colors.TEXT_PRIMARY,
            activebackground=colors.BUTTON_BG_HOVER,
            activeforeground=colors.TEXT_PRIMARY,
            disabledforeground=colors.TEXT_FAINT,
            highlightbackground=colors.BUTTON_BORDER,
            relief=tk.FLAT,
            anchor=tk.W,
            justify=tk.LEFT,
            wraplength=640,
            padx=14,
            pady=10,
            cursor="hand2",
            **kwargs,
        )

    def set_label(self, letter: str, text: str) -> None:
        self.config(text=f"{letter})  {text}")
