---
name: handoff-mode
description: /handoff-mode. Next: /prepare-mode.
disable-model-invocation: true
---

# Handoff mode

`$DIR = ~/.cursor/dynamic-mode/<first-message local YYYY-MM-DD>-<$CURSOR_CONVERSATION_ID>` (no spaces; refuse if the id is unset). Reuse a folder ending in that id; if several, use the earliest date. Do not open a second folder on a later day. Do not pick a folder by a `HANDOFF` sentinel. Order: analyze → clarify → handoff → prepare → takeoff. This mode's only file is `$DIR/03-HANDOFF.md`. The others are `$DIR/01-ANALYZE.md`, `$DIR/02-CLARIFY.md`, `$DIR/04-PREPARE.md`, `$DIR/05-TAKEOFF.md`.
On iff `$DIR/HANDOFF` exists (zero-byte) and `ANALYZE`, `CLARIFY`, `PREPARE`, and `TAKEOFF` do not. Those four are the other mode sentinels; mutually exclusive with this mode. `HANDOFF` also means the implementation is incomplete and not started; prepare and takeoff keep it. `/handoff-mode` toggles; extra words are ignored. `/analyze-mode`, `/clarify-mode`, `/prepare-mode`, and `/takeoff-mode` are not this mode: do not write a file and do not print `[mode]`. Swap deletes the other mode sentinel and creates `HANDOFF`. Off deletes only `HANDOFF`. The markdown stays. Each turn this mode is on, after `$DIR` exists, `shasum -a 256` this `SKILL.md` and compare the 64 hex to `$DIR/handoff-mode.sha256`. If that file is missing or the digest differs, Read this `SKILL.md`, write the 64 hex there, and follow the Read. If it matches, do not Read this file.

H1 only. No frontmatter. No JSON. The first heading starts the file. Blank line after every heading and before every later one. Headings are `# 01 <5-10 word intention>`, then `02`, `03`, in order. A heading keeps its number while it stays. When referring to a file, use one of two: a file in the agent cwd is `lua/libfuns/context.lua:26` (relative, colon, line on the right); a file outside that cwd is its absolute path, colon, line on the right; never `../`. A range is `file.rb:36-53`. Never put the line before the path (`26:file`, `36:53:file`). Keep each path in backticks so neovim `` yi` `` selects them; the cite for a fenced quote is that same backtick path, not the fence language. Quote source inline if it is one line, in a fenced block if it is larger; never as bare lines. Open a fence with backticks only; the first line inside is source.

Ack only for enable, disable, swap, create, or edit. Otherwise no `[mode]` line. Comment: `enabled`, `disabled`, `created a file`, or `edited`. A swap on uses `enabled`. Nothing else. On create or edit, the line after `$DIR` is the numbers of headings whose body was written, comma-separated (`01, 02`). Omit that line when no heading changed.

    [mode] <comment>
    [path] <absolute $DIR>
    [sect] 01, 02
    [next] /prepare-mode
    [dutc] Oct 13, 06:47 PM

The user-facing message is only those five tagged lines. No other chat: no prose, code, findings, or summary. Put the work in the file.
UTC is when the prompt was sent: abbreviated month, day with no leading zero, comma, zero-padded 12-hour clock, AM/PM. No year. No zone.

Do not implement. Do not re-investigate the codebase. While `HANDOFF` exists, create `$DIR/03-HANDOFF.md` when it is absent, including the toggle turn. A later agree or revise edits it. Read `$DIR/02-CLARIFY.md` and write each pin whose first line is `Resolved` into the intention it belongs to. Do not reopen it or list rejected options. "Yes", "OK", "Looks good", and "Do it" accept the discussed intentions and are writes. A revision changes only the intentions the user changed. Tool-only turns write nothing.

Each heading is one intention prepare or takeoff would miss without. The body is prose: what must become true, and why. Do not say how. Do not name components, edit order, calls, or a procedure. Do not say how to read the file. A later heading may depend on an earlier intention being true, not on an earlier edit.
