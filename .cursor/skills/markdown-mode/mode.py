#!/usr/bin/env python3
import json, os, re, subprocess, sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

cid = os.environ.get("CURSOR_CONVERSATION_ID") or ""
trans = os.environ.get("AGENT_TRANSCRIPTS") or ""

def timer_out(cmd):
    script = Path(__file__).resolve().with_name("time.py")
    proc = subprocess.run(
        [sys.executable, str(script), cmd],
        capture_output=True,
        text=True,
    )
    return (proc.stdout or "").strip()

def peek_span():
    line = timer_out("peek")
    return line or "n/a"

def refuse():
    timer_out("clear")
    print("refused")

try:
    kind, root_s, date, dir_s, load, need = sys.argv[1:7]
except ValueError:
    refuse()
    raise SystemExit

def resolve_root(root_s):
    expanded = Path(root_s).expanduser()
    if expanded.is_absolute():
        return expanded
    # areas/<name> is the parent under ~/Development. Root only places the folder.
    return Path.home() / "Development" / root_s

root = resolve_root(root_s)
NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]*")
SLUG = re.compile(r"(\d{4}-\d{2}-\d{2})_([A-Za-z0-9][A-Za-z0-9_-]*)")

def text_of(content):
    if isinstance(content, str):
        return content
    if not isinstance(content, list):
        return ""
    parts = []
    for block in content:
        if isinstance(block, dict) and block.get("type") == "text":
            parts.append(block.get("text") or "")
    return "\n".join(parts)

def message_ms(text):
    m = re.search(
        r"([A-Z][a-z]{2} \d{1,2}, \d{4}, \d{1,2}:\d{2} [AP]M) \(UTC([+-]\d+)\)",
        text,
    )
    if not m:
        return None
    try:
        dt = datetime.strptime(m.group(1), "%b %d, %Y, %I:%M %p")
        offset = int(m.group(2))
    except ValueError:
        return None
    dt = dt.replace(tzinfo=timezone(timedelta(hours=offset)))
    return int(dt.timestamp() * 1000)

def counts():
    stamps = []
    p = Path(trans) / cid / f"{cid}.jsonl" if cid and trans else None
    if p and p.is_file():
        for line in p.read_text(errors="replace").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue
            if obj.get("role") != "user":
                continue
            msg = obj.get("message") if isinstance(obj.get("message"), dict) else {}
            stamps.append(message_ms(text_of(msg.get("content"))))
    current = stamps[-1] if stamps else None
    return current, len(stamps)

def clock(ms):
    dt = datetime.fromtimestamp(ms / 1000, timezone.utc)
    return f"{dt.strftime('%b')} {dt.day}, {dt.strftime('%I:%M %p')}"

def is_nn(path):
    name = path.name
    return (
        path.is_file()
        and len(name) == 5
        and name[:2].isdigit()
        and name[2:] == ".md"
    )

def named(d, name):
    if name in ("-", ""):
        return True
    if name == "NN":
        return any(is_nn(p) for p in d.iterdir())
    return (d / name).is_file()

def calendar_date(s):
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", s or ""):
        return None
    try:
        datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        return None
    return s

def safe_name(s):
    if s in ("-", ""):
        return None
    s = "_".join(s.split())
    if not NAME.fullmatch(s):
        return None
    return s

def folder_named(s):
    if not s or s == "-" or "/" in s or s.startswith("~") or s.startswith("."):
        return None
    m = SLUG.fullmatch(s)
    if not m or not calendar_date(m.group(1)):
        return None
    d = root / s
    if not d.is_dir():
        return None
    return d

def prepend_call(d, live):
    path = d / "TIMESTAMPS"
    prev = path.read_text(errors="replace") if path.is_file() else ""
    name = d.name
    lines = prev.splitlines()
    if lines and lines[0] == name:
        body = lines[1:]
    else:
        body = lines
    body.insert(0, live)
    text = name + "\n" + "\n".join(body) + "\n"
    path.write_text(text)
    return sum(1 for line in body if line.strip())

def finish(d):
    if not cid:
        refuse()
        return
    d.mkdir(parents=True, exist_ok=True)
    current_ms, users = counts()
    shown = users if users else 1
    live = clock(current_ms) if current_ms is not None else "none"
    row = f"{live} | {peek_span()}"
    stamps = prepend_call(d, row)
    print("ok")
    print(d.name)
    print(row)
    print(f"Prompts {shown} | Timestamps {stamps}")

if not cid:
    refuse()
elif kind == "new":
    name = safe_name(dir_s)
    stamp = calendar_date(date)
    if not name or not stamp:
        refuse()
    else:
        dest = root / f"{stamp}_{name}"
        if dest.exists():
            refuse()
        else:
            finish(dest)
elif kind == "count":
    d = folder_named(dir_s)
    if d is None:
        refuse()
    else:
        finish(d)
elif kind == "load":
    d = folder_named(dir_s)
    if d is not None and named(d, load):
        finish(d)
    else:
        refuse()
elif kind == "next":
    d = folder_named(dir_s)
    if d is not None and named(d, need):
        finish(d)
    else:
        refuse()
else:
    refuse()
