#!/usr/bin/env python3
import base64, json, os, re, sys, time, urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

try:
    kind, root_s, date, dir_s, sentinel, load, need, mark, drop_s = sys.argv[1:10]
except ValueError:
    print("refused")
    raise SystemExit

root = Path(root_s).expanduser()
cid = os.environ.get("CURSOR_CONVERSATION_ID") or ""
trans = os.environ.get("AGENT_TRANSCRIPTS") or ""

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
    previous = stamps[-2] if len(stamps) >= 2 else None
    return current, previous, len(stamps)

def ordinal(n):
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n:02d}{suffix}"

def clock(ms):
    dt = datetime.fromtimestamp(ms / 1000, timezone.utc)
    return f"{dt.strftime('%b')} {dt.day}, {dt.strftime('%I:%M %p')}"

def api_key():
    key = os.environ.get("CURSOR_API_KEY", "").strip()
    if key:
        return key
    try:
        lines = (Path.home() / ".cursor" / "team-api-key").read_text().splitlines()
    except Exception:
        return ""
    for line in lines:
        line = line.strip()
        if line:
            return line
    return ""

def usage_events(start_ms, end_ms):
    key = api_key()
    if not key or not cid:
        return None
    auth = base64.b64encode(f"{key}:".encode()).decode()

    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    opener = urllib.request.build_opener(NoRedirect)

    def page(number):
        payload = json.dumps({
            "startDate": start_ms,
            "endDate": end_ms,
            "page": number,
            "pageSize": 100,
        }).encode()
        req = urllib.request.Request(
            "https://api.cursor.com/teams/filtered-usage-events",
            data=payload,
            headers={
                "Authorization": f"Basic {auth}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with opener.open(req, timeout=5) as resp:
            return json.loads(resp.read().decode())

    try:
        data = page(1)
    except Exception:
        return None
    events = list(data.get("usageEvents") or [])
    pages = (data.get("pagination") or {}).get("numPages") or 1
    if pages > 1:
        try:
            last = page(pages)
        except Exception:
            return None
        events.extend(last.get("usageEvents") or [])
    return events

def event_row(event):
    try:
        ts = int(event.get("timestamp"))
    except (TypeError, ValueError):
        return "none"
    tokens = "none"
    usage = event.get("tokenUsage")
    if isinstance(usage, dict):
        total = 0
        try:
            for name in ("inputTokens", "outputTokens", "cacheWriteTokens", "cacheReadTokens"):
                total += int(usage.get(name) or 0)
            tokens = token_label(total)
        except (TypeError, ValueError):
            tokens = "none"
    cost = "none"
    cents = event.get("chargedCents")
    if cents is not None:
        try:
            cost = f"${float(cents) / 100:.2f}"
        except (TypeError, ValueError):
            cost = "none"
    model = event.get("model") or "none"
    return f"{clock(ts)} | {cost} | {tokens} | {model}"

def past_line(previous_ms, current_ms):
    if previous_ms is None or current_ms is None or previous_ms >= current_ms:
        return "none"
    start_ms = previous_ms - 5000
    end_ms = current_ms - 5000
    if end_ms < start_ms:
        return "none"
    events = usage_events(start_ms, end_ms)
    if events is None:
        return "none"
    best = None
    best_ts = -1
    for event in events:
        if event.get("conversationId") != cid:
            continue
        try:
            ts = int(event.get("timestamp"))
        except (TypeError, ValueError):
            continue
        if ts < start_ms or ts >= current_ms - 5000 or ts < best_ts:
            continue
        best = event
        best_ts = ts
    if not isinstance(best, dict):
        return "none"
    return event_row(best)

def token_label(total):
    if total >= 1_000_000:
        return f"{total / 1_000_000:.1f}M"
    if total >= 1000:
        return f"{total / 1000:.1f}K"
    return str(total)

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

def has_mark(d):
    if mark in ("-", ""):
        return True
    f = d / mark
    return f.is_file() and f.stat().st_size == 0

def folder_arg(s):
    if not s.startswith("/"):
        return None
    d = Path(s)
    name = d.name
    if not (
        len(name) > 11
        and name[4] == "-"
        and name[7] == "-"
        and name[10] == "-"
        and name[:4].isdigit()
        and name[5:7].isdigit()
        and name[8:10].isdigit()
        and name[11:]
    ):
        return None
    try:
        if d.parent.resolve() != root.resolve():
            return None
    except Exception:
        return None
    if not d.is_dir():
        return None
    return d

def append_usage(d, past_n, row):
    path = d / "99-CURSOR.md"
    line = f"[{ordinal(past_n)}] {row}\n"
    if path.exists():
        with path.open("a", encoding="utf-8") as handle:
            handle.write(line)
        return
    path.write_text(f"# Cursor Usage\n\n{line}", encoding="utf-8")

def finish(d):
    if not cid:
        print("refused")
        return
    d.mkdir(parents=True, exist_ok=True)
    if drop_s != "-":
        for name in drop_s.split(","):
            if not name or name == sentinel:
                continue
            f = d / name
            if f.is_file():
                f.unlink()
    b = d / sentinel
    if not b.exists():
        b.write_bytes(b"")
    if (not b.is_file()) or b.stat().st_size != 0:
        print("refused")
        return
    current_ms, previous_ms, users = counts()
    shown = users if users else 1
    live = clock(current_ms) if current_ms is not None else "none"
    past = past_line(previous_ms, current_ms)
    if past != "none" and shown >= 2:
        append_usage(d, shown - 1, past)
    print("ok")
    print(d.resolve())
    print(f"{live} | {ordinal(shown)}")
    print(past)

if not cid or not sentinel:
    print("refused")
elif kind == "new":
    finish(root / f"{date}-{cid}")
elif kind == "count":
    d = Path(dir_s).expanduser()
    if dir_s == "-" or not d.is_dir():
        print("refused")
    else:
        finish(d)
elif kind == "load":
    d = folder_arg(dir_s)
    if d is not None and named(d, load):
        finish(d)
    else:
        print("refused")
elif kind == "join":
    d = folder_arg(dir_s)
    if d is not None and has_mark(d) and named(d, need):
        finish(d)
    else:
        print("refused")
elif kind == "next":
    d = Path(dir_s)
    if dir_s.startswith("/") and d.is_dir() and named(d, need):
        finish(d)
    else:
        print("refused")
else:
    print("refused")
