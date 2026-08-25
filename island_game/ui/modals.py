"""Pop-up modal windows: economic term explanations and ending summaries."""

import tkinter as tk
from typing import Any, Dict

from utils import colors, fonts


def _center_on_parent(modal: tk.Toplevel, parent: tk.Misc, width: int, height: int) -> None:
    modal.update_idletasks()
    x = parent.winfo_rootx() + (parent.winfo_width() - width) // 2
    y = parent.winfo_rooty() + (parent.winfo_height() - height) // 2
    modal.geometry(f"{width}x{height}+{max(x, 0)}+{max(y, 0)}")


def show_term_modal(parent: tk.Misc, term_data: Dict[str, Any]) -> None:
    """Show an economic term explanation modal. Blocks until dismissed."""
    modal = tk.Toplevel(parent)
    modal.title("Economic Concept")
    modal.configure(bg=colors.BG)
    modal.transient(parent)
    modal.resizable(False, False)

    tk.Label(
        modal,
        text=f"\U0001F4DA {term_data['term'].upper()}",
        font=fonts.MODAL_TITLE,
        fg=colors.ACCENT_GREEN,
        bg=colors.BG,
        wraplength=560,
        justify=tk.LEFT,
    ).pack(pady=(18, 6), padx=24, anchor=tk.W)

    tk.Frame(modal, bg=colors.BORDER, height=1).pack(fill=tk.X, padx=24, pady=(0, 12))

    body = (
        f"Definition:\n{term_data['definition']}\n\n"
        f"What just happened in your choice:\n{term_data['consequence']}\n\n"
        f"Real-world impact:\n{term_data['realworld']}"
    )
    tk.Label(
        modal,
        text=body,
        font=fonts.MODAL_BODY,
        fg=colors.TEXT_PRIMARY,
        bg=colors.BG,
        wraplength=560,
        justify=tk.LEFT,
    ).pack(padx=24, pady=(0, 16), anchor=tk.W)

    def close_modal(event=None):
        modal.destroy()

    btn = tk.Button(
        modal,
        text="Continue →",
        command=close_modal,
        font=fonts.BUTTON,
        bg=colors.ACCENT_GREEN_DIM,
        fg="#000000",
        relief=tk.FLAT,
        padx=16,
        pady=6,
        cursor="hand2",
    )
    btn.pack(pady=(0, 18))

    modal.bind("<Return>", close_modal)
    _center_on_parent(modal, parent, 620, 380)
    modal.grab_set()
    btn.focus_set()
    parent.wait_window(modal)


