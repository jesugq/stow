#!/usr/bin/env python3

# Gemini: three-dot "sparkle" stadium wave. Each dot is one Braille cell whose
# dot travels through the four cell rows; adjacent dots stay at most two rows
# apart so the wave never tears. Braille (U+2801..U+2840) is plain Unicode, not
# Nerd Font, and is already used by the Antigravity and Cursor spinners.
# Colors: pure white dots, like the real Gemini spinner.
PROVIDER = "Gemini"
FRAMES = [
    "⠄⠁⠄",
    "⠄⠁⠂",
    "⡀⠂⠂",
    "⡀⠂⠁",
    "⡀⠄⠁",
    "⠄⠄⠂",
    "⠄⡀⠂",
    "⠂⡀⠄",
    "⠁⠄⠄",
    "⠁⠄⡀",
    "⠁⠂⡀",
    "⠂⠂⠄",
]
SPIN_MS = 0.12
INTERVAL = 0.05
WHITE = (255, 255, 255)
reset = "\033[0m"


def rgb(color):
    return f"\033[38;2;{color[0]};{color[1]};{color[2]}m"


def render(elapsed, label):
    label = f"{PROVIDER} is {label}"
    frame = FRAMES[int(elapsed / SPIN_MS) % len(FRAMES)]
    return f"{rgb(WHITE)}{frame}{reset} {label}"


if __name__ == "__main__":
    from thinking_template import run

    run(render, INTERVAL)
