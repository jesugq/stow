#!/usr/bin/env python3

# Qwen Code CLI: reuses gemini-cli's GeminiSpinner.tsx verbatim (confirmed in
# GeminiRespondingSpinner.tsx) - default spinnerType 'dots', tinygradient
# cycling forward through the theme's Accent* colors every 4000ms, updated
# every 30ms. Colors below are qwen-dark.ts's Accent* values (GradientColors
# is a separate 2-stop array used only for the ASCII header banner).
import os
import sys

sys.path.insert(0, os.path.expanduser("~/.script"))
from thinking import run

FRAMES = list("⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏")
SPIN_MS = 0.08
INTERVAL = 0.03
CYCLE = 4.0
# qwen-dark.ts Accent* (AccentPurple -> Blue -> Cyan -> Green -> Yellow -> Red -> loop)
BRAND = [
    (210, 166, 255),  # AccentPurple #D2A6FF
    (57, 185, 230),   # AccentBlue   #39B9E6
    (149, 214, 203),  # AccentCyan   #95D6CB
    (170, 233, 76),   # AccentGreen  #AAE94C
    (255, 215, 0),    # AccentYellow #FFD700
    (242, 109, 120),  # AccentRed    #F26D78
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
