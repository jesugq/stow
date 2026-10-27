---
name: takeoff-mode
description: Toggle with `/takeoff-mode`. While on, every substantive reply is written to the next `NN-<slug>.md` under `$DIR`. Chat prints only the `[takeoff-mode]` line, the absolute directory, and the `[usage-utc-date]` line. No in-chat responses.
disable-model-invocation: true
---

# Takeoff mode

Shared with outline-mode, handoff-mode, and resolve-mode. `$NAME` is `<local YYYY-MM-DD>-<$CURSOR_CONVERSATION_ID>`: the date, one hyphen, then the conversation id, with no spaces. `$DIR = ~/.cursor/dynamic-mode/$NAME` (refuse if the conversation id is unset). Example: `~/.cursor/dynamic-mode/2026-09-24-<id>`. All four modes use this one folder and the same `NN-*.md` sequence. The date is the local `YYYY-MM-DD` when the conversation started, taken from its first message. A later turn on another calendar day keeps that same date and the same `$DIR`. If a directory whose name ends in `-$CURSOR_CONVERSATION_ID` already exists under `~/.cursor/dynamic-mode`, that directory is `$DIR`; when more than one exists, use the earliest date. Do not create a second folder because the current turn falls on a later day.

On iff `$DIR/TAKEOFF` exists (zero-byte sentinel). `$DIR/OUTLINE` means outline-mode is on instead. `$DIR/HANDOFF` means handoff-mode is on instead. `$DIR/RESOLVE` means resolve-mode is on instead. No sentinel means off — a folder or leftover markdown alone is off. The four sentinels are mutually exclusive. `/takeoff-mode` toggles this mode (ignore extra words). `/outline-mode`, `/handoff-mode`, and `/resolve-mode` belong to the other skills: do not write a file and do not print a `[takeoff-mode]` line for them.

Enabling while `OUTLINE`, `HANDOFF`, or `RESOLVE` exists swaps. Delete those sentinels, create `TAKEOFF`, keep every `NN-*.md`, and continue that index. The next substantive reply uses takeoff-mode’s shape.

Chat is only these three lines, with a blank line between each:

    [takeoff-mode] <enabled|disabled|created a file|limit reached>

    <absolute $DIR>

    [usage-utc-date] <UTC time the prompt was sent>

The last line is the UTC time Cursor records for this model call on the usage dashboard: the time the user sent the prompt, not the time the response finishes. Take that prompt timestamp and convert it to UTC. Format it `[usage-utc-date] Oct 13, 06:47 PM`: the tag, then an abbreviated English month, day with no leading zero, a comma, then a zero-padded 12-hour clock and `AM` or `PM`. No year and no timezone label.

Off → on: mkdir `$DIR` if needed, create `TAKEOFF`, keep existing `NN-*.md`. If `OUTLINE`, `HANDOFF`, or `RESOLVE` is present, delete it first (swap).
On → off: delete `TAKEOFF` only.

While `TAKEOFF` exists, each substantive query writes exactly one new `$DIR/<NN>-<slug>.md` (never edit prior files, including ones the other modes wrote). `NN` = count of `[0-9][0-9]-*.md` + 1, two digits. Slug is kebab-case from a 5–10 word summary of the file, not from a section heading. Do not write that summary as a heading. Do not start a slug with `resolve-`. At 100: write nothing and comment `limit reached`.

    # <5-10 word title>

    <full section body>

    # ...

Every heading in the file is an H1. Never write a `##` heading. A heading that would have been `##` is `#`.

The first heading starts the file (no blank line before it). Blank line after every heading. Blank line before every heading after the first.

Each `#` is one thing that was done. The 5–10 word title names that work. The body states what was done. Do not write a decision, an assumption, a product-intent reading, an open question, or an alternate approach. As many `#` sections as the reply needs. Omit a section that has nothing to say.

Skip the file for toggle/cap acks and trivial one-liners ("Yes", "Done", tool-only). Anything substantive still writes a file.
