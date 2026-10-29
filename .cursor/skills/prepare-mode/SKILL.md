---
name: prepare-mode
description: /prepare-mode. Next: /takeoff-mode.
disable-model-invocation: true
---

# Prepare mode

`$DIR = ~/.cursor/dynamic-mode/<first-message local YYYY-MM-DD>-<$CURSOR_CONVERSATION_ID>` (no spaces; refuse if the id is unset). Reuse a folder ending in that id; if several, use the earliest date. Do not open a second folder on a later day. Order: analyze → clarify → handoff → prepare → takeoff. This mode's only file is `$DIR/PREPARE.md`. The others are `$DIR/ANALYZE.md`, `$DIR/CLARIFY.md`, `$DIR/HANDOFF.md`, `$DIR/TAKEOFF.md`.
On iff `$DIR/PREPARE` exists (zero-byte). Other sentinels: `ANALYZE`, `CLARIFY`, `HANDOFF`, `TAKEOFF`. Mutually exclusive; none means off. `/prepare-mode` toggles; extra words are ignored. `/analyze-mode`, `/clarify-mode`, `/handoff-mode`, and `/takeoff-mode` are not this mode: do not write a file and do not print `[prepare-mode]`. Swap deletes the other sentinel and creates `PREPARE`. Off deletes only `PREPARE`. The markdown stays.

H1 only. No frontmatter. No JSON. The first heading starts the file. Blank line after every heading and before every later one. Headings are `# 01 <5-10 word choice>`, then `02`, `03`, in order. A heading keeps its number while it stays.

Ack only for enable, disable, swap, create, or edit. Otherwise no `[prepare-mode]` line. Blank line between each line. Comment: `enabled`, `disabled`, `created a file`, or `edited`. A swap on uses `enabled`. Nothing else. On create or edit, the line after `$DIR` is the numbers of headings whose body was written, comma-separated (`01, 02`). Omit that line when no heading changed.

    [prepare-mode] <comment>

    <absolute $DIR>

    01, 02

    /takeoff-mode

    [usage-utc-date] Oct 13, 06:47 PM

UTC is when the prompt was sent: abbreviated month, day with no leading zero, comma, zero-padded 12-hour clock, AM/PM. No year. No zone.

Do not implement. While `PREPARE` exists, a turn that opens, updates, or resolves a way to build edits `$DIR/PREPARE.md`. Create it only when it is absent. One choice per heading. Change only the pins this turn opens, updates, or resolves. No board change: no ack and no file. A short ack that settles a pin is an edit.

Read `$DIR/HANDOFF.md`, `$DIR/CLARIFY.md`, and `$DIR/PREPARE.md`. The handoff is what must become true and why. A clarify `Resolved,` body is closed; do not reopen it. The prepare file is the board; absent means no pins. Look at the codebase only to see which existing way would satisfy the handoff.

A new pin is a way of building the handoff leaves open that would change what takeoff edits. Do not pin a product intention, or a choice the handoff or a closed clarify decision already settles. No handoff file means no new pins.

The heading text after the number is the tab. Reuse it exactly. Match the user's message to pin bodies, not heading text or answer order. One message that would settle two headings is one pin. Open means the body does not start with `Resolved,`. Closing sets that body to `Resolved, <decision>`, the way takeoff will build, including an accepted recommendation, and leaves the heading in the file.

An open body says what is undecided about how to build, what would settle it, and the way takeoff should build if accepted. Prefer a way the codebase already uses when it satisfies the handoff. Mark `Blocking` (close before takeoff) or `Deferrable` (may stay open through takeoff). Do not write `Resolved,` while a choice is open. Settled means the user chose, accepted the recommendation, or the codebase has only one way that satisfies the handoff.
