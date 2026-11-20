---
name: markdown-mode
description: /markdown-mode new, load, or next.
disable-model-invocation: true
---

# Markdown mode

`CURSOR_CONVERSATION_ID` and `AGENT_TRANSCRIPTS` are exported. This skill is the command. Call the Skill tool with `markdown-mode` for the folder, the ack, and the markdown file. A caller passes parameters and does not restate this file. Read this file once. Do not Read it again.

`/markdown-mode new`, `/markdown-mode load`, and `/markdown-mode next` run it with the direct parameters. `new` creates a folder. `load` opens an existing folder. `next` follows the sentinel of the previous mode.

## Parameters

Direct commands use these values. A caller replaces the ones it names.

```
verb: new | load | next
root: ~/.cursor/markdown-mode
sentinel: MARKDOWN
drop: -
load: NN
need: -
mark: MARKDOWN
then:
sect: file
```

`verb` is the word immediately after the mode command. `new`, `load`, and `next` are accepted. Anything else, including no word, prints `refused` and stops. That reply has no folder, no file, and no ack. A caller may accept a subset. A verb outside that subset is `refused`.

`root` is the parent of the conversation folders. `sentinel` is the zero-byte file that marks this mode on. `drop` is the sentinels to delete when this mode turns on, comma-separated, or `-`. `load` is the file `load` searches for. `NN` means a file named `[0-9][0-9].md`. `need` is a markdown file `next` requires, or `-`. `mark` is the previous mode's sentinel that `next` searches for when this conversation has no folder yet. `then` is the text of the `[next]` line. Empty omits that line. `sect` is `file` or `heading`.

When the message is only the mode command and an accepted verb, follow Common and Only the command, then stop. Do not read Work. Any other message that asks for an answer follows Common and Work. Do not write markdown for a message that is only the command, including when the caller's skill describes a file.

If the message contains more than one of `/markdown-mode`, `/booking-mode`, `/analyze-mode`, `/clarify-mode`, `/handoff-mode`, `/prepare-mode`, or `/takeoff-mode`, the last one is the caller for the whole message. Use that caller's parameters. Write that caller's file and print that ack. A caller may append lines after the ack only when its own skill says so.

A folder this conversation already set stays `$DIR` until a later `new` or `load`. `next` keeps that folder and does not scan.

## Common

The prompt timestamp is local. The folder date is that local calendar date, before the offset is applied. Use the local date of the earliest user message whose timestamp you can see. When `new` is the first user message, the folder date is the current stamp's local date.

The ack clock is UTC. The parentheses hold the offset in hours, west when negative, east when positive. Subtract the offset from the local clock: offset `-6` adds 6 hours, offset `+2` subtracts 2 hours. Roll the day when the clock crosses midnight. Format: abbreviated month, day with no leading zero, comma, zero-padded 12-hour clock, AM/PM. No year. No zone. A local stamp of Oct 13, 12:47 PM with offset `-6` is `Oct 13, 06:47 PM`.

The mode is on exactly when `$DIR/<sentinel>` exists and its size is 0. A sentinel whose size is not 0 prints `refused` and writes no markdown.

One shell. Do not list the environment. Do not Read the transcript jsonl. Do not scan line bodies. Count a line only when its top-level JSON `role` is `user` or `assistant`. A `tool_use` inside a line is not another line. The transcript is `$AGENT_TRANSCRIPTS/$CURSOR_CONVERSATION_ID/$CURSOR_CONVERSATION_ID.jsonl`. A missing file is 0 and 0.

Args, in order: `kind`, `root`, `date`, `dir`, `sentinel`, `load`, `need`, `mark`, `drop`. `kind` is `new`, `load`, `next`, or `count`. `date` is the folder date for `new`, otherwise `-`. `dir` is the absolute `$DIR` already set, otherwise `-`. `count` is the kind when this conversation already has `$DIR` and the message is work with no `new`, `load`, or `next`.

```
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

def hits(pred):
    if not root.is_dir():
        return []
    return sorted(p for p in root.iterdir() if p.is_dir() and pred(p))

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
    found = hits(lambda d: named(d, load))
    if len(found) == 1:
        finish(found[0])
    elif not found:
        print("refused")
    else:
        print("which")
        for p in found:
            print(p.resolve())
elif kind == "next":
    if dir_s != "-":
        d = Path(dir_s).expanduser()
        if d.is_dir() and named(d, need):
            finish(d)
        else:
            print("refused")
    else:
        found = hits(lambda d: has_mark(d) and named(d, need))
        if len(found) == 1:
            finish(found[0])
        elif not found:
            print("refused")
        else:
            print("paths")
            for p in found:
                print(p.resolve())
else:
    print("refused")
```

