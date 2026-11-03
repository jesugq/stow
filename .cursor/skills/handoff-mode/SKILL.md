---
name: handoff-mode
description: /handoff-mode. Next: /prepare-mode.
disable-model-invocation: true
---

# Handoff mode

`$DIR = ~/.cursor/dynamic-mode/<first-message local YYYY-MM-DD>-<$CURSOR_CONVERSATION_ID>` (no spaces; refuse if the id is unset). Reuse a folder ending in that id; if several, use the earliest date. Do not open a second folder on a later day. Order: analyze → clarify → handoff → prepare → takeoff. This mode's only file is `$DIR/03-HANDOFF.md`. The others are `$DIR/01-ANALYZE.md`, `$DIR/02-CLARIFY.md`, `$DIR/04-PREPARE.md`, `$DIR/05-TAKEOFF.md`.
On iff `$DIR/HANDOFF` exists (zero-byte). Other sentinels: `ANALYZE`, `CLARIFY`, `PREPARE`, `TAKEOFF`. Mutually exclusive; none means off. `/handoff-mode` toggles; extra words are ignored. `/analyze-mode`, `/clarify-mode`, `/prepare-mode`, and `/takeoff-mode` are not this mode: do not write a file and do not print `[mode]`. Swap deletes the other sentinel and creates `HANDOFF`. Off deletes only `HANDOFF`. The markdown stays.

H1 only. No frontmatter. No JSON. The first heading starts the file. Blank line after every heading and before every later one. Headings are `# 01 <5-10 word intention>`, then `02`, `03`, in order. A heading keeps its number while it stays. A file in the agent cwd is `lua/libfuns/context.lua:26` (relative, colon, line). A file outside that cwd is its absolute path, colon, line; never `../`. A component is `context.lua` (filename with extension, not a classname). Keep each in backticks so neovim `` yi` `` selects them.

Ack only for enable, disable, swap, create, or edit. Otherwise no `[mode]` line. Comment: `enabled`, `disabled`, `created a file`, or `edited`. A swap on uses `enabled`. Nothing else. On create or edit, the line after `$DIR` is the numbers of headings whose body was written, comma-separated (`01, 02`). Omit that line when no heading changed.

    [mode] <comment>
    [path] <absolute $DIR>
    [sect] 01, 02
    [next] /prepare-mode
    [dutc] Oct 13, 06:47 PM

The user-facing message is only those five tagged lines. No other chat: no prose, code, findings, or summary. Put the work in the file.
UTC is when the prompt was sent: abbreviated month, day with no leading zero, comma, zero-padded 12-hour clock, AM/PM. No year. No zone.

The toggle writes no markdown. Do not implement. Do not re-investigate the codebase. The next prompt creates `$DIR/03-HANDOFF.md`; a later agree or revise edits it. Read `$DIR/02-CLARIFY.md` and write each pin whose first line is `Resolved` into the intention it belongs to. Do not reopen it or list rejected options. "Yes", "OK", "Looks good", and "Do it" accept the discussed intentions and are writes. A revision changes only the intentions the user changed. Tool-only turns write nothing.

Each heading is one intention prepare or takeoff would miss without. The body is prose: what must become true, and why. Do not say how. Do not name components, edit order, calls, or a procedure. Do not say how to read the file. A later heading may depend on an earlier intention being true, not on an earlier edit.
