#!/usr/bin/env python3

# ChatGPT: a large blue dot that breathes. A terminal cell cannot scale a
# glyph, so the inhale/exhale steps through three single-width filled circles
# of graded size from the Maple Mono NF (Nerd Font) glyph set:
#   U+EA71  smallest, 9x9 px at 18pt
#   U+25CF  middle, plain Unicode BLACK CIRCLE, 12x13 px
#   U+E39B  largest, 14x14 px
# The blue brightness swells with the size to make the breath read smoothly.
import math

PROVIDER = "ChatGPT"
FRAMES = [
    "\uea71",
    "\uea71",
    "\uea71",
    "●",
    "\ue39b",
    "\ue39b",
    "\ue39b",
    "●",
    "\uea71",
    "\uea71",
]
SPIN_MS = 0.16
INTERVAL = 0.05
CYCLE = len(FRAMES) * SPIN_MS
# Deep to bright azure; brightness peaks in the middle of the large frames.
BLUE_DIM = (30, 80, 160)
BLUE = (80, 165, 255)
reset = "\033[0m"


def lerp(a, b, t):
    return tuple(int(x + (y - x) * t) for x, y in zip(a, b))


def breath_at(elapsed):
    t = (elapsed % CYCLE) / CYCLE
    return 0.5 - 0.5 * math.cos(2 * math.pi * t)


def rgb(color):
    return f"\033[38;2;{color[0]};{color[1]};{color[2]}m"


def render(elapsed, label):
    label = f"{PROVIDER} is {label}"
    frame = FRAMES[int(elapsed / SPIN_MS) % len(FRAMES)]
    color = lerp(BLUE_DIM, BLUE, breath_at(elapsed))
    return f"{rgb(color)}{frame}{reset} {label}"


if __name__ == "__main__":
    from thinking_template import run

    run(render, INTERVAL)
