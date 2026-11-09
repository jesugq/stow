#!/usr/bin/env python3

# Kilo Code TUI: footer activity indicator. The blocks comet comes from
# @opentui's spinner generator (width 8, bidirectional hold, 40ms/frame).
# Build agent uses theme secondary, which is purple on this terminal.
PROVIDER = "Kilo"
FRAME_MS = 0.04
INTERVAL = 0.04
THINKING_LENGTH = 8
HOLD_START = 30
HOLD_END = 9
TRAIL = 6
ACCENT = (168, 85, 247)
BACKGROUND = (15, 15, 15)
MIN_ALPHA = 0.3
FILLED = "\u25a0"
EMPTY = "\u2b1d"
reset = "\033[0m"


def trail_colors(accent):
    colors = []
    for index in range(TRAIL):
        if index == 0:
            alpha, boost = 1.0, 1.0
        elif index == 1:
            alpha, boost = 0.9, 1.15
        else:
            alpha, boost = 0.65 ** (index - 1), 1.0
        colors.append((tuple(min(255.0, c * boost) for c in accent), alpha))
    return colors


COLORS = trail_colors(ACCENT)
DEFAULT_ALPHA = 0.6
BACKWARD = THINKING_LENGTH - 1
FRAME_COUNT = THINKING_LENGTH + HOLD_END + BACKWARD + HOLD_START


def state(frame):
    if frame < THINKING_LENGTH:
        return frame, False, 0, 0, frame, THINKING_LENGTH, True
    if frame < THINKING_LENGTH + HOLD_END:
        return THINKING_LENGTH - 1, True, frame - THINKING_LENGTH, HOLD_END, 0, 0, True
    if frame < THINKING_LENGTH + HOLD_END + BACKWARD:
        moved = frame - THINKING_LENGTH - HOLD_END
        return THINKING_LENGTH - 2 - moved, False, 0, 0, moved, BACKWARD, False
    return 0, True, frame - THINKING_LENGTH - HOLD_END - BACKWARD, HOLD_START, 0, 0, False


def cell_index(frame, cell):
    active, holding, held, _held_total, moved, _moved_total, forward = state(frame)
    distance = active - cell if forward else cell - active
    if holding:
        return distance + held
    if 0 < distance < TRAIL:
        return distance
    return 0 if distance == 0 else -1


def fade(frame):
    _active, holding, held, held_total, moved, moved_total, _forward = state(frame)
    if holding and held_total > 0:
        progress = min(held / held_total, 1.0)
        return max(MIN_ALPHA, 1.0 - progress * (1.0 - MIN_ALPHA))
    if not holding and moved_total > 0:
        progress = min(moved / max(1, moved_total - 1), 1.0)
        return MIN_ALPHA + progress * (1.0 - MIN_ALPHA)
    return 1.0


def blend(color, alpha):
    return tuple(int(round(bg + (c - bg) * alpha)) for c, bg in zip(color, BACKGROUND))


def paint(frame):
    parts = []
    dim = DEFAULT_ALPHA * fade(frame)
    for cell in range(THINKING_LENGTH):
        index = cell_index(frame, cell)
        if 0 <= index < TRAIL:
            color, alpha = COLORS[index]
            glyph = FILLED
        else:
            color, alpha = ACCENT, dim
            glyph = EMPTY
        red, green, blue = blend(color, alpha)
        parts.append(f"\033[38;2;{red};{green};{blue}m{glyph}")
    return "".join(parts)


FRAMES = [paint(frame) for frame in range(FRAME_COUNT)]


def render(elapsed, label):
    label = f"{PROVIDER} is {label}"
    frame = FRAMES[int(elapsed / FRAME_MS) % len(FRAMES)]
    return f"{frame}{reset} {label}"


if __name__ == "__main__":
    from thinking_template import run

    run(render, INTERVAL)
