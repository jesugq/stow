---
name: bandage-mode
description: /bandage-mode new or load.
disable-model-invocation: true
---

# Bandage mode

`CURSOR_CONVERSATION_ID` and `AGENT_TRANSCRIPTS` are exported. Read this file once. Do not Read it again.

The argument is the word immediately after `/bandage-mode`. `new` and `load` are accepted. Anything else, including no word, prints `refused` and stops. That reply has no folder, no file, and no ack.

A message that is only `/bandage-mode new` or `/bandage-mode load` follows Common and Only the command, then stops. It does not read Work. Any other message that asks for an answer follows Common and Work. A folder this conversation already set stays `$DIR` until a later `new` or `load`.

## Common

The prompt timestamp is local. The folder date is that local calendar date, before the offset is applied. Use the local date of the earliest user message whose timestamp you can see. When `/bandage-mode new` is the first user message, the folder date is the current stamp's local date.

The ack clock is UTC. The parentheses hold the offset in hours, west when negative, east when positive. Subtract the offset from the local clock: offset `-6` adds 6 hours, offset `+2` subtracts 2 hours. Roll the day when the clock crosses midnight. Format: abbreviated month, day with no leading zero, comma, zero-padded 12-hour clock, AM/PM. No year. No zone. A local stamp of Oct 13, 12:47 PM with offset `-6` is `Oct 13, 06:47 PM`.

`$DIR` has no spaces: `~/.cursor/bandage-mode/<local YYYY-MM-DD>-<$CURSOR_CONVERSATION_ID>`. The mode is on exactly when `$DIR/BANDAGE` exists and its size is 0. A `BANDAGE` whose size is not 0 prints `refused` and writes no `NN.md`.

One shell prints the counts. Do not list the environment. Do not Read the transcript jsonl. Do not scan line bodies. Count a line only when its top-level JSON `role` is `user` or `assistant`. A `tool_use` inside a line is not another line. The transcript path is `$AGENT_TRANSCRIPTS/$CURSOR_CONVERSATION_ID/$CURSOR_CONVERSATION_ID.jsonl`. A missing file is 0 and 0.

Pass `new` and the folder date, or `load`, or `count` and the absolute `$DIR` already set. This is the program:

```
import json, os, sys
from pathlib import Path

kind = sys.argv[1]
home = Path.home() / ".cursor" / "bandage-mode"
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

def bandage(d):
    d.mkdir(parents=True, exist_ok=True)
    b = d / "BANDAGE"
    if not b.exists():
        b.write_bytes(b"")
    if b.stat().st_size != 0:
        print("refused")
        return
    users, assistants = counts()
    print(d)
    print(users)
    print(assistants)

if not cid:
    print("refused")
elif kind == "new":
    bandage(home / f"{sys.argv[2]}-{cid}")
elif kind == "count":
    d = Path(sys.argv[2])
    if d.is_dir():
        bandage(d)
    else:
        print("refused")
elif kind == "load":
    hits = []
    if home.is_dir():
        hits = sorted(
            p for p in home.iterdir()
            if p.is_dir() and any(p.glob("[0-9][0-9].md"))
        )
    if not hits:
        print("refused")
    elif len(hits) == 1:
        bandage(hits[0])
    else:
        for p in hits:
            print(p)
else:
    print("refused")
```

Stdout is one of three shapes. `refused` alone means print `refused` and stop. A second line that is an integer means line 1 is the absolute `$DIR`, line 2 the raw user count, line 3 the raw assistant count. Any other stdout is one absolute path per line: the message is `Which conversation?` and those paths, each in backticks, then stop. No ack. No file. The user's reply picks one path. That path is `$DIR`.

The speaking message is the message after this shell. It does not run the shell again and it does not open the jsonl. A raw assistant count above 0 is earlier rounds of this prompt. Prompts is the number of user messages in this conversation, including the one being answered. When the raw user count is higher, Prompts is the raw user count. Model Calls is the raw assistant count plus 2. The shell invocation is already in the file. The speaking message is the current call. A model call is one assistant invocation. A `tool_use` inside it is not another model call.

The user-facing message is only the ack lines. Omit `[sect]` when this speaking message wrote no `NN.md`. When it wrote one, the line after `[path]` is `[sect] created file NN`.

```
[path] <absolute $DIR>
[sect] created file 01
[dutc] Oct 13, 06:47 PM
[call] Prompts: 4, Model Calls: 11
```

## Only the command

Run the shell once. `new` passes the folder date and does not look for other folders. The shell creates `$DIR` when absent and creates an empty `BANDAGE` only when `BANDAGE` is absent. It does not truncate `BANDAGE`. `load` does not create a conversation folder. A `BANDAGE` file with no `NN.md` is not a conversation. One match creates an empty `BANDAGE` only when it is absent.

The speaking message prints the ack or `refused` or `Which conversation?`. It writes no `NN.md`. It deletes nothing.

Stop.

## Work

The command may sit anywhere in the message. The shell from Common is the last tool invocation before the speaking message. Research tools run in that same invocation or earlier. Do not run a tool after that shell returns. `new` and `load` are the shell kinds when this message contains that command. When `$DIR` is already set and the message does not contain `new` or `load`, the kind is `count`.

The shell creates the sentinel. The speaking message writes the answer and prints the ack. Do not end after the sentinel with no answer. Do not take another turn to check the write, lint, or restate the answer.

While `BANDAGE` exists and its size is 0, each message that asks for an answer writes the next `NN.md`. Create `$DIR` when it is absent. The turn that sets `$DIR` leaves an existing `BANDAGE` in place.

Once `$DIR` is set, read the `NN.md` files there once and continue from them. Do not read another conversation's transcript. The next number is one higher than the highest `NN.md` in `$DIR`. After that read, do not Read an earlier `NN.md` again.

The answer is one new file, `$DIR/NN.md`. `NN` is `01`, then `02`, in the order written. The first line is `# NN`, the file number alone (`# 01` in `01.md`). A blank line follows. The rest is the whole answer. Do not add another heading. Do not split the answer into more than one file. Do not change an earlier file.

When referring to a file, use one of two: a file in the agent cwd is `lua/libfuns/context.lua:26` (relative, colon, line on the right); a file outside that cwd is its absolute path, colon, line on the right; never `../`. A range is `file.rb:36-53`. Never put the line before the path (`26:file`, `36:53:file`, `254:258:app/policies/practice_policy.rb`). Keep each path in backticks so neovim `` yi` `` selects them; the cite for a fenced quote is that same backtick path, not the fence language. Quote source inline if it is one line, in a fenced block if it is larger; never as bare lines. Open a fence with backticks only; the first line inside is source. Nothing follows those backticks: no language, no line numbers, no path. The lines always go to the right (`app/policies/practice_policy.rb:254-258`). Do not open a fence with `254:258:app/policies/practice_policy.rb`.

A tool result already in the conversation is the file contents. Do not Read that path again. Re-read only when this conversation has edited that file since the last read and a later step needs the new contents, or the user says the file changed outside this conversation. After a successful Write, do not Read the file to confirm it. Do not Read the transcript jsonl. To find a symbol, Grep first and Read only that line range. Do not read a large file to locate a few lines.

One speaking message writes one answer file, then stops.

Do not run test suites or test runners. Do not run rspec, QUnit, ember test, pnpm test, `sp rspec`, `sp exec test:browser`, dockerized test containers, or a retry loop around those. Do not start, stop, or probe containers. Do not run checksums, docker logs, or curl probes.

No other chat: no prose, code, findings, or summary. Put the answer in the file. The file-question exception is `Which conversation?` and the paths.
