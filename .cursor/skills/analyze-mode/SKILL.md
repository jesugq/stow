---
name: analyze-mode
description: Toggle with `/analyze-mode`. While on, every substantive reply is written to the next `NN-ANALYZE-<slug>.md` under `$DIR`. Chat prints only the `[analyze-mode]` line, the absolute directory, `/clarify-mode`, and the `[usage-utc-date]` line. No in-chat analysis.
disable-model-invocation: true
---

# Analyze mode

Shared with clarify-mode, handoff-mode, prepare-mode, and takeoff-mode. `$NAME` is `<local YYYY-MM-DD>-<$CURSOR_CONVERSATION_ID>`: the date, one hyphen, then the conversation id, with no spaces. `$DIR = ~/.cursor/dynamic-mode/$NAME` (refuse if the conversation id is unset). Example: `~/.cursor/dynamic-mode/2026-09-24-<id>`. All five modes use this one folder and the same `NN-*.md` sequence. Each mode prefixes its own files: `NN-ANALYZE-<slug>.md`, `NN-CLARIFY-<slug>.md`, `NN-HANDOFF-<slug>.md`, `NN-PREPARE-<slug>.md`, `NN-TAKEOFF-<slug>.md`. The index counts every prefix. `<slug>` does not repeat the mode name. The modes run analyze-mode, then clarify-mode, then handoff-mode, then prepare-mode, then takeoff-mode. The date is the local `YYYY-MM-DD` when the conversation started, taken from its first message. A later turn on another calendar day keeps that same date and the same `$DIR`. If a directory whose name ends in `-$CURSOR_CONVERSATION_ID` already exists under `~/.cursor/dynamic-mode`, that directory is `$DIR`; when more than one exists, use the earliest date. Do not create a second folder because the current turn falls on a later day.

On is `$DIR/ANALYZE` existing (a zero-byte sentinel, not JSON). `$DIR/CLARIFY` means clarify-mode is on instead. `$DIR/HANDOFF` means handoff-mode is on instead. `$DIR/PREPARE` means prepare-mode is on instead. `$DIR/TAKEOFF` means takeoff-mode is on instead. No sentinel means off — a folder or leftover markdown alone is off. The five sentinels are mutually exclusive. `/analyze-mode` toggles this mode; extra words after it are ignored. `/clarify-mode`, `/handoff-mode`, `/prepare-mode`, and `/takeoff-mode` belong to the other skills: do not write a file and do not print an `[analyze-mode]` line for them.

Enabling while `CLARIFY`, `HANDOFF`, `PREPARE`, or `TAKEOFF` exists swaps. Delete those sentinels, create `ANALYZE`, keep every `NN-*.md`, and continue that index. The next substantive reply uses analyze-mode’s shape.

## Action comment

Every analyze-mode action — enabling, disabling, swapping on, creating a file, hitting the 99-file cap — is only these four lines, with a blank line between each:

    [analyze-mode] <short comment>

    <absolute $DIR>

    /clarify-mode

    [usage-utc-date] <UTC time the prompt was sent>

`<short comment>` is `enabled`, `disabled`, `created a file`, or `limit reached`. A swap that turns analyze-mode on uses `enabled`. Nothing else (no titles, analysis, file path, or section bodies). The line after `$DIR` is the next mode to swap to. The last line is the UTC time Cursor records for this model call on the usage dashboard: the time the user sent the prompt, not the time the response finishes. Take that prompt timestamp and convert it to UTC. Format it `[usage-utc-date] Oct 13, 06:47 PM`: the tag, then an abbreviated English month, day with no leading zero, a comma, then a zero-padded 12-hour clock and `AM` or `PM`. No year and no timezone label.

Enable / swap / disable / write:

    [analyze-mode] enabled

    /Users/<you>/.cursor/dynamic-mode/2026-09-24-<id>

    /clarify-mode

    [usage-utc-date] Oct 13, 06:47 PM

## Toggle

- Off → on: create `$DIR` if needed, write `$DIR/ANALYZE`, comment `enabled`, print `$DIR`. If `$DIR/CLARIFY`, `$DIR/HANDOFF`, `$DIR/PREPARE`, or `$DIR/TAKEOFF` exists, delete it first (swap). Keep any existing `NN-*.md`; the next write continues the index, including files the other modes already wrote.
- On → off: delete only `$DIR/ANALYZE`. Leave every markdown file. Comment `disabled`, print `$DIR`.

## Write

While `ANALYZE` exists, each substantive user query creates exactly one new file. Never edit an existing file (follow-ups and revisions are the next index), including files the other modes wrote. Ignore leftover `major-*` / `minor-*` / `*.json` names.

- Next index = `count($DIR/[0-9][0-9]-*.md) + 1`, zero-padded to two digits (`01`, `02`, …).
- Path: `$DIR/<NN>-ANALYZE-<slug>.md`. `<slug>` is kebab-case from a 5–10 word summary of the file (lowercase, hyphens, no spaces). Do not write that summary as a heading. Example: `01-ANALYZE-passkey-login-error-attribution.md`.
- If the next index would be `100`, write nothing and comment `limit reached`. Two-digit prefixes only — `100-*.md` would sort before `99-*.md`.

Shape:

    # <5-10 word title>

    <full section body>

    # ...

As many `#` sections as the reply needs. Never write a `##` heading. A heading that would have been `##` is `#`. No YAML frontmatter. No JSON sidecar. The first heading starts the file (no blank line before it). Blank line after every heading. Blank line before every heading after the first.

## Bypass

These skip creating a markdown file but still use the action comment when they are analyze-mode actions. The UTC line stays last.

- **Toggle acks** — the `[analyze-mode]` line, the `$DIR` line, `/clarify-mode`, then the UTC line. A swap that enables analyze-mode is an enable ack.
- **Capacity** — `[analyze-mode] limit reached`, the `$DIR` line, `/clarify-mode`, then the UTC line.
- **Short prose** — trivial one-liners unrelated to any analyze-mode action (e.g. plain "Yes", "Done", tool-only turns) get no comment line and no file. Use sparingly; anything substantive still goes through analyze mode.
