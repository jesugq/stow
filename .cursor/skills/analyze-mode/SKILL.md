---
name: analyze-mode
description: /analyze-mode. Next: /clarify-mode.
disable-model-invocation: true
---

# Analyze mode

`$DIR = ~/.cursor/dynamic-mode/<first-message local YYYY-MM-DD>-<$CURSOR_CONVERSATION_ID>` (no spaces; refuse if the id is unset). Reuse a folder ending in that id; if several, use the earliest date. Do not open a second folder on a later day. Order: analyze → clarify → handoff → prepare → takeoff. This mode's only file is `$DIR/ANALYZE.md`. The others are `$DIR/CLARIFY.md`, `$DIR/HANDOFF.md`, `$DIR/PREPARE.md`, `$DIR/TAKEOFF.md`.
On iff `$DIR/ANALYZE` exists (zero-byte). Other sentinels: `CLARIFY`, `HANDOFF`, `PREPARE`, `TAKEOFF`. Mutually exclusive; none means off. `/analyze-mode` toggles; extra words are ignored. `/clarify-mode`, `/handoff-mode`, `/prepare-mode`, and `/takeoff-mode` are not this mode: do not write a file and do not print `[analyze-mode]`. Swap deletes the other sentinel and creates `ANALYZE`. Off deletes only `ANALYZE`. The markdown stays.

H1 only. No frontmatter. No JSON. The first heading starts the file. Blank line after every heading and before every later one. Headings are `# 01 <5-10 word title>`, then `02`, `03`, in order. A heading keeps its number while it stays.

Ack only for enable, disable, swap, create, or edit. Otherwise no `[analyze-mode]` line. Blank line between each line. Comment: `enabled`, `disabled`, `created a file`, or `edited`. A swap on uses `enabled`. Nothing else. On create or edit, the line after `$DIR` is the numbers of headings whose body was written, comma-separated (`01, 02`). Omit that line when no heading changed.

    [analyze-mode] <comment>

    <absolute $DIR>

    01, 02

    /clarify-mode

    [usage-utc-date] Oct 13, 06:47 PM

UTC is when the prompt was sent: abbreviated month, day with no leading zero, comma, zero-padded 12-hour clock, AM/PM. No year. No zone.

While `ANALYZE` exists, create `$DIR/ANALYZE.md` on the first substantive query and edit it after that. Each heading is one finding clarify would decide differently without. Add or replace only that heading. Do not rewrite an unchanged heading, and do not write the rest of the investigation. "Yes", "Done", and tool-only turns that are not this mode: no ack and no file.
