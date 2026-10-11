import os
import random
import re
import select
import shutil
import signal
import sys
import termios
import time
import tty
from collections import deque

_input_fd = None
_input_settings = None
_ansi = re.compile(r"\033\[[0-?]*[ -/]*[@-~]")
_teammate = re.compile(r"\{\{TEAMMATE\}\}")

# Halfway between the old faint gray (120, 120, 128) and Ryuuko foreground.
DIM = "\033[38;2;178;178;182m"
RESET = "\033[0m"
# Halfway between the original 0.18s/word pace and the fast 0.016s stream.
WORD_INTERVAL = 0.098
BREAK_INTERVAL = 0.12
# Status verbs ("Thinking", "Writing", ...) hold for about ten seconds.
LABEL_INTERVAL = 10
# The status band is a blank row, the centered line, and a blank row.
STATUS_ROWS = 3


def tokenize(text):
    """Words, with None marking a blank line so paragraphs stay separated."""
    tokens = []
    for line in text.splitlines():
        words = line.split()
        if words:
            tokens.extend(words)
        else:
            tokens.append(None)
    while tokens and tokens[0] is None:
        tokens.pop(0)
    while tokens and tokens[-1] is None:
        tokens.pop()
    return tokens


def load_text(path):
    try:
        with open(os.path.expanduser(path), encoding="utf-8") as handle:
            return handle.read()
    except OSError as exc:
        name = exc.filename or path
        sys.stderr.write(f"thinking: {name}: {exc.strerror}\n")
        raise SystemExit(1) from exc


def load_lines(path, kind):
    lines = [line.strip() for line in load_text(path).splitlines() if line.strip()]
    if not lines:
        sys.stderr.write(f"thinking: {path}: no {kind}\n")
        raise SystemExit(1)
    return lines


def parse_invocation():
    """Positional args, same shape as the afk pane commands.

    script.py MESSAGES NAMES REASONING

    MESSAGES is a text file with one status line per row. NAMES is the same
    shape, one person per row. REASONING is the dimmed text file. Each
    Each {{TEAMMATE}} is replaced, as it is printed, with the next name.
    Messages, names, and reasoning each start on a random line and loop.
    """
    args = sys.argv[1:]
    if len(args) < 3:
        sys.stderr.write("thinking: messages, names, and reasoning files are expected\n")
        raise SystemExit(1)
    messages = load_lines(args[0], "messages")
    names = load_lines(args[1], "names")
    text = load_text(args[2])
    if not tokenize(text):
        sys.stderr.write(f"thinking: {args[2]}: no reasoning\n")
        raise SystemExit(1)
    return messages, names, text


def rotate_to_random_line(text):
    """Begin at a random non-empty line, then continue through the file."""
    lines = text.splitlines()
    filled = [index for index, line in enumerate(lines) if line.strip()]
    if len(filled) <= 1:
        return text
    start = random.choice(filled)
    return "\n".join(lines[start:] + lines[:start])


class Messages:
    def __init__(self, lines):
        self.lines = lines
        self.start = random.randrange(len(self.lines))

    def current(self, elapsed):
        index = (self.start + int(elapsed / LABEL_INTERVAL)) % len(self.lines)
        return self.lines[index]


def reasoning_limit(height):
    return max(height - STATUS_ROWS, 0)


