---
name: outline-mode
description: Toggle with `/outline-mode`. While on, every substantive reply is written to the next `NN-<slug>.md` under `$DIR`; chat only names the folder and the new file. No in-chat outlines.
disable-model-invocation: true
---

# Outline mode

Shared with takeoff-mode, mermaid-mode, and handoff-mode. `$NAME` is `<local YYYY-MM-DD>-<$CURSOR_CONVERSATION_ID>`: the date, one hyphen, then the conversation id, with no spaces. `$DIR = ~/.cursor/dynamic-mode/$NAME` (refuse if the conversation id is unset). Example: `~/.cursor/dynamic-mode/2026-09-24-<id>`. All four modes use this one folder and the same `NN-*.md` sequence. The date is the local calendar date at the start of the turn; the same day and conversation always resolve to the same `$DIR`.

On is `$DIR/OUTLINE` existing (a zero-byte sentinel, not JSON). `$DIR/TAKEOFF` means takeoff-mode is on instead. `$DIR/MERMAID` means mermaid-mode is on instead. `$DIR/HANDOFF` means handoff-mode is on instead. Neither sentinel means off — a folder or leftover markdown alone is off. The four sentinels are mutually exclusive. `/outline-mode` toggles this mode; extra words after it are ignored. `/takeoff-mode`, `/mermaid-mode`, and `/handoff-mode` belong to the other skills: do not write a file and do not print an outline-mode comment for them.

Enabling while `TAKEOFF`, `MERMAID`, or `HANDOFF` exists swaps. Delete those sentinels, create `OUTLINE`, keep every `NN-*.md`, and continue that index. The next substantive reply uses outline-mode’s shape.

## Action comment

Every outline-mode action — enabling, disabling, swapping on, creating a file, hitting the 99-file cap — is only these sections, with a blank line between each:

    [outline-mode] <short comment>

    <absolute $DIR>

    [<absolute new file, write turns only>]

    [usage-utc-date] <UTC time the prompt was sent>

`<short comment>` is `enabled`, `disabled`, `created a file`, or `limit reached`. A swap that turns outline-mode on uses `enabled`. Nothing else (no titles, outline, or section bodies). The last line is the UTC time Cursor records for this model call on the usage dashboard: the time the user sent the prompt, not the time the response finishes. Take that prompt timestamp and convert it to UTC. Format it `[usage-utc-date] Oct 13, 06:47 PM`: the tag, then an abbreviated English month, day with no leading zero, a comma, then a zero-padded 12-hour clock and `AM` or `PM`. No year and no timezone label.

Enable / swap / disable:

    [outline-mode] enabled

    /Users/<you>/.cursor/dynamic-mode/2026-09-24-<id>

    [usage-utc-date] Oct 13, 06:47 PM

Write:

    [outline-mode] created a file

    /Users/<you>/.cursor/dynamic-mode/2026-09-24-<id>

    /Users/<you>/.cursor/dynamic-mode/2026-09-24-<id>/01-what-is-outline-mode.md

    [usage-utc-date] Oct 13, 06:47 PM

## Toggle

- Off → on: create `$DIR` if needed, write `$DIR/OUTLINE`, comment `enabled`, print `$DIR`. If `$DIR/TAKEOFF`, `$DIR/MERMAID`, or `$DIR/HANDOFF` exists, delete it first (swap). Keep any existing `NN-*.md`; the next write continues the index, including files takeoff-mode, mermaid-mode, or handoff-mode already wrote.
- On → off: delete only `$DIR/OUTLINE`. Leave every markdown file. Comment `disabled`, print `$DIR`.

## Write

While `OUTLINE` exists, each substantive user query creates exactly one new file. Never edit an existing file (follow-ups and revisions are the next index), including files takeoff-mode, mermaid-mode, or handoff-mode wrote. Ignore leftover `major-*` / `minor-*` / `*.json` names.

- Next index = `count($DIR/[0-9][0-9]-*.md) + 1`, zero-padded to two digits (`01`, `02`, …).
- Path: `$DIR/<NN>-<slug>.md`. `<slug>` is kebab-case from the H1 summary (lowercase, hyphens, no spaces).
- If the next index would be `100`, write nothing, comment `limit reached`, print `$DIR`, and tell the user inline to start a new conversation. Two-digit prefixes only — `100-*.md` would sort before `99-*.md`.

Shape:

    # <5-10 word summary>

    ## <5-10 word title>

    <full section body>

    ## ...

As many `##` sections as the reply needs. No YAML frontmatter. No JSON sidecar. The H1 starts the file (no blank line before it). Blank line after every heading, including `#`.

## Bypass

These skip creating a markdown file but still use the action comment when they are outline-mode actions. The UTC line stays last.

- **Toggle acks** — comment, the `$DIR` line, then the UTC line. A swap that enables outline-mode is an enable ack.
- **Capacity** — comment `limit reached`, `$DIR` line, one-line “start a new conversation.”, then the UTC line.
- **Short prose** — trivial one-liners unrelated to any outline-mode action (e.g. plain "Yes", "Done", tool-only turns) get no comment line and no file. Use sparingly; anything substantive still goes through outline mode.
