#!/usr/bin/env python3

# Antigravity CLI (agy): dots8 spinner + Gemini brand gradient
# Observed: ⣯ Thinking... / ⣽ Working... ; colors from gemini-cli darkTheme
import os
import sys

sys.path.insert(0, os.path.expanduser("~/.script"))
from thinking import run

FRAMES = list("⣾⣽⣻⢿⡿⣟⣯⣷")
SPIN_MS = 0.08
INTERVAL = 0.03
CYCLE = 4.0
# gemini-cli darkTheme Accent* (GeminiSpinner tinygradient)
BRAND = [
    (215, 175, 255),  # AccentPurple #D7AFFF
    (135, 175, 255),  # AccentBlue   #87AFFF
    (135, 215, 215),  # AccentCyan   #87D7D7
    (215, 255, 215),  # AccentGreen  #D7FFD7
    (255, 255, 175),  # AccentYellow #FFFFAF
    (255, 135, 175),  # AccentRed    #FF87AF
]
reset = "\033[0m"


def lerp(a, b, t):
    return tuple(int(x + (y - x) * t) for x, y in zip(a, b))


def gradient_at(elapsed):
    t = (elapsed % CYCLE) / CYCLE * len(BRAND)
    i = int(t) % len(BRAND)
    return lerp(BRAND[i], BRAND[(i + 1) % len(BRAND)], t - int(t))


def rgb(color):
    return f"\033[38;2;{color[0]};{color[1]};{color[2]}m"


def render(elapsed, label):
    color = gradient_at(elapsed)
    frame = FRAMES[int(elapsed / SPIN_MS) % len(FRAMES)]
    return f"{rgb(color)}{frame} {label}{reset}"


run(render, INTERVAL)
