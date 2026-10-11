#!/usr/bin/env python3

# Claude Code: sparkle palindrome (Spinner.tsx) + dark theme claude / claudeShimmer
import os
import sys

sys.path.insert(0, os.path.expanduser("~/.script"))
from thinking import run

# getDefaultCharacters() (darwin) + reverse — Spinner.tsx SPINNER_FRAMES
BASE = ["·", "✢", "✱", "✶", "✻", "✽"]
FRAMES = BASE + BASE[::-1]
SPIN_MS = 0.12
INTERVAL = 0.05
CYCLE = 2.0
# darkTheme: claude rgb(215,119,87) / claudeShimmer rgb(235,159,127)
CLAUDE = (215, 119, 87)
SHIMMER = (235, 159, 127)
reset = "\033[0m"


def lerp(a, b, t):
    t = max(0.0, min(1.0, t))
    return tuple(int(x + (y - x) * t) for x, y in zip(a, b))


def gradient_at(elapsed):
    x = (elapsed % CYCLE) / CYCLE
    t = x * 2 if x < 0.5 else 2 - x * 2
    return lerp(CLAUDE, SHIMMER, t)


def rgb(color):
    return f"\033[38;2;{color[0]};{color[1]};{color[2]}m"


def render(elapsed, label):
    color = gradient_at(elapsed)
    frame = FRAMES[int(elapsed / SPIN_MS) % len(FRAMES)]
    return f"{rgb(color)}{frame} {label}{reset}"


run(render, INTERVAL)
