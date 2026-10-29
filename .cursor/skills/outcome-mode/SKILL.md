---
name: outcome-mode
description: Toggle with `/outcome-mode`. While on, ambiguity-bearing replies are written to the next `NN-OUTCOME-<slug>.md` under `$DIR`, one ambiguity per `#` section. Each section is a browser tab pin and stays in later outcome-mode files until the ambiguity is resolved, when its body is `Resolved, <decision>` and later files omit it. Chat prints only the `[outcome-mode]` line, the absolute directory, `/handoff-mode`, and the `[usage-utc-date]` line when a file or toggle ack is produced. No in-chat resolutions.
disable-model-invocation: true
---

# Outcome mode

Shared with outline-mode, takeoff-mode, and handoff-mode. `$NAME` is `<local YYYY-MM-DD>-<$CURSOR_CONVERSATION_ID>`: the date, one hyphen, then the conversation id, with no spaces. `$DIR = ~/.cursor/dynamic-mode/$NAME` (refuse if the conversation id is unset). Example: `~/.cursor/dynamic-mode/2026-09-24-<id>`. All four modes use this one folder and the same `NN-*.md` sequence. Each mode prefixes its own files: `NN-OUTLINE-<slug>.md`, `NN-OUTCOME-<slug>.md`, `NN-HANDOFF-<slug>.md`, `NN-TAKEOFF-<slug>.md`. The index counts every prefix. `<slug>` does not repeat the mode name. The modes run outline-mode, then outcome-mode, then handoff-mode, then takeoff-mode. The date is the local `YYYY-MM-DD` when the conversation started, taken from its first message. A later turn on another calendar day keeps that same date and the same `$DIR`. If a directory whose name ends in `-$CURSOR_CONVERSATION_ID` already exists under `~/.cursor/dynamic-mode`, that directory is `$DIR`; when more than one exists, use the earliest date. Do not create a second folder because the current turn falls on a later day.

On is `$DIR/OUTCOME` existing (a zero-byte sentinel, not JSON). `$DIR/OUTLINE` means outline-mode is on instead. `$DIR/TAKEOFF` means takeoff-mode is on instead. `$DIR/HANDOFF` means handoff-mode is on instead. No sentinel means off — a folder or leftover markdown alone is off. The four sentinels are mutually exclusive. `/outcome-mode` toggles this mode; extra words after it are ignored. `/outline-mode`, `/takeoff-mode`, and `/handoff-mode` belong to the other skills: do not write a file and do not print an `[outcome-mode]` line for them.

Enabling while `OUTLINE`, `TAKEOFF`, or `HANDOFF` exists swaps. Delete those sentinels, create `OUTCOME`, keep every `NN-*.md`, and continue that index. The next ambiguity-bearing reply uses outcome-mode’s shape.

## Action comment

When this turn writes a file, enables, disables, swaps, or hits the cap, chat is only these four lines, with a blank line between each. When this turn does none of those, answer in chat and do not print an `[outcome-mode]` line.

    [outcome-mode] <short comment>

    <absolute $DIR>

    /handoff-mode

    [usage-utc-date] <UTC time the prompt was sent>

`<short comment>` is `enabled`, `disabled`, `created a file`, or `limit reached`. A swap that turns outcome-mode on uses `enabled`. Nothing else (no titles, ambiguities, file path, or section bodies). The line after `$DIR` is the next mode to swap to. The last line is the UTC time Cursor records for this model call on the usage dashboard: the time the user sent the prompt, not the time the response finishes. Take that prompt timestamp and convert it to UTC. Format it `[usage-utc-date] Oct 13, 06:47 PM`: the tag, then an abbreviated English month, day with no leading zero, a comma, then a zero-padded 12-hour clock and `AM` or `PM`. No year and no timezone label.

Enable / swap / disable / write:

    [outcome-mode] enabled

    /Users/<you>/.cursor/dynamic-mode/2026-09-24-<id>

    /handoff-mode

    [usage-utc-date] Oct 13, 06:47 PM

## Toggle

- Off → on: create `$DIR` if needed, write `$DIR/OUTCOME`, comment `enabled`, print `$DIR`. If `$DIR/OUTLINE`, `$DIR/TAKEOFF`, or `$DIR/HANDOFF` exists, delete it first (swap). Keep any existing `NN-*.md`; the next write continues the index, including files the other modes already wrote.
- On → off: delete only `$DIR/OUTCOME`. Leave every markdown file. Comment `disabled`, print `$DIR`.

