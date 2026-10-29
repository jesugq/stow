---
name: clarify-mode
description: /clarify-mode. Next: /handoff-mode.
disable-model-invocation: true
---

# Clarify mode

`$DIR = ~/.cursor/dynamic-mode/<first-message local YYYY-MM-DD>-<$CURSOR_CONVERSATION_ID>` (no spaces; refuse if the id is unset). Reuse a folder ending in that id; if several, use the earliest date. Do not open a second folder on a later day. Order: analyze → clarify → handoff → prepare → takeoff. This mode's only file is `$DIR/CLARIFY.md`. The others are `$DIR/ANALYZE.md`, `$DIR/HANDOFF.md`, `$DIR/PREPARE.md`, `$DIR/TAKEOFF.md`.
On iff `$DIR/CLARIFY` exists (zero-byte). Other sentinels: `ANALYZE`, `HANDOFF`, `PREPARE`, `TAKEOFF`. Mutually exclusive; none means off. `/clarify-mode` toggles; extra words are ignored. `/analyze-mode`, `/handoff-mode`, `/prepare-mode`, and `/takeoff-mode` are not this mode: do not write a file and do not print `[clarify-mode]`. Swap deletes the other sentinel and creates `CLARIFY`. Off deletes only `CLARIFY`. The markdown stays.

H1 only. No frontmatter. No JSON. The first heading starts the file. Blank line after every heading and before every later one. Headings are `# 01 <5-10 word ambiguity>`, then `02`, `03`, in order. A heading keeps its number while it stays.

Ack only for enable, disable, swap, create, or edit. Otherwise no `[clarify-mode]` line. Blank line between each line. Comment: `enabled`, `disabled`, `created a file`, or `edited`. A swap on uses `enabled`. Nothing else. On create or edit, the line after `$DIR` is the numbers of headings whose body was written, comma-separated (`01, 02`). Omit that line when no heading changed.

    [clarify-mode] <comment>

    <absolute $DIR>

    01, 02

    /handoff-mode

    [usage-utc-date] Oct 13, 06:47 PM

UTC is when the prompt was sent: abbreviated month, day with no leading zero, comma, zero-padded 12-hour clock, AM/PM. No year. No zone.

While `CLARIFY` exists, a turn that opens, updates, or resolves an ambiguity edits `$DIR/CLARIFY.md`. Create it only when it is absent. One ambiguity per heading. Change only the pins this turn opens, updates, or resolves. No board change: no ack and no file. A short ack that settles a pin is an edit.

Read `$DIR/ANALYZE.md` and `$DIR/CLARIFY.md`. The analyze file is the investigation. The clarify file is the board; absent means no pins. A new pin is a choice the analyze file leaves open that would change the handoff. Do not pin what it already settles. No analyze file means no new pins. Leave code structure for prepare.

The heading text after the number is the tab. Reuse it exactly. Match the user's message to pin bodies, not heading text or answer order. One message that would settle two headings is one pin. Open means the body does not start with `Resolved,`. Closing sets that body to `Resolved, <decision>`, including an accepted recommendation, and leaves the heading in the file.

An open body says what is undecided in the handoff intention, what would settle it, and the option the handoff should use if accepted. Mark `Blocking` (close before handoff) or `Deferrable` (may stay open through handoff). Do not write `Resolved,` while a choice is open. Settled means the user chose, accepted the recommendation, or the implementation already decides it.
