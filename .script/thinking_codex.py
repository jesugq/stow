#!/usr/bin/env python3

# Codex TUI: motion.rs activity_indicator + summary_shimmer.rs
import math
import os
import select
import sys
import termios
import time
import tty

sys.path.insert(0, os.path.expanduser("~/.script"))
from thinking import run


INTERVAL = 0.032


def blend(a, b, t):
    t = max(0.0, min(1.0, t))
    return tuple(int(x * t + y * (1.0 - t)) for x, y in zip(a, b))


def query_osc(code, timeout=0.15):
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        return None
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        # os.read, not sys.stdin.read: the text wrapper slurps the whole reply
        # into its buffer, select() then sees an empty fd, and the parse fails.
        # The leftover bytes later look like Escape and the animation exits.
        os.write(sys.stdout.fileno(), f"\033]{code};?\033\\".encode())
        buf = b""
        end = time.time() + timeout
        while time.time() < end:
            ready, _, _ = select.select([fd], [], [], max(0.0, end - time.time()))
            if not ready:
                break
            buf += os.read(fd, 1)
            if buf.endswith(b"\a") or buf.endswith(b"\033\\"):
                break
    except (termios.error, OSError):
        return None
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)
    text = buf.decode("latin1")
    marker = "rgb:"
    i = text.find(marker)
    if i < 0:
        return None
    parts = text[i + len(marker) :].split("\033", 1)[0].split("\a", 1)[0].split("/")
    if len(parts) != 3:
        return None
    try:
        return tuple(int(p, 16) >> 8 if len(p) > 2 else int(p, 16) for p in parts)
    except ValueError:
        return None


def rgb(color):
    return f"\033[38;2;{color[0]};{color[1]};{color[2]}m"


# GitHub Dark fallback when OSC 10/11 is unavailable
fg = query_osc(10) or (201, 209, 217)
bg = query_osc(11) or (13, 17, 23)
bold = "\033[1m"
reset = "\033[0m"


def shimmer_dot(elapsed):
    padding = 10
    period = 1 + padding * 2
    pos = int((elapsed % 2.0) / 2.0 * period)
    dist = abs((0 + padding) - pos)
    t = 0.5 * (1.0 + math.cos(math.pi * dist / 5.0)) if dist <= 5.0 else 0.0
    return f"{bold}{rgb(blend(bg, fg, t * 0.9))}•{reset}"


def summary_shimmer(elapsed, label):
    width = float(len(label))
    half = 5.0  # shimmer.rs: band_half_width is a fixed constant, not width-proportional
    position = (elapsed % 2.0) / 2.0 * (width + 2.0 * half) - half
    out = []
    for i, ch in enumerate(label):
        distance = min(abs((i + 0.5) - position) / half, 1.0)
        intensity = 0.5 * (1.0 + math.cos(math.pi * distance))
        out.append(f"{rgb(blend(fg, bg, 0.5 + 0.5 * intensity))}{ch}")
    return "".join(out) + reset


def render(elapsed, label):
    return f"{shimmer_dot(elapsed)} {summary_shimmer(elapsed, label)}"


run(render, INTERVAL)