The first stdout line decides the reply.

- `refused` — print `refused` and stop.
- `which` — the remaining lines are absolute paths. The message is `Which conversation?` and those paths, each in backticks. No ack. No file. Stop. The user's reply picks one path. That path is `$DIR`. The next shell is `count` with that `dir` and the same parameters.
- `paths` — the remaining lines are absolute paths. Print those paths, each in backticks. No ack. No file. Do not ask `Which conversation?`. Stop.
- `ok` — line 2 is the absolute `$DIR`, line 3 the raw user count, line 4 the raw assistant count.

`new` creates `$DIR` as `<root>/<local YYYY-MM-DD>-<$CURSOR_CONVERSATION_ID>` and does not look at sibling folders. `load` searches `root` for `load` and creates no folder when nothing matches. `next` with `dir` set uses it, does not scan, and requires `need` when `need` is not `-`. `next` with no `dir` searches `root` for a zero-byte `mark`, and for `need` when `need` is not `-`. One match sets `$DIR`. The shell creates `sentinel` empty only when it is absent, deletes each `drop` name, and does not truncate a sentinel that exists. It does not delete markdown.

The speaking message is the next message after this shell. It does not run the shell again and it does not open the jsonl. A raw assistant count above 0 is earlier rounds of this prompt. Prompts is the number of user messages in this conversation, including the one being answered. When the raw user count is higher, Prompts is the raw user count. Model Calls is the raw assistant count plus 2. The shell invocation is already in the file. The speaking message is the current call. A model call is one assistant invocation. A `tool_use` inside it is not another model call.

The user-facing message is only the ack. Omit `[sect]` when this speaking message wrote no markdown. Omit `[next]` when `then` is empty. `[sect]` is `created` or `updated`, then the noun, then the numbers whose body was written. `sect: file` uses `file` and `files`. `sect: heading` uses `heading` and `headings`. One number uses the singular. More than one uses the plural. A turn that both creates and updates lists created first (`created heading 01, updated headings 02, 03`). A heading that only shifted number is not listed.

```
[path] <absolute $DIR>
[sect] created heading 01, updated headings 02, 03
[next] /clarify-mode next
[dutc] Oct 13, 06:47 PM
[call] Prompts: 4, Model Calls: 11
```

## Only the command

Run the shell once. The speaking message prints the ack, `refused`, `Which conversation?`, or the `paths` list. It writes no markdown. It deletes nothing.

Stop.

## Work

The shell from Common is the last tool invocation before the speaking message. Research tools run in that same invocation or earlier. Do not run a tool after that shell returns.

The shell creates the sentinel. The speaking message writes the caller's file and prints the ack. Do not end after the sentinel when the message asked for work and the file was not written. Do not take another turn to check the write, lint, or restate the answer.

While the sentinel exists and its size is 0, each message that asks for an answer writes that file. Once `$DIR` is set, read the markdown files there once and continue from them. Do not read another conversation's transcript. Read each file in `$DIR` at most once per user message. Do not Read a skill file to resume a mode.

A tool result already in the conversation is the file contents. Do not Read that path again. Re-read only when this conversation has edited that file since the last read and a later step needs the new contents, or the user says the file changed outside this conversation. After a successful Write, do not Read the file to confirm it. Do not Read the transcript jsonl. To find a symbol, Grep first and Read only that line range. Do not read a large file to locate a few lines.

