import os
import random
import re
import select
import shutil
import signal
import subprocess
import sys
import termios
import time
import tty
import unicodedata

_input_fd = None
_input_settings = None
_ansi = re.compile(r"\033\[[0-?]*[ -/]*[@-~]")
_teammate = re.compile(r"\{\{TEAMMATE\}\}")
# Bold text with no color of its own, as in the cursor renderer.
# Replaced by OSC 10 when the terminal answers.
_DEFAULT_FG = (229, 229, 229)
# Real palette from OSC 4. Indexed fades stay on the SGR index until this
# arrives: xterm's stock color 5/13 is hot pink, and themes such as Ryuuko
# use those slots for a tan. Substituting the stock RGB paints that pink
# for the whole fade.
_PALETTE = None

# Halfway between the old faint gray (120, 120, 128) and Ryuuko foreground.
DIM_RGB = (178, 178, 182)
# Ryuuko's warmest ansi is khaki (#b1a990), so names use Oasis Mirage @thm_orange.
NAME_RGB = (248, 180, 113)
# Ryuuko's background. Replaced by the live terminal or tmux pane color.
_BG_FALLBACK = (0x2C, 0x39, 0x41)
_bg = _BG_FALLBACK
_osc_bg = None
_tmux_override = None
_bg_checked = 0.0
_osc_at = 0.0
RESET = "\033[0m"
# One character fades in, and one fades out, over this long.
# Sixteen characters share that window: the next character starts one share
# later. A quarter of the 1.4s letter fade, so the wave moves four times
# faster and a screen can fill.
FADE_CHARS = 16
LINE_FADE = 0.35
CHAR_STAGGER = LINE_FADE / FADE_CHARS
# afk runs drift with --duration 5. That hold starts the fade. Drift's
# default fade is 0.3s out and 0.3s in, and the next scene is swapped in
# at black. Later scenes count the fade-in toward the hold, so fades
# then begin hold-plus-one-fade apart.
DRIFT_HOLD = 5
DRIFT_FADE = 0.3
# Band under the reasoning: blank rows, the thinking line, blank rows.
# Two blanks above the line and two below.
STATUS_ROWS = 5
# Fade steps. Coarse enough that a row keeps one SGR for several frames,
# fine enough that the fade still reads as continuous. Steady rows sit on the last step.
_LEVELS = 16
_LEVEL_MAX = _LEVELS - 1
# How often to ask tmux which color it is painting. Spawning tmux on the
# animation clock is what hitches the fade.
_BG_EVERY = 5.0
_SYNC_ON = "\033[?2026h"
_SYNC_OFF = "\033[?2026l"

_lut_key = None
_lut_gen = 0
_dim_ramp = None
_name_ramp = None
_default_ramp = None
_ansi_ramp = None
_tc_cache = {}
_fade_cache = {}
_bg_force = False
_TC_CACHE_MAX = 2048
_FADE_CACHE_MAX = 64


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
    shape, one person per row. REASONING is the dimmed text file.
    Each {{TEAMMATE}} is replaced, as it is printed, with the next name,
    and that name is drawn in orange.
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


def presentation(elapsed):
    """Script slot and fade alpha. Alpha is 0 when lit and 1 at black.

    The slot changes at black, halfway through the fade, the way drift
    swaps scenes. One clock serves both so the swap and the alpha agree.
    Milliseconds keep the 0.3s boundary from landing on the wrong side.
    """
    hold = round(DRIFT_HOLD * 1000)
    fade = round(DRIFT_FADE * 1000)
    period = hold + fade
    ms = round(elapsed * 1000)
    if ms < hold:
        return 0, 0.0
    since = ms - hold
    cycle = since // period
    into = since - cycle * period
    if into < fade:
        return cycle, into / fade
    slot = cycle + 1
    if into < 2 * fade:
        return slot, 1.0 - (into - fade) / fade
    return slot, 0.0


def scene_slot(elapsed):
    return presentation(elapsed)[0]


def fade_alpha(elapsed):
    return presentation(elapsed)[1]


def _clamp_channel(value):
    if value < 0:
        return 0
    if value > 255:
        return 255
    return value