class Reasoning:
    def __init__(self, source, names):
        self.tokens = tokenize(rotate_to_random_line(source))
        self.names = names
        self.name_at = random.randrange(len(names))
        self.max_lines = 1
        self.index = 0
        self.pending = deque()
        self.emitted = []
        self.next_at = 0.0
        self.limit = 8
        # Wrapped rows for the tokens already in self.emitted. Rebuilt only
        # when the width changes; a new word rewraps the last line only.
        self.rows = None
        self.starts = []
        self.layout_limit = None
        self.laid_out = 0

    def advance(self, elapsed, width, max_lines):
        self.limit = max(width - 2, 8)
        self.max_lines = max(0, max_lines)
        emitted = 0
        while self.max_lines > 0 and elapsed >= self.next_at and emitted < 4:
            self._emit()
            emitted += 1
        self._ensure()
        self._trim()
        return self.visible()

    def _next_name(self):
        """Next person, walking forward from a random line and wrapping."""
        name = self.names[self.name_at % len(self.names)]
        self.name_at += 1
        return name

    def _fill_teammate(self, token):
        """Swap each {{TEAMMATE}} for the next name. A suffix stays on the last word."""
        if "{{TEAMMATE}}" not in token:
            return [token]
        filled = _teammate.sub(lambda _match: self._next_name(), token)
        return filled.split() or [token]

    def _emit(self):
        if self.pending:
            self.emitted.append(self.pending.popleft())
            self.next_at += WORD_INTERVAL
            return
        token = self.tokens[self.index % len(self.tokens)]
        cycling = self.index > 0 and self.index % len(self.tokens) == 0
        self.index += 1
        if cycling and (not self.emitted or self.emitted[-1] is not None):
            self.emitted.append(None)
        if token is None:
            self.emitted.append(None)
            self.next_at += BREAK_INTERVAL
            return
        pieces = self._fill_teammate(token)
        self.emitted.append(pieces[0])
        self.pending.extend(pieces[1:])
        self.next_at += WORD_INTERVAL

    def _hyphenate(self, token):
        """Break a token that cannot fit on one line, marking each cut with '-'."""
        limit = max(self.limit, 2)
        if len(token) <= limit:
            return [token]
        pieces = []
        while len(token) > limit:
            pieces.append(token[: limit - 1] + "-")
            token = token[limit - 1 :]
        if token:
            pieces.append(token)
        return pieces

    def _layout(self, tokens):
        """Wrap tokens. Each row records the emitted token that starts it."""
        rows = []
        starts = []
        current = ""
        current_start = None

        def flush():
            nonlocal current, current_start
            if current_start is None:
                return
            rows.append(current)
            starts.append(current_start)
            current = ""
            current_start = None

        for index, token in enumerate(tokens):
            if token is None:
                flush()
                rows.append("")
                starts.append(index)
                continue
            for piece in self._hyphenate(token):
                if current and len(current) + 1 + len(piece) > self.limit:
                    flush()
                if current:
                    current = f"{current} {piece}"
                else:
                    current = piece
                    current_start = index
        flush()
        return rows, starts

    def _ensure(self):
        """Wrap anything not already cached. Width changes reflow the kept tokens."""
        if self.rows is not None and self.layout_limit == self.limit and self.laid_out == len(self.emitted):
            return
        if (
            self.rows is not None
            and self.layout_limit == self.limit
            and self.starts
            and self.laid_out < len(self.emitted)
        ):
            # The last row may still have room, so rebuild from the token that opened it.
            cut = self.starts[-1]
            while self.starts and self.starts[-1] == cut:
                self.starts.pop()
                self.rows.pop()
            added, added_starts = self._layout(self.emitted[cut:])
            self.rows.extend(added)
            self.starts.extend(index + cut for index in added_starts)
            self.laid_out = len(self.emitted)
            return
        self.rows, self.starts = self._layout(self.emitted)
        self.layout_limit = self.limit
        self.laid_out = len(self.emitted)

    def _trim(self):
        # Only the rows on screen are kept. Their original tokens stay so a
        # narrower pane can rehyphenate; lines that have scrolled off are gone.
        keep = self.max_lines
        if keep <= 0 or self.rows is None or len(self.rows) <= keep:
            return
        cut = self.starts[len(self.rows) - keep]
        if cut <= 0:
            return
        del self.emitted[:cut]
        first = 0
        while first < len(self.starts) and self.starts[first] < cut:
            first += 1
        self.rows = self.rows[first:]
        self.starts = [index - cut for index in self.starts[first:]]
        self.laid_out = len(self.emitted)

    def visible(self):
        if self.max_lines <= 0 or not self.rows:
            return []
        return self.rows[-self.max_lines :]