def show_ending_modal(parent: tk.Misc, ending_data: Dict[str, Any], game_state, main_window) -> None:
    """Show the ending summary modal with stats, real-world parallel, and
    Play Again / View Summary / Quit controls."""
    modal = tk.Toplevel(parent)
    modal.title("Game Over -- Ending Reached")
    modal.configure(bg=colors.BG)
    modal.transient(parent)
    modal.resizable(False, False)

    tk.Label(
        modal,
        text="\U0001F3C1 GAME OVER -- ENDING REACHED",
        font=fonts.MODAL_BODY,
        fg=colors.TEXT_MUTED,
        bg=colors.BG,
    ).pack(pady=(16, 4))

    tk.Label(
        modal,
        text=f"{ending_data['name'].upper()}  {ending_data['emoji']}",
        font=fonts.MODAL_TITLE,
        fg=colors.ACCENT_GREEN,
        bg=colors.BG,
        wraplength=620,
        justify=tk.CENTER,
    ).pack(pady=(0, 10))

    tk.Label(
        modal,
        text=ending_data["narrative"],
        font=fonts.MODAL_BODY,
        fg=colors.TEXT_PRIMARY,
        bg=colors.BG,
        wraplength=620,
        justify=tk.LEFT,
    ).pack(padx=28, pady=(0, 12))

    stats = ending_data["stats"]
    stats_text = (
        "FINAL STATS\n"
        + "━" * 32
        + f"\nGDP per capita:       ${stats['gdp_per_capita']:,}\n"
        f"Annual growth:        {stats['annual_growth']:.1f}%\n"
        f"Inequality (Gini):    {stats['gini']:.2f}\n"
        f"Stability:            {stats['stability_years']} years\n"
        f"Final population:     {stats['population_final']}"
    )
    tk.Label(
        modal,
        text=stats_text,
        font=fonts.MODAL_STATS,
        fg=colors.STATS_TEXT,
        bg=colors.BG_PANEL,
        justify=tk.LEFT,
        padx=16,
        pady=12,
    ).pack(padx=28, pady=(0, 12), fill=tk.X)

    tk.Label(
        modal,
        text=f"Real-world parallel ({ending_data['country']}):\n{ending_data['realworld']}",
        font=fonts.MODAL_SMALL,
        fg=colors.TEXT_SECONDARY,
        bg=colors.BG,
        wraplength=620,
        justify=tk.LEFT,
    ).pack(padx=28, pady=(0, 10))

    path_str = " → ".join(game_state.decision_path)
    tk.Label(
        modal,
        text=f"Your decision path: {path_str}",
        font=fonts.MODAL_SMALL,
        fg=colors.TEXT_FAINT,
        bg=colors.BG,
    ).pack(pady=(0, 14))

    def play_again():
        modal.destroy()
        game_state.reset()
        main_window.display_round()

    def view_summary():
        show_summary_modal(modal, game_state, main_window.data)

    def quit_game():
        parent.quit()

    btn_frame = tk.Frame(modal, bg=colors.BG)
    btn_frame.pack(pady=(0, 20))

    tk.Button(
        btn_frame, text="Play Again", command=play_again, font=fonts.BUTTON,
        bg=colors.ACCENT_GREEN_DIM, fg="#000000", relief=tk.FLAT, padx=14, pady=6, cursor="hand2",
    ).pack(side=tk.LEFT, padx=6)

    tk.Button(
        btn_frame, text="View Summary", command=view_summary, font=fonts.BUTTON,
        bg=colors.BUTTON_BG, fg=colors.TEXT_PRIMARY, relief=tk.FLAT, padx=14, pady=6, cursor="hand2",
    ).pack(side=tk.LEFT, padx=6)

    tk.Button(
        btn_frame, text="Quit", command=quit_game, font=fonts.BUTTON,
        bg=colors.ACCENT_RED, fg=colors.TEXT_PRIMARY, relief=tk.FLAT, padx=14, pady=6, cursor="hand2",
    ).pack(side=tk.LEFT, padx=6)

    _center_on_parent(modal, parent, 680, 620)
    modal.grab_set()


def show_summary_modal(parent: tk.Misc, game_state, game_data: Dict[str, Any]) -> None:
    """Show the full decision transcript: each round's title and the choice made."""
    modal = tk.Toplevel(parent)
    modal.title("Game Summary")
    modal.configure(bg=colors.BG)
    modal.transient(parent)
    modal.resizable(False, False)

    tk.Label(
        modal,
        text="YOUR PLAYTHROUGH",
        font=fonts.MODAL_TITLE,
        fg=colors.ACCENT_GREEN,
        bg=colors.BG,
    ).pack(pady=(18, 10))

    text_widget = tk.Text(
        modal,
        width=64,
        height=16,
        font=fonts.MODAL_BODY,
        bg=colors.BG_PANEL,
        fg=colors.TEXT_PRIMARY,
        relief=tk.FLAT,
        padx=14,
        pady=12,
        wrap=tk.WORD,
    )
    text_widget.pack(padx=20, pady=(0, 12))

    round_num = 1
    for i, choice in enumerate(game_state.decision_path, start=1):
        round_data = game_data["rounds"].get(round_num)
        if round_data is None:
            break
        choice_data = round_data["choices"][choice]
        text_widget.insert(
            tk.END,
            f"Round {round_num} -- {round_data['title']}: chose {choice}) "
            f"{choice_data['text']}\n\n",
        )
        leads_to = choice_data["leads_to"]
        if leads_to.startswith("round_"):
            round_num = int(leads_to.split("_")[1])
        else:
            ending = game_data["endings"][leads_to]
            text_widget.insert(tk.END, f"-> Ending reached: {ending['name']} ({leads_to})\n")

    text_widget.config(state=tk.DISABLED)

    tk.Button(
        modal,
        text="Close",
        command=modal.destroy,
        font=fonts.BUTTON,
        bg=colors.BUTTON_BG,
        fg=colors.TEXT_PRIMARY,
        relief=tk.FLAT,
        padx=14,
        pady=6,
        cursor="hand2",
    ).pack(pady=(0, 18))

    _center_on_parent(modal, parent, 560, 480)
    modal.grab_set()
