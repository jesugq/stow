#!/usr/bin/env python3

# OpenCode TUI: verified against packages/tui/src/component/spinner.tsx.
# Frames/interval match the real ink-style dots spinner exactly. The
# component takes no gradient - its default color is theme.textMuted (a
# flat, terminal-background-derived gray), so there is no primary/accent
# color animation on this indicator.
FRAMES = list("⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏")
SPIN_MS = 0.08
INTERVAL = SPIN_MS
# theme.textMuted approximation (generateMutedTextColor over a dark bg)
MUTED = (128, 128, 136)
reset = "\033[0m"


def rgb(color):
    return f"\033[38;2;{color[0]};{color[1]};{color[2]}m"


def render(elapsed, label):
    frame = FRAMES[int(elapsed / SPIN_MS) % len(FRAMES)]
    return f"{rgb(MUTED)}{frame} {label}{reset}"


if __name__ == "__main__":
    from thinking_template import run

    run(render, INTERVAL)