A file in the agent cwd is `lua/libfuns/context.lua:26` (relative, colon, line on the right). A file outside that cwd is its absolute path, colon, line on the right. Never `../`. A range is `file.rb:36-53`. Never put the line before the path (`26:file`, `36:53:file`, `254:258:app/policies/practice_policy.rb`). Keep each path in backticks so neovim `` yi` `` selects them. The cite for a fenced quote is that same backtick path, not the fence language. Quote source inline if it is one line, in a fenced block if it is larger, never as bare lines. Open a fence with backticks only. The first line inside is source. Nothing follows those backticks: no language, no line numbers, no path. The lines always go to the right (`app/policies/practice_policy.rb:254-258`). Do not open a fence with `254:258:app/policies/practice_policy.rb`.

## Writing style

The caller decides the sections, the headings, and the focus. This style decides the sentences in those sections. A caller does not restate this style. Do not add a heading for the style. Do not write the output-style frontmatter into the answer file. That frontmatter is `name: STE` and `keep-coding-instructions: true` on the Claude style file. It is not part of the answer.

Write prose in STE-flavored Simplified Technical English. Follow the structural rules of ASD-STE100. This file omits its approved dictionary. Treat word choice as a direction, not a verifiable rule. Drop the style when the user asks for another voice.

The caller's required first line stays the first line. A fixed phrase the caller requires stays as the caller wrote it. The style does not govern code, identifiers, paths, commands, or configuration. Never rename an identifier to satisfy the style. Quote a file, a tool result, an error, or the user exactly.

These rules govern prose in the caller's file, and commit messages, code comments, and documentation.

Check each sentence against these three before you write the next one. Scan the finished draft for all three before you send it.

1. Name the actor. Look for a form of `be` or `get` before a past participle. Name who acts, or rewrite. A state description is fine: nothing acts in "the file is corrupted". Wrong: "Code blocks are stripped." Right: "The script strips code blocks."
2. One idea per sentence. Look for `, and`, `, but`, or `, so` joining two clauses. Split the sentence. `, so` leaks most often. Wrong: "It spreads load, so no machine saturates." Right: "It spreads load. No machine saturates."
3. Repeat the verb. Never replace a verb you already used with `did`, `does`, or `is`. Wrong: "Topic changed at the same moment the style did." Right: "Topic changed at the same moment the style changed."

Cap an instruction at 20 words. Cap a description at 25. Use no semicolons. Write two sentences. Stack 3 nouns at most. Write "the handler for the retry backoff policy", not "request retry backoff policy handler". Use simple tenses. Keep a compound tense that carries information: "the build has finished" states current relevance. Put one topic in one paragraph. Cap it at 6 sentences. Use a numbered list for 3 or more steps. Use a bulleted list for 3 or more parallel items.

Use one name for one thing. Do not rotate synonyms. Prefer the plain verb. Write "start", not "spin up". Write "read", not "dive into". Prefer the verb to its noun form. Write "analyze the log", not "perform an analysis of the log". Delete marketing adjectives: seamless, robust, powerful, blazing-fast, cutting-edge, effortless. Give the measurement that earns the claim, or write nothing. Delete stacked hedges. One hedge at true strength carries information. Three carry none.

Cut what carries no information. Delete a section before compressing every sentence in it. Cut preamble, self-narration, and the closing offer. Cut a point you already made. Cut filler openers: "I will now", "let me", "it is worth noting that". Cut any adjective that states no measurement.

Keep every hedge at its original strength. "The test may have failed" is not "the test failed". Keep every condition, exception, number, and scope qualifier. Add no fact you have not verified. A sentence that reads better because it supplies a cause has stopped being true. Stop when the sentence is unambiguous, not when it is shortest. Say what you kept and why. Put that sentence in the section you changed. When the caller forbids a sentence that is not the section's focus, keep the qualifier in the required sentence and add no extra sentence.

In the file, put the answer in the first sentence after any required first line. The chat message stays the ack.

`sect: file` writes one new file, `$DIR/NN.md`. `NN` is `01`, then `02`, in the order written. The first line is `# NN`, the file number alone (`# 01` in `01.md`). A blank line follows. The rest is the whole answer. That prose follows Writing style. Do not add another heading. Do not split the answer into more than one file. Do not change an earlier file. One speaking message writes that one file, then stops. Do not run test suites or test runners. Do not run rspec, QUnit, ember test, pnpm test, `sp rspec`, `sp exec test:browser`, dockerized test containers, or a retry loop around those. Do not start, stop, or probe containers. Do not run checksums, docker logs, or curl probes.

`sect: heading` writes the caller's named file. H1 only. No frontmatter. No JSON. The first heading starts the file. A blank line follows every heading, and a blank line precedes every later heading. A heading keeps its number while it stays. The caller names the headings and the bodies. Prose in a body follows Writing style. Do not delete the markdown. One speaking message writes that file, then stops.

No other chat: no prose, code, findings, or summary. Put the answer in the file.
