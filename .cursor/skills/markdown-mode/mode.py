#!/usr/bin/env python3
import json, os, sys
from pathlib import Path

try:
    kind, root_s, date, dir_s, sentinel, load, need, mark, drop_s = sys.argv[1:10]
except ValueError:
    print("refused")
    raise SystemExit

root = Path(root_s).expanduser()
cid = os.environ.get("CURSOR_CONVERSATION_ID") or ""
trans = os.environ.get("AGENT_TRANSCRIPTS") or ""

def counts():
    users = assistants = 0
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
            role = obj.get("role")
            if role == "user":
                users += 1
            elif role == "assistant":
                assistants += 1
    return users, assistants

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
    users, assistants = counts()
    print("ok")
    print(d.resolve())
    print(users)
    print(assistants)

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
