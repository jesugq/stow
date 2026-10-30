#!/usr/bin/env python3

# Cursor CLI: verified against the shipped bundle (spinner-definitions.ts +
# app render tree). Frames/interval match exactly; the pending-turn indicator
# renders the spinner in plain ANSI green next to bold "Working" text -
# there is no orange/brand gradient on this indicator.
FRAMES = ["⠀⠞", "⠠⠜", "⠰⠰", "⠘⠤", "⠘⠆", "⠘⠣", "⠰⠳", "⠠⠛"]
SPIN_MS = 0.25
INTERVAL = 0.05
green = "\033[32m"
bold = "\033[1m"
reset = "\033[0m"


def render(elapsed, label):
    frame = FRAMES[int(elapsed / SPIN_MS) % len(FRAMES)]
    return f"{green}{frame}{reset} {bold}{label}{reset}"


if __name__ == "__main__":
    from thinking_common import run

    run(render, INTERVAL)
