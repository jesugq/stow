---
name: handoff-mode
description: /handoff-mode. Next: /prepare-mode.
disable-model-invocation: true
---

# Handoff mode

`$DIR = ~/.cursor/dynamic-mode/<first-message local YYYY-MM-DD>-<$CURSOR_CONVERSATION_ID>` (no spaces; refuse if the id is unset). Reuse a folder ending in that id; if several, use the earliest date. Do not open a second folder on a later day. Order: analyze → clarify → handoff → prepare → takeoff. This mode's only file is `$DIR/HANDOFF.md`. The others are `$DIR/ANALYZE.md`, `$DIR/CLARIFY.md`, `$DIR/PREPARE.md`, `$DIR/TAKEOFF.md`.
On iff `$DIR/HANDOFF` exists (zero-byte). Other sentinels: `ANALYZE`, `CLARIFY`, `PREPARE`, `TAKEOFF`. Mutually exclusive; none means off. `/handoff-mode` toggles; extra words are ignored. `/analyze-mode`, `/clarify-mode`, `/prepare-mode`, and `/takeoff-mode` are not this mode: do not write a file and do not print `[handoff-mode]`. Swap deletes the other sentinel and creates `HANDOFF`. Off deletes only `HANDOFF`. The markdown stays.

H1 only. No frontmatter. No JSON. The first heading starts the file. Blank line after every heading and before every later one. Headings are `# 01 <5-10 word intention>`, then `02`, `03`, in order. A heading keeps its number while it stays.

Ack only for enable, disable, swap, create, or edit. Otherwise no `[handoff-mode]` line. Blank line between each line. Comment: `enabled`, `disabled`, `created a file`, or `edited`. A swap on uses `enabled`. Nothing else. On create or edit, the line after `$DIR` is the numbers of headings whose body was written, comma-separated (`01, 02`). Omit that line when no heading changed.

    [handoff-mode] <comment>

    <absolute $DIR>

    01, 02

    /prepare-mode

    [usage-utc-date] Oct 13, 06:47 PM

UTC is when the prompt was sent: abbreviated month, day with no leading zero, comma, zero-padded 12-hour clock, AM/PM. No year. No zone.

The toggle writes no markdown. Do not implement. Do not re-investigate the codebase. The next prompt creates `$DIR/HANDOFF.md`; a later agree or revise edits it. Read `$DIR/CLARIFY.md` and write each `Resolved,` decision into the intention it belongs to. Do not reopen it or list rejected options. "Yes", "OK", "Looks good", and "Do it" accept the discussed intentions and are writes. A revision changes only the intentions the user changed. Tool-only turns write nothing.

Each heading is one intention prepare or takeoff would miss without. The body is prose: what must become true, and why. Do not say how. Do not name components, edit order, calls, or a procedure. Do not say how to read the file. A later heading may depend on an earlier intention being true, not on an earlier edit.
