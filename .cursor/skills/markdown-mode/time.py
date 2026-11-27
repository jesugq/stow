#!/usr/bin/env python3
import os, re, sys, time
from pathlib import Path

cid = os.environ.get("CURSOR_CONVERSATION_ID") or ""

def timer_path():
    if not re.fullmatch(r"[A-Za-z0-9_-]+", cid or ""):
        return None
    d = Path.home() / ".local/state/markdown-mode/timers"
    d.mkdir(parents=True, exist_ok=True)
    return d / cid

def format_span(secs):
    h, rem = divmod(secs, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h}h {m:02d}m {s:02d}s"
    if m:
        return f"{m}m {s:02d}s"
    return f"{s}s"

def span(unlink):
    p = timer_path()
    if p is None or not p.is_file():
        return "n/a"
    raw = p.read_text(errors="replace").strip()
    if unlink:
        p.unlink()
    try:
        start = float(raw)
    except ValueError:
        return "n/a"
    secs = max(0, int(time.time() - start))
    return format_span(secs)

def begin():
    p = timer_path()
    if p is not None and not p.is_file():
        p.write_text(f"{time.time():.3f}\n")
    print("timer")

def cancel():
    p = timer_path()
    if p is not None and p.is_file():
        p.unlink()
    print("timer")

def clear():
    p = timer_path()
    if p is not None and p.is_file():
        p.unlink()

cmd = sys.argv[1] if len(sys.argv) > 1 else ""
if cmd == "begin":
    begin()
elif cmd == "cancel":
    cancel()
elif cmd == "stop":
    print(span(True))
elif cmd == "peek":
    print(span(False))
elif cmd == "clear":
    clear()
else:
    print("refused")