def _ramp(color):
    """16 SGR strings from the pane background to color. Ends are exact."""
    br, bg, bb = _bg
    cr = _clamp_channel(color[0])
    cg = _clamp_channel(color[1])
    cb = _clamp_channel(color[2])
    out = [None] * _LEVELS
    out[0] = f"\033[38;2;{br};{bg};{bb}m"
    out[_LEVEL_MAX] = f"\033[38;2;{cr};{cg};{cb}m"
    for step in range(1, _LEVEL_MAX):
        out[step] = (
            f"\033[38;2;{br + (cr - br) * step // _LEVEL_MAX};"
            f"{bg + (cg - bg) * step // _LEVEL_MAX};"
            f"{bb + (cb - bb) * step // _LEVEL_MAX}m"
        )
    return out


def _ensure_lut():
    """Rebuild blend ramps when the background, palette, or default ink changes."""
    global _lut_key, _lut_gen, _dim_ramp, _name_ramp, _default_ramp, _ansi_ramp
    key = (_bg, _PALETTE, _DEFAULT_FG)
    if key == _lut_key and _dim_ramp is not None:
        return
    _lut_key = key
    _lut_gen += 1
    _dim_ramp = _ramp(DIM_RGB)
    _name_ramp = _ramp(NAME_RGB)
    _default_ramp = _ramp(_DEFAULT_FG)
    _ansi_ramp = [_ramp(color) for color in _PALETTE] if _PALETTE is not None else None
    _tc_cache.clear()
    _fade_cache.clear()


def _tc_sgr(red, green, blue, level):
    red = _clamp_channel(red)
    green = _clamp_channel(green)
    blue = _clamp_channel(blue)
    if level >= _LEVEL_MAX:
        return f"\033[38;2;{red};{green};{blue}m"
    if level <= 0:
        return _default_ramp[0]
    key = (red, green, blue, level, _lut_gen)
    cached = _tc_cache.get(key)
    if cached is not None:
        return cached
    br, bg, bb = _bg
    sgr = (
        f"\033[38;2;{br + (red - br) * level // _LEVEL_MAX};"
        f"{bg + (green - bg) * level // _LEVEL_MAX};"
        f"{bb + (blue - bb) * level // _LEVEL_MAX}m"
    )
    if len(_tc_cache) >= _TC_CACHE_MAX:
        _tc_cache.clear()
    _tc_cache[key] = sgr
    return sgr


