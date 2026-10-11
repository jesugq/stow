#!/usr/bin/env python3

# OpenCode TUI: verified against packages/tui/src/component/spinner.tsx.
# Frames/interval match the real ink-style dots spinner exactly. The
# component takes no gradient - its default color is theme.textMuted (a
# flat, terminal-background-derived gray), so there is no primary/accent
# color animation on this indicator.
import os
import sys

sys.path.insert(0, os.path.expanduser("~/.script"))
from thinking import run

FRAMES = list("⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏")
SPIN_MS = 0.08
# theme.textMuted approximation (generateMutedTextColor over a dark bg)
MUTED = (128, 128, 136)
reset = "\033[0m"


def rgb(color):
    return f"\033[38;2;{color[0]};{color[1]};{color[2]}m"


def render(elapsed, label):
    frame = FRAMES[int(elapsed / SPIN_MS) % len(FRAMES)]
    return f"{rgb(MUTED)}{frame} {label}{reset}"


run(render, SPIN_MS)