class Display:
    """Redraws only the rows that changed. A size change clears the pane once."""

    def __init__(self):
        self.cells = {}
        self.size = None
        self.above = None
        self.left = None
        self.start = None

    def render(self, text, above, column, size):
        width = size.columns
        height = size.lines
        visible = _ansi.sub("", text)
        padding = max((width - len(visible)) // 2, 0)
        room = reasoning_limit(height)
        if len(above) > room:
            above = above[-room:]
        if column <= 0:
            column = max((len(_ansi.sub("", line)) for line in above), default=0)
        left = max((width - min(column, width)) // 2, 0)
        # Middle row of the bottom 3-line band. Reasoning sits above that band.
        status_row = max(height - (STATUS_ROWS // 2) - 1, 0)
        start = status_row - 1 - len(above)
        status_at = status_row + 1
        status_cell = f"{' ' * padding}{text}" if 1 <= status_at <= height else None
        # Spinner frames change constantly; the paragraph usually does not.
        if (
            self.size == (width, height)
            and self.above == above
            and self.left == left
            and self.start == start
        ):
            if status_cell is not None and self.cells.get(status_at) != status_cell:
                self.cells[status_at] = status_cell
                return f"\033[{status_at};1H\033[2K{status_cell}"
            return ""
        cells = {}
        pad = " " * left
        for offset, line in enumerate(above):
            row = start + offset + 1
            if row < 1 or row > height:
                continue
            cells[row] = f"{pad}{DIM}{line}{RESET}" if line else ""
        if status_cell is not None:
            cells[status_at] = status_cell
        full = self.size != (width, height)
        parts = []
        if full:
            parts.append("\033[2J\033[H")
            for row in sorted(cells):
                content = cells[row]
                if content:
                    parts.append(f"\033[{row};1H{content}")
        else:
            for row in sorted(set(self.cells) | set(cells)):
                content = cells.get(row)
                if content is None:
                    parts.append(f"\033[{row};1H\033[2K")
                    continue
                if self.cells.get(row) != content:
                    parts.append(f"\033[{row};1H\033[2K{content}")
        self.cells = cells
        self.size = (width, height)
        self.above = above
        self.left = left
        self.start = start
        return "".join(parts)


def enable_quit():
    global _input_fd, _input_settings
    try:
        _input_fd = os.open("/dev/tty", os.O_RDONLY)
        _input_settings = termios.tcgetattr(_input_fd)
        tty.setcbreak(_input_fd)
    except (OSError, termios.error):
        if _input_fd is not None:
            os.close(_input_fd)
        _input_fd = None
        _input_settings = None


def _read_byte(timeout):
    ready, _, _ = select.select([_input_fd], [], [], timeout)
    if not ready:
        return None
    return os.read(_input_fd, 1) or None


def _discard_terminal_reply(kind):
    """Eat an OSC or CSI sequence so a color query is not a keypress."""
    end = time.monotonic() + 0.05
    if kind == b"]":
        buf = b""
        while time.monotonic() < end:
            ch = _read_byte(max(0.0, end - time.monotonic()))
            if ch is None:
                return
            buf += ch
            if buf.endswith(b"\a") or buf.endswith(b"\033\\"):
                return
        return
    while time.monotonic() < end:
        ch = _read_byte(max(0.0, end - time.monotonic()))
        if ch is None:
            return
        if 0x40 <= ch[0] <= 0x7E:
            return


def _click(button, released):
    """A mouse button press. Wheel and drag reports are not clicks."""
    if released or button & 32 or button >= 64:
        return False
    return (button & 3) < 3


def _sgr_click():
    """SGR mouse report: CSI < button ; x ; y M (press) or m (release)."""
    buf = b""
    end = time.monotonic() + 0.05
    while time.monotonic() < end and len(buf) < 48:
        ch = _read_byte(max(0.0, end - time.monotonic()))
        if ch is None:
            return False
        if ch in (b"M", b"m"):
            try:
                button = int(buf.split(b";", 1)[0])
            except ValueError:
                return False
            return _click(button, ch == b"m")
        buf += ch
    return False


def _x10_click():
    """Legacy mouse report: CSI M, then button, column, and row bytes."""
    payload = b""
    end = time.monotonic() + 0.05
    while len(payload) < 3 and time.monotonic() < end:
        ch = _read_byte(max(0.0, end - time.monotonic()))
        if ch is None:
            return False
        payload += ch
    if len(payload) < 3:
        return False
    return _click(payload[0] - 32, False)


def quit_requested():
    if _input_fd is None:
        return False
    try:
        key = _read_byte(0)
        if key is None:
            return False
        if key.lower() == b"q":
            return True
        if key != b"\033":
            return False
        nxt = _read_byte(0.01)
        if nxt is None:
            return True
        if nxt == b"]":
            # OSC replies (Codex color queries) are not a quit key.
            _discard_terminal_reply(nxt)
            return False
        if nxt != b"[":
            return True
        third = _read_byte(0.01)
        if third == b"<":
            return _sgr_click()
        if third == b"M":
            return _x10_click()
        if third is None:
            return False
        if not (0x40 <= third[0] <= 0x7E):
            _discard_terminal_reply(b"[")
        return False
    except (OSError, termios.error):
        return False


def _drain_input():
    if _input_fd is None:
        return
    try:
        while _read_byte(0) is not None:
            pass
    except (OSError, termios.error):
        return


def restore_terminal(reset):
    # Drop mouse tracking before cooked mode, or the click leaks into the shell.
    sys.stdout.write("\033[?1006l\033[?1000l\033[?25h" + reset + "\n")
    sys.stdout.flush()
    _drain_input()
    if _input_fd is not None and _input_settings is not None:
        try:
            termios.tcsetattr(_input_fd, termios.TCSADRAIN, _input_settings)
        except (OSError, termios.error):
            pass
        os.close(_input_fd)
    os._exit(0)


def run(render, interval):
    messages, names, source = parse_invocation()
    status = Messages(messages)
    reasoning = Reasoning(source, names)
    display = Display()

    def restore(*_):
        restore_terminal(RESET)

    enable_quit()
    signal.signal(signal.SIGINT, restore)
    signal.signal(signal.SIGTERM, restore)
    hidden = "\033[?25l"
    if _input_fd is not None:
        # 1000 reports clicks; 1006 uses the SGR form tmux forwards.
        hidden += "\033[?1000h\033[?1006h"
    sys.stdout.write(hidden + "\n")
    sys.stdout.flush()
    start = time.monotonic()
    while True:
        if quit_requested():
            restore()
        elapsed = time.monotonic() - start
        size = shutil.get_terminal_size((80, 24))
        above = reasoning.advance(elapsed, size.columns, reasoning_limit(size.lines))
        frame = display.render(render(elapsed, status.current(elapsed)), above, reasoning.limit, size)
        if frame:
            sys.stdout.write(frame)
            sys.stdout.flush()
        time.sleep(interval)
