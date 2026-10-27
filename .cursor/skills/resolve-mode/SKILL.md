---
name: resolve-mode
description: Toggle with `/resolve-mode`. While on, ambiguity-bearing replies are written to the next `NN-resolve-<slug>.md` under `$DIR`, one ambiguity per `#` section. Each section is a browser tab pin and stays in later resolve-mode files until the ambiguity is resolved, when its body is `Resolved.` and later files omit it. Chat prints only the `[resolve-mode]` line, the absolute directory, and the `[usage-utc-date]` line when a file or toggle ack is produced. No in-chat resolutions.
disable-model-invocation: true
---

# Resolve mode

Shared with outline-mode, takeoff-mode, and handoff-mode. `$NAME` is `<local YYYY-MM-DD>-<$CURSOR_CONVERSATION_ID>`: the date, one hyphen, then the conversation id, with no spaces. `$DIR = ~/.cursor/dynamic-mode/$NAME` (refuse if the conversation id is unset). Example: `~/.cursor/dynamic-mode/2026-09-24-<id>`. All four modes use this one folder and the same `NN-*.md` sequence. The date is the local `YYYY-MM-DD` when the conversation started, taken from its first message. A later turn on another calendar day keeps that same date and the same `$DIR`. If a directory whose name ends in `-$CURSOR_CONVERSATION_ID` already exists under `~/.cursor/dynamic-mode`, that directory is `$DIR`; when more than one exists, use the earliest date. Do not create a second folder because the current turn falls on a later day.

On is `$DIR/RESOLVE` existing (a zero-byte sentinel, not JSON). `$DIR/OUTLINE` means outline-mode is on instead. `$DIR/TAKEOFF` means takeoff-mode is on instead. `$DIR/HANDOFF` means handoff-mode is on instead. No sentinel means off — a folder or leftover markdown alone is off. The four sentinels are mutually exclusive. `/resolve-mode` toggles this mode; extra words after it are ignored. `/outline-mode`, `/takeoff-mode`, and `/handoff-mode` belong to the other skills: do not write a file and do not print a `[resolve-mode]` line for them.

Enabling while `OUTLINE`, `TAKEOFF`, or `HANDOFF` exists swaps. Delete those sentinels, create `RESOLVE`, keep every `NN-*.md`, and continue that index. The next ambiguity-bearing reply uses resolve-mode’s shape.

## Action comment

When this turn writes a file, enables, disables, swaps, or hits the cap, chat is only these three lines, with a blank line between each. When this turn does none of those, answer in chat and do not print a `[resolve-mode]` line.

    [resolve-mode] <short comment>

    <absolute $DIR>

    [usage-utc-date] <UTC time the prompt was sent>

`<short comment>` is `enabled`, `disabled`, `created a file`, or `limit reached`. A swap that turns resolve-mode on uses `enabled`. Nothing else (no titles, ambiguities, file path, or section bodies). The last line is the UTC time Cursor records for this model call on the usage dashboard: the time the user sent the prompt, not the time the response finishes. Take that prompt timestamp and convert it to UTC. Format it `[usage-utc-date] Oct 13, 06:47 PM`: the tag, then an abbreviated English month, day with no leading zero, a comma, then a zero-padded 12-hour clock and `AM` or `PM`. No year and no timezone label.

Enable / swap / disable / write:

    [resolve-mode] enabled

    /Users/<you>/.cursor/dynamic-mode/2026-09-24-<id>

    [usage-utc-date] Oct 13, 06:47 PM

## Toggle

- Off → on: create `$DIR` if needed, write `$DIR/RESOLVE`, comment `enabled`, print `$DIR`. If `$DIR/OUTLINE`, `$DIR/TAKEOFF`, or `$DIR/HANDOFF` exists, delete it first (swap). Keep any existing `NN-*.md`; the next write continues the index, including files the other modes already wrote.
- On → off: delete only `$DIR/RESOLVE`. Leave every markdown file. Comment `disabled`, print `$DIR`.

## Write

While `RESOLVE` exists, a turn that opens an ambiguity, updates one, or resolves one writes exactly one new file. That file is the whole pin board. Never edit an existing file (follow-ups and revisions are the next index), including files the other modes wrote. Ignore leftover `major-*` / `minor-*` / `*.json` names.

- Next index = `count($DIR/[0-9][0-9]-*.md) + 1`, zero-padded to two digits (`01`, `02`, …). Count every mode’s files, not only resolve-mode files.
- Path: `$DIR/<NN>-resolve-<slug>.md`. The `resolve-` prefix is required so later turns can find the pin board. `<slug>` is kebab-case from a 5–10 word summary of the file (lowercase, hyphens, no spaces). Do not write that summary as a heading.
- If the next index would be `100`, write nothing and comment `limit reached`. Two-digit prefixes only — `100-*.md` would sort before `99-*.md`.

Shape — one ambiguity per section. Never write a `##` heading. A heading that would have been `##` is `#`. No YAML frontmatter. No JSON sidecar. The first heading starts the file (no blank line before it). Blank line after every heading. Blank line before every heading after the first.

    # <5-10 word ambiguity>

    <full section body>

    # ...

## Pins

Each `#` section is one ambiguity and one browser tab pin. The heading text is the pin. Reuse it character for character while the pin stays. Do not rename a pin. Do not open a second pin for the same ambiguity.

Before writing, read every `$DIR/[0-9][0-9]-resolve-*.md` in index order. The latest of those files is the pin board. No such file means there are no pins yet.

- A heading on that board whose body is not exactly `Resolved.` is open. Include it in this file, in the same order.
- A heading on that board whose body is exactly `Resolved.` is closed. Do not include it.
- A heading that an older resolve-mode file had, and that the latest file omits, stays closed. Do not bring it back.
- Append new ambiguities from this turn after the carried pins.
- When this turn resolves an open pin, keep that heading in this file and set its body to exactly `Resolved.`. The next resolve-mode file omits that heading.
- A file that carries an open pin includes it even when this turn does not mention it.

While a pin is open, the body addresses that ambiguity in the implementation: what is undecided, and what would settle it. Update the body when this turn changes the ambiguity. When nothing changed, copy the previous body.

When the ambiguity is resolved, that section's content is just the text `Resolved.`. No other words in that section. Do not write `Resolved.` while a choice is still open. Settled means the user chose, or the implementation already decides it.

A turn that leaves the board unchanged — nothing new, nothing updated, nothing resolved — writes no file. Open pins stay on the latest resolve-mode file until a later file carries them.

## Bypass

These skip creating a markdown file but still use the action comment when they are resolve-mode actions. The UTC line stays last.

- **Toggle acks** — the `[resolve-mode]` line, the `$DIR` line, then the UTC line. A swap that enables resolve-mode is an enable ack.
- **Capacity** — `[resolve-mode] limit reached`, the `$DIR` line, then the UTC line.
- **No pin change** — trivial one-liners (plain "Yes", "Done", tool-only turns) and any turn that does not open, update, or resolve an ambiguity get no comment line and no file. A short ack that settles an open ambiguity is a write, not a skip. The section in that file is `Resolved.`