## Write

While `OUTCOME` exists, a turn that opens an ambiguity, updates one, or resolves one writes exactly one new file. That file is the whole pin board. Never edit an existing file (follow-ups and revisions are the next index), including files the other modes wrote. Ignore leftover `major-*` / `minor-*` / `*.json` names.

- Next index = `count($DIR/[0-9][0-9]-*.md) + 1`, zero-padded to two digits (`01`, `02`, …). Count every mode’s files, not only outcome-mode files.
- Path: `$DIR/<NN>-OUTCOME-<slug>.md`. The `OUTCOME` prefix is required so later turns can find the pin board. `<slug>` is kebab-case from a 5–10 word summary of the file (lowercase, hyphens, no spaces). Do not write that summary as a heading. Example: `02-OUTCOME-questions-blocking-passkey-error-plan.md`.
- If the next index would be `100`, write nothing and comment `limit reached`. Two-digit prefixes only — `100-*.md` would sort before `99-*.md`.

Shape — one ambiguity per section. Never write a `##` heading. A heading that would have been `##` is `#`. No YAML frontmatter. No JSON sidecar. The first heading starts the file (no blank line before it). Blank line after every heading. Blank line before every heading after the first.

    # <5-10 word ambiguity>

    <full section body>

    # ...

## Pins

Each `#` section is one ambiguity and one browser tab pin. The heading text is the tab label. Reuse it character for character while the pin stays. Do not rename a pin.

The heading is not how a message is matched. Which open pin the user means, and whether a new point is a decision already on the board, comes from the contents of their message and the pin bodies. Do not use answer order. Do not require them to name a heading. Do not open a second pin for a decision already on the board. Two headings that one message would settle are one pin; compare the bodies, not the headings.

Before writing, read every `$DIR/[0-9][0-9]-OUTLINE-*.md` and every `$DIR/[0-9][0-9]-OUTCOME-*.md` in index order. The outline files are the investigation. The latest outcome-mode file is the pin board. No outcome-mode file means there are no pins yet.

A new pin is a choice those outline files leave open that would change the handoff. Do not pin a choice an outline file already settles. No outline file means no new pins. Append new pins after the carried pins. Keep carried pins in the same order.

- A heading on that board whose body does not start with `Resolved,` is open. Include it in this file, in the same order.
- A heading on that board whose body starts with `Resolved,` is closed. Do not include it.
- A heading that an older outcome-mode file had, and that the latest file omits, stays closed. Do not bring it back.
- A file that carries an open pin includes it even when this turn does not mention it.
- When this turn resolves an open pin, keep that heading in this file and set its body to `Resolved, <decision>`. `<decision>` is the choice that will be made. Accepting the recommendation already written in the body is that choice. The next outcome-mode file omits that heading. The decision stays in the file that closed it.

While a pin is open, the body addresses that ambiguity in the implementation: what is undecided, what would settle it, and the option the later handoff should use if the user accepts it. Mark the pin `Blocking` or `Deferrable`. `Blocking` means close it before handoff. `Deferrable` means it can stay open through handoff. Update the body when this turn changes the ambiguity. When nothing changed, copy the previous body.

Do not write a `Resolved,` body while a choice is still open. Settled means the user chose, they accepted the recommendation, or the implementation already decides it.

A turn that leaves the board unchanged — nothing new, nothing updated, nothing resolved — writes no file. Open pins stay on the latest outcome-mode file until a later file carries them.

## Bypass

These skip creating a markdown file but still use the action comment when they are outcome-mode actions. The UTC line stays last.

- **Toggle acks** — the `[outcome-mode]` line, the `$DIR` line, `/handoff-mode`, then the UTC line. A swap that enables outcome-mode is an enable ack.
- **Capacity** — `[outcome-mode] limit reached`, the `$DIR` line, `/handoff-mode`, then the UTC line.
- **No pin change** — trivial one-liners (plain "Yes", "Done", tool-only turns) and any turn that does not open, update, or resolve an ambiguity get no comment line and no file. A short ack that settles an open ambiguity is a write, not a skip. The section in that file is `Resolved, <decision>`.
