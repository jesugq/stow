#!/usr/bin/env python3

# Copilot CLI TextSpinner animation (1.0.x)
import math
import os
import sys

sys.path.insert(0, os.path.expanduser("~/.script"))
from thinking import run

INTERVAL = 0.09
TICK_STEP = 3
PAUSE = 0.3
PULSE_FRAMES = "●◉◎○◎◉"
# Copilot's "default" theme delegates these colors to the terminal palette.
BRAND = "\033[35m"
BRAND_BRIGHT = "\033[95m"
GRADIENT = (
    BRAND_BRIGHT,
    BRAND_BRIGHT,
    BRAND,
    BRAND,
    BRAND,
    BRAND,
    BRAND_BRIGHT,
    BRAND_BRIGHT,
)
RESET = "\033[0m"


def render(elapsed, label):
    ticks = int(elapsed / INTERVAL) * TICK_STEP
    gradient_length = len(GRADIENT)
    shimmer_length = len(label) + gradient_length
    pause_ticks = round(PAUSE / INTERVAL) * TICK_STEP
    cycle = math.ceil((shimmer_length + pause_ticks) / TICK_STEP) * TICK_STEP
    position = min(ticks % cycle, shimmer_length)
    frame_index = (ticks // TICK_STEP) % len(PULSE_FRAMES)
    sweep_width = max((gradient_length - 1) * 2, 1)
    sweep = (ticks // TICK_STEP) % sweep_width
    color_index = sweep if sweep < gradient_length else sweep_width - sweep

    text = []
    for index, character in enumerate(label):
        gradient_index = position - index
        color = GRADIENT[gradient_index] if 0 <= gradient_index < gradient_length else BRAND
        text.append(f"{color}{character}")
    return f"{GRADIENT[color_index]}{PULSE_FRAMES[frame_index]}{RESET} " + "".join(text) + RESET


run(render, INTERVAL)
