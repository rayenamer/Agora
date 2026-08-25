"""ASCII art rendering onto the Canvas sketch area."""

import tkinter as tk
from typing import Any, Dict

from utils import colors, fonts


def render_sketch(canvas: tk.Canvas, sketch_key: str, game_data: Dict[str, Any]) -> None:
    """Draw the ASCII art for sketch_key centered on the canvas."""
    sketch_text = game_data["sketches"].get(sketch_key, "")

    width = int(canvas["width"])
    height = int(canvas["height"])

    canvas.create_text(
        width // 2,
        height // 2,
        text=sketch_text,
        font=fonts.SKETCH,
        fill=colors.ACCENT_GREEN,
        anchor=tk.CENTER,
        justify=tk.LEFT,
    )
