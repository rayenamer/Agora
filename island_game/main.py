"""Entry point for Island Economy."""

import os
import sys
import tkinter as tk

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data.parser import load_game_data
from game_state import GameState
from ui.main_window import MainWindow

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "game_data.json")


def main() -> None:
    root = tk.Tk()
    root.geometry("900x700")
    root.minsize(800, 600)
    root.title("Agora island")
    root.configure(bg="#1a1a1a")

    game_data = load_game_data(DATA_PATH)
    game_state = GameState()

    MainWindow(root, game_state, game_data)
    root.mainloop()


if __name__ == "__main__":
    main()