def _hex_rgb(text):
    text = text.strip().lstrip("#")
    if len(text) != 6:
        return None
    try:
        return tuple(int(text[i : i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        return None


def _style_bg(field):
    """A tmux style's background, or None when the pane uses the terminal color."""
    for piece in field.replace(",", " ").split():
        if not piece.startswith("bg="):
            continue
        value = piece[3:]
        if value in ("terminal", "default"):
            return None
        return _hex_rgb(value)
    return None


def _parse_osc_color(buf):
    text = buf.decode("latin1", "replace")
    marker = "rgb:"
    start = text.find(marker)
    if start < 0:
        return None
    parts = text[start + len(marker) :].split("\033", 1)[0].split("\a", 1)[0].split("/")
    if len(parts) != 3:
        return None
    try:
        return tuple(int(part, 16) >> 8 if len(part) > 2 else int(part, 16) for part in parts)
    except ValueError:
        return None


def _invalidate_background():
    global _bg_checked, _bg_force
    _bg_checked = 0.0
    _bg_force = True


def _note_osc(color):
    global _osc_bg, _osc_at, _bg
    _osc_bg = color
    _osc_at = time.monotonic()
    if _tmux_override is None and color != _bg:
        _bg = color


def _rgb_at(text, mark):
    raw = text[mark + 4 :]
    end = len(raw)
    for index, char in enumerate(raw):
        if char in ("\033", "\a", " ", '"'):
            end = index
            break
    parts = raw[:end].split("/")
    if len(parts) < 3:
        return None
    try:
        return tuple(int(part, 16) >> 8 if len(part) > 2 else int(part, 16) for part in parts[:3])
    except ValueError:
        return None


def _absorb_color_replies(buf):
    """OSC 10, 11, and 4 replies. Palette is applied only when all 16 arrived."""
    global _PALETTE, _DEFAULT_FG, _osc_bg, _osc_at
    text = buf.decode("latin1", "replace")
    found = {}
    start = 0
    while True:
        mark = text.find("rgb:", start)
        if mark < 0:
            break
        start = mark + 4
        color = _rgb_at(text, mark)
        if color is None:
            continue
        head = text[max(0, mark - 16) : mark]
        # "4;10;" / "4;11;" also end in those digits. Only a real OSC 10/11
        # marker counts, or palette slot 10 is stored as the foreground.
        if head.endswith("]10;"):
            if color != _DEFAULT_FG:
                _DEFAULT_FG = color
            continue
        if head.endswith("]11;"):
            _osc_bg = color
            _osc_at = time.monotonic()
            continue
        semi = head.rfind(";")
        if semi < 0:
            continue
        digits_end = semi
        digits_at = semi - 1
        while digits_at >= 0 and head[digits_at].isdigit():
            digits_at -= 1
        number = head[digits_at + 1 : digits_end]
        if not number or not head[: digits_at + 1].endswith("4;"):
            continue
        index = int(number)
        if 0 <= index <= 15:
            found[index] = color
    if len(found) == 16:
        _PALETTE = tuple(found[index] for index in range(16))


def _passthrough(seq):
    """Hand a query to the outer terminal. tmux answers OSC 4 from its own palette."""
    if os.environ.get("TMUX"):
        return b"\033Ptmux;\033" + seq + b"\033\\"
    return seq


def _query_colors(timeout):
    """One burst for foreground, background, and the 16 ANSI slots.

    Return as soon as the replies go quiet. Sitting on the full timeout
    freezes the first frames, which is when a half-drawn spinner flashes.
    """
    if _input_fd is None:
        return
    parts = [b"\033]10;?\033\\", b"\033]11;?\033\\"]
    parts.extend(f"\033]4;{index};?\033\\".encode() for index in range(16))
    payload = _passthrough(b"".join(parts))
    try:
        os.write(sys.stdout.fileno(), payload)
        sys.stdout.flush()
    except OSError:
        return
    buf = bytearray()
    deadline = time.monotonic() + timeout
    found = 0
    while len(buf) < 8192:
        now = time.monotonic()
        if now >= deadline:
            break
        char = _read_byte(min(deadline - now, 0.03 if not buf else 0.006))
        if char is None:
            break
        buf += char
        if char == b":" and buf[-4:] == b"rgb:":
            found += 1
            if found >= 18:
                deadline = min(deadline, time.monotonic() + 0.008)
    if buf:
        _absorb_color_replies(bytes(buf))


_palette_tries = 0


def _tmux_pane_bg():
    """Color tmux paints behind this pane, or None when that is the terminal.

    A slow tmux keeps the last answer. Dropping it would repaint every fade
    against the fallback background for one frame.
    """
    if not os.environ.get("TMUX"):
        return None
    try:
        raw = subprocess.check_output(
            [
                "tmux",
                "display-message",
                "-p",
                "#{pane_active}|#{E:window-style}|#{E:window-active-style}",
            ],
            stderr=subprocess.DEVNULL,
            timeout=0.05,
        )
    except subprocess.TimeoutExpired:
        return _tmux_override
    except (OSError, subprocess.SubprocessError):
        return _tmux_override
    parts = raw.decode("utf-8", "replace").strip().split("|", 2)
    if len(parts) != 3:
        return None
    return _style_bg(parts[2] if parts[0] == "1" else parts[1])


def _refresh_background(now, block=False):
    """Follow the pane background. Unfocused tmux panes use window-style.

    The palette and OSC colors are read at startup and when focus changes.
    Polling them on the frame clock stalls the fade and feeds the terminal
    queries that show up as a one-frame color glitch.
    """
    global _bg, _bg_checked, _tmux_override, _bg_force, _palette_tries
    if not block and not _bg_force and now - _bg_checked < _BG_EVERY:
        return
    _bg_checked = now
    force = block or _bg_force
    _bg_force = False
    if os.environ.get("TMUX"):
        _tmux_override = _tmux_pane_bg()
    if _input_fd is not None and (force or _palette_tries < 1):
        _palette_tries += 1
        _query_colors(0.12 if block else 0.04)
    if _tmux_override is not None:
        if _tmux_override != _bg:
            _bg = _tmux_override
        return
    if _osc_bg is not None and _osc_bg != _bg:
        _bg = _osc_bg


def _level(amount):
    if amount <= 0.0:
        return 0
    if amount >= 1.0:
        return _LEVEL_MAX
    return int(amount * _LEVEL_MAX + 0.5)


def _emit_sgr(out, params, level):
    """Rewrite one SGR. True/False is whether a foreground remains.

    Indexed colors stay indexed until OSC 4 has the real palette. Mapping
    them through xterm's stock magenta is what flashes pink.
    256-color 38;5 stays one sequence. Splitting it would emit SGR 5.
    """
    if params == "" or params == "0":
        out.append("\033[0m")
        return False
    try:
        codes = [int(part) if part else 0 for part in params.split(";")]
    except ValueError:
        out.append("\033[")
        out.append(params)
        out.append("m")
        return None
    colored = None
    plain = []
    index = 0
    ramp = _ansi_ramp

    def flush_plain():
        if not plain:
            return
        out.append("\033[")
        out.append(";".join(plain))
        out.append("m")
        plain.clear()

    while index < len(codes):
        code = codes[index]
        if code == 0:
            flush_plain()
            out.append("\033[0m")
            colored = False
            index += 1
            continue
        if code == 39:
            flush_plain()
            out.append("\033[39m")
            colored = False
            index += 1
            continue
        if code == 38 and index + 4 < len(codes) and codes[index + 1] == 2:
            flush_plain()
            out.append(_tc_sgr(codes[index + 2], codes[index + 3], codes[index + 4], level))
            colored = True
            index += 5
            continue
        if 30 <= code <= 37 or 90 <= code <= 97:
            flush_plain()
            slot = code - 30 if code <= 37 else code - 82
            if ramp is not None:
                out.append(ramp[slot][level])
            else:
                out.append(f"\033[{code}m")
            colored = True
            index += 1
            continue
        plain.append(str(code))
        index += 1
    flush_plain()
    return colored


def _fade_uncached(text, level):
    default = _default_ramp[level]
    out = []
    known = False
    n = len(text)
    i = 0
    while i < n:
        if text[i] != "\033" or i + 1 >= n or text[i + 1] != "[":
            j = text.find("\033", i)
            if j < 0:
                j = n
            if not known:
                out.append(default)
                known = True
            out.append(text[i:j])
            i = j
            continue
        k = i + 2
        while k < n:
            char = text[k]
            if char == "m":
                break
            if char != ";" and (char < "0" or char > "9"):
                k = -1
                break
            k += 1
        else:
            k = -1
        if k < 0 or k >= n or text[k] != "m":
            if not known:
                out.append(default)
                known = True
            out.append(text[i])
            i += 1
            continue
        colored = _emit_sgr(out, text[i + 2 : k], level)
        if colored is not None:
            known = colored
        i = k + 1
    return "".join(out)


def fade_ansi(text, alpha):
    """Fade foregrounds toward the pane background. Alpha 1 draws nothing."""
    if not text or alpha <= 0.0:
        return text
    if alpha >= 1.0:
        return ""
    level = _level(1.0 - alpha)
    if level <= 0:
        return ""
    _ensure_lut()
    key = (text, level, _lut_gen)
    cached = _fade_cache.get(key)
    if cached is not None:
        return cached
    faded = _fade_uncached(text, level)
    if len(_fade_cache) >= _FADE_CACHE_MAX:
        _fade_cache.clear()
    _fade_cache[key] = faded
    return faded


class Messages:
    def __init__(self, lines):
        self.lines = lines
        self.start = random.randrange(len(self.lines))

    def current(self, elapsed):
        index = (self.start + scene_slot(elapsed)) % len(self.lines)
        return self.lines[index]


def band_rows(height):
    """Odd height for the bottom band, so the thinking line stays centered."""
    rows = STATUS_ROWS
    if height < 1:
        return 1
    if rows > height:
        rows = height
    if rows % 2 == 0:
        rows -= 1
    if rows < 1:
        return 1
    return rows


def reasoning_limit(height):
    return max(height - band_rows(height), 0)


def _tick(elapsed):
    """Character clock. One tick is one share of the fade."""
    if elapsed <= 0.0:
        return 0
    return int(elapsed / CHAR_STAGGER)


def _flatten(pieces):
    """Visible characters, and whether each one is a name.

    Spaces inside a same-color run keep that color, matching a fully lit line.
    The result is built once per row and reused for every tick after that.
    """
    chars = []
    flags = bytearray()
    group_name = False
    started = False
    mark = b"\1"
    plain = b"\0"
    for text, is_name in pieces:
        if started:
            chars.append(" ")
            flags.append(1 if is_name and is_name == group_name else 0)
        started = True
        group_name = is_name
        chars.append(text)
        flags.extend(mark * len(text) if is_name else plain * len(text))
    return "".join(chars), bytes(flags)


def _attach(row, tick):
    """Cache the flat characters for a row born at this tick. Returns the count."""
    pieces = row["pieces"]
    if pieces:
        text, flags = _flatten(pieces)
    else:
        text = ""
        flags = b""
    row["text"] = text
    row["flags"] = flags
    row["n"] = len(text)
    row["tick"] = tick
    row.pop("draw", None)
    row.pop("key", None)
    row.pop("full", None)
    row.pop("out_tick", None)
    return row["n"]


def _render_wave(text, flags, birth, out_tick, now):
    """Paint letters that have started. Level 0 is skipped, not drawn dim.

    A background-colored glyph still rasterizes, and that fringe is the pink
    flash. Finished letters share one SGR per run. Only the 16-character
    wave carries a different level per letter.
    """
    dim = _dim_ramp
    name = _name_ramp
    full = _LEVEL_MAX
    span = FADE_CHARS
    n = len(text)
    parts = []
    buf = []
    buf_level = -1
    buf_name = 0

    def flush():
        nonlocal buf_level
        if not buf:
            return
        if buf_level > 0:
            parts.append(name[buf_level] if buf_name else dim[buf_level])
            parts.append("".join(buf))
        else:
            parts.append("".join(buf))
        buf.clear()
        buf_level = -1

    # Letters born at least one full fade ago are one color, unless leaving.
    stable = 0
    if out_tick is None:
        stable = now - birth - span
        if stable > n:
            stable = n
        if stable < 0:
            stable = 0
        index = 0
        while index < stable:
            flag = flags[index]
            end = index + 1
            while end < stable and flags[end] == flag:
                end += 1
            parts.append(name[full] if flag else dim[full])
            parts.append(text[index:end])
            index = end
    else:
        index = 0

    while index < n:
        age = now - birth - index
        if age <= 0:
            break
        if age > span:
            level = full
        else:
            level = (age * full + (span >> 1)) // span
            if level < 1:
                level = 1
        if out_tick is not None:
            gone = now - out_tick - index
            if gone > span:
                level = 0
            elif gone > 0:
                remain = span - gone + 1
                level = level * remain // span
                if level < 1:
                    level = 1
        if level <= 0:
            if buf_level != 0:
                flush()
                buf_level = 0
                buf_name = 0
            buf.append(" ")
            index += 1
            continue
        flag = flags[index]
        if buf and (buf_level != level or buf_name != flag):
            flush()
        buf_level = level
        buf_name = flag
        buf.append(text[index])
        index += 1
    flush()
    return "".join(parts)


def _line_for(row, now):
    """Cached line. Unchanged ticks return the same string object."""
    n = row.get("n", 0)
    if n <= 0:
        return ""
    birth = row["tick"]
    out_tick = row.get("out_tick")
    gen = _lut_gen
    if out_tick is None and now >= birth + n + FADE_CHARS:
        if row.get("full") and row.get("gen") == gen:
            return row["draw"]
        draw = _render_wave(row["text"], row["flags"], birth, None, birth + n + FADE_CHARS)
        row["draw"] = draw
        row["gen"] = gen
        row["full"] = True
        row["key"] = None
        return draw
    key = (now, out_tick, gen)
    if row.get("key") == key:
        return row["draw"]
    draw = _render_wave(row["text"], row["flags"], birth, out_tick, now)
    row["draw"] = draw
    row["key"] = key
    row["full"] = False
    row["gen"] = gen
    return draw


class Reasoning:
    def __init__(self, source, names):
        self.tokens = tokenize(rotate_to_random_line(source))
        self.names = names
        self.name_at = random.randrange(len(names))
        self.max_lines = 1
        self.index = 0
        self.pending = []
        self.next_tick = 0
        self.limit = 8
        self.rows = []
        self.next_row_id = 0
        self.layout_limit = None

    def advance(self, elapsed, width, max_lines):
        limit = max(width - 2, 8)
        self.max_lines = max(0, max_lines)
        if self.layout_limit != limit:
            self.limit = limit
            if self.layout_limit is not None:
                self._reflow()
            else:
                self.layout_limit = limit
        # A blank row does not hold the clock. It appears with the line
        # that follows. Text rows spend one tick per character.
        now = _tick(elapsed)
        blanks = 0
        while self.max_lines > 0 and now >= self.next_tick and blanks < 32:
            row = self._take_complete_row(self.next_tick, pull=True)
            if row is None:
                break
            count = _attach(row, self.next_tick)
            self.rows.append(row)
            if count:
                self.next_tick += count
                break
            blanks += 1
        self._trim()
        return self.visible(now)

    def _next_name(self):
        """Next person, walking forward from a random line and wrapping."""
        name = self.names[self.name_at % len(self.names)]
        self.name_at += 1
        return name

    def _fill_teammate(self, token):
        """Swap each {{TEAMMATE}} for the next name. A suffix stays on the last word.

        Each piece is (text, is_name). Only the substituted name is marked.
        """
        if "{{TEAMMATE}}" not in token:
            return [(token, False)]
        filled = _teammate.sub(lambda _match: self._next_name(), token)
        words = filled.split() or [token]
        return [(word, True) for word in words]

    def _pull_token(self):
        token = self.tokens[self.index % len(self.tokens)]
        cycling = self.index > 0 and self.index % len(self.tokens) == 0
        self.index += 1
        if cycling:
            self.pending.append(None)
        if token is None:
            self.pending.append(None)
            return
        self.pending.extend(self._fill_teammate(token))

    def _seal(self, pieces, born):
        row = {"pieces": pieces, "born": born, "id": self.next_row_id}
        self.next_row_id += 1
        return row

    def _take_complete_row(self, born, pull):
        """The next full row. A row ends when the next word would wrap, or at a break.

        pull is false while reflowing text already on screen, so a shortfall
        stays pending instead of reading further into the file.
        """
        pieces = []
        length = 0
        while True:
            if not self.pending:
                if not pull:
                    if pieces:
                        return self._seal(pieces, born)
                    return None
                self._pull_token()
            item = self.pending[0]
            if item is None:
                self.pending.pop(0)
                if pieces:
                    self.pending.insert(0, None)
                    return self._seal(pieces, born)
                return self._seal([], born)
            text, is_name = item
            parts = self._hyphenate(text)
            if pieces and length + 1 + len(parts[0]) > self.limit:
                return self._seal(pieces, born)
            self.pending.pop(0)
            for index, part in enumerate(parts):
                extra = len(part) if not pieces else 1 + len(part)
                if pieces and length + extra > self.limit:
                    self.pending[:0] = [(rest, is_name) for rest in parts[index:]]
                    return self._seal(pieces, born)
                pieces.append((part, is_name))
                length += extra

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

    def _reflow(self):
        """Rewrap the rows on screen after the pane width changes."""
        items = []
        for row in self.rows:
            if row["pieces"]:
                items.extend(row["pieces"])
            else:
                items.append(None)
        items.extend(self.pending)
        shown_end = None
        for row in self.rows:
            count = row.get("n", 0)
            if count:
                shown_end = row["tick"] + count
        self.pending = items
        self.rows = []
        built = []
        while self.pending:
            row = self._take_complete_row(0, pull=False)
            if row is None:
                break
            built.append(row)
        total = 0
        for row in built:
            total += len(_flatten(row["pieces"])[0]) if row["pieces"] else 0
        tick = 0
        if shown_end is not None:
            tick = shown_end - total
            if tick < 0:
                tick = 0
        for row in built:
            count = _attach(row, tick)
            if count:
                tick += count
        if self.next_tick < tick:
            self.next_tick = tick
        self.rows = built
        self.layout_limit = self.limit

    def _trim(self):
        # Lines that have scrolled off are gone.
        extra = len(self.rows) - self.max_lines
        if self.max_lines > 0 and extra > 0:
            del self.rows[:extra]

    def _sync_fade_out(self, now):
        """Walk a 16-character fade off the top once the screen is full.

        The top row stays until its last letter has finished, and the wave
        continues into the rows under it so letters leave one at a time.
        """
        if self.max_lines < 2 or len(self.rows) < self.max_lines:
            return
        origin = len(self.rows) - self.max_lines
        rows = self.rows
        cursor = None
        first = True
        for index in range(origin, len(rows)):
            row = rows[index]
            count = row.get("n", 0)
            if count <= 0:
                continue
            if first:
                if "out_tick" not in row:
                    row["out_tick"] = now
                finish = row["out_tick"] + count + FADE_CHARS
                if self.next_tick < finish:
                    self.next_tick = finish
                cursor = row["out_tick"] + count
                first = False
                continue
            if "out_tick" not in row:
                if now < cursor:
                    break
                row["out_tick"] = cursor
            cursor = row["out_tick"] + count

    def visible(self, now):
        if self.max_lines <= 0 or not self.rows:
            return []
        self._sync_fade_out(now)
        _ensure_lut()
        rows = self.rows
        start = len(rows) - self.max_lines
        if start < 0:
            start = 0
        line_for = _line_for
        return [line_for(rows[index], now) for index in range(start, len(rows))]


def _char_cols(char):
    code = ord(char)
    if code < 128:
        return 1
    if unicodedata.category(char) in ("Mn", "Me"):
        return 0
    if unicodedata.east_asian_width(char) in ("W", "F"):
        return 2
    return 1


def _text_cols(text):
    plain = _ansi.sub("", text) if "\033" in text else text
    cols = 0
    for char in plain:
        cols += _char_cols(char)
    return cols


def _clip_ansi(text, max_cols):
    """Keep the line on one row. A wrap leaves a colored cell on the next one."""
    out = []
    cols = 0
    index = 0
    limit = len(text)
    while index < limit:
        if text[index] == "\033" and index + 1 < limit and text[index + 1] == "[":
            end = index + 2
            while end < limit and not ("@" <= text[end] <= "~"):
                end += 1
            if end < limit:
                end += 1
            out.append(text[index:end])
            index = end
            continue
        width = _char_cols(text[index])
        if cols + width > max_cols:
            out.append(RESET)
            break
        out.append(text[index])
        cols += width
        index += 1
    return "".join(out)


def _fit_status(text, width):
    if width <= 0:
        return None
    # Empty is a real cell. Returning None leaves the previous spinner up
    # through the black frame of a scene change.
    if not text:
        return ""
    cols = _text_cols(text)
    if cols >= width:
        return _clip_ansi(text, width)
    pad = (width - cols) // 2
    if pad:
        return (" " * pad) + text
    return text


def _paint_row(row, content):
    # Reset before erase. Otherwise the line clear inherits the previous
    # foreground, and a torn write shows that color for a frame.
    if content:
        return f"\033[0m\033[{row};1H\033[2K{content}"
    return f"\033[0m\033[{row};1H\033[2K"


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
        room = reasoning_limit(height)
        if len(above) > room:
            above = above[-room:]
        if column <= 0:
            column = max((_text_cols(line) for line in above), default=0)
        left = max((width - min(column, width)) // 2, 0)
        # Thinking line is the middle row of the bottom band. Reasoning ends
        # on the row above that band.
        rows = band_rows(height)
        band_top = height - rows + 1
        status_at = band_top + rows // 2
        start = band_top - len(above) - 1
        status_cell = _fit_status(text, width) if 1 <= status_at <= height else None
        # Spinner frames change constantly; the paragraph usually does not.
        if (
            self.size == (width, height)
            and self.above == above
            and self.left == left
            and self.start == start
        ):
            if status_cell is not None and self.cells.get(status_at) != status_cell:
                self.cells[status_at] = status_cell
                return _SYNC_ON + _paint_row(status_at, status_cell) + _SYNC_OFF
            return ""
        cells = {}
        pad = " " * left
        for offset, line in enumerate(above):
            row = start + offset + 1
            if row < 1 or row > height:
                continue
            cells[row] = f"{pad}{line}{RESET}" if line else ""
        if status_cell is not None:
            cells[status_at] = status_cell
        full = self.size != (width, height)
        parts = [_SYNC_ON]
        if full:
            parts.append("\033[0m\033[2J\033[H")
            for row in sorted(cells):
                content = cells[row]
                if content:
                    parts.append(_paint_row(row, content))
        else:
            dirty = set(self.cells)
            dirty.update(cells)
            for row in sorted(dirty):
                content = cells.get(row)
                if content is None:
                    parts.append(_paint_row(row, ""))
                    continue
                if self.cells.get(row) != content:
                    parts.append(_paint_row(row, content))
        parts.append(_SYNC_OFF)
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


def _consume_osc():
    """Eat an OSC reply. A background report updates the fade target.

    The bytes are already in the tty buffer by the time the escape is seen.
    Waiting out a long timeout here is a visible hitch in the fade.
    """
    global _bg
    buf = bytearray()
    end = time.monotonic() + 0.008
    while time.monotonic() < end and len(buf) < 1024:
        char = _read_byte(0.002 if not buf else 0)
        if char is None:
            break
        buf += char
        if buf.endswith(b"\a") or buf.endswith(b"\033\\"):
            break
    if not buf:
        return
    _absorb_color_replies(bytes(buf))
    if _tmux_override is None and _osc_bg is not None and _osc_bg != _bg:
        _bg = _osc_bg


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
            # OSC replies (background and Codex color queries) are not a quit key.
            _consume_osc()
            return False
        if nxt != b"[":
            return True
        third = _read_byte(0.01)
        if third == b"<":
            return _sgr_click()
        if third == b"M":
            return _x10_click()
        if third in (b"I", b"O"):
            # Focus in or out. The pane background may have changed with it.
            _invalidate_background()
            return False
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
    sys.stdout.write(_SYNC_OFF + "\033[?1004l\033[?1006l\033[?1000l\033[?25h" + reset + "\n")
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
    _refresh_background(time.monotonic(), block=True)
    signal.signal(signal.SIGINT, restore)
    signal.signal(signal.SIGTERM, restore)
    hidden = "\033[?25l"
    if _input_fd is not None:
        # 1000 reports clicks; 1006 uses the SGR form tmux forwards.
        # 1004 reports focus, which is the cue to reread the pane color.
        hidden += "\033[?1000h\033[?1006h\033[?1004h"
    sys.stdout.write(hidden + "\n")
    sys.stdout.flush()
    start = time.monotonic()
    pace = interval if callable(interval) else None
    pause = 0 if pace else interval
    write = sys.stdout.write
    flush = sys.stdout.flush
    mono = time.monotonic
    getsize = shutil.get_terminal_size
    lines = status.lines
    count = len(lines)
    origin = status.start
    while True:
        if quit_requested():
            restore()
        now = mono()
        _refresh_background(now)
        elapsed = now - start
        size = getsize((80, 24))
        slot, alpha = presentation(elapsed)
        above = reasoning.advance(elapsed, size.columns, reasoning_limit(size.lines))
        shown = fade_ansi(render(elapsed, lines[(origin + slot) % count]), alpha)
        frame = display.render(shown, above, reasoning.limit, size)
        if frame:
            write(frame)
            flush()
        # A number, or a callable so the active script can change the pace.
        time.sleep(pace() if pace else pause)
