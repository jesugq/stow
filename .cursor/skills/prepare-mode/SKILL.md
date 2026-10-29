---
name: prepare-mode
description: Toggle with `/prepare-mode`. While on, choices about how to build are written to the next `NN-PREPARE-<slug>.md` under `$DIR`, one choice per `#` section. Each section is a browser tab pin and stays in later prepare-mode files until it is resolved, when its body is `Resolved, <decision>` and later files omit it. Chat prints only the `[prepare-mode]` line, the absolute directory, `/takeoff-mode`, and the `[usage-utc-date]` line when a file or toggle ack is produced. No in-chat resolutions.
disable-model-invocation: true
---

# Prepare mode

Shared with analyze-mode, clarify-mode, handoff-mode, and takeoff-mode. `$NAME` is `<local YYYY-MM-DD>-<$CURSOR_CONVERSATION_ID>`: the date, one hyphen, then the conversation id, with no spaces. `$DIR = ~/.cursor/dynamic-mode/$NAME` (refuse if the conversation id is unset). Example: `~/.cursor/dynamic-mode/2026-09-24-<id>`. All five modes use this one folder and the same `NN-*.md` sequence. Each mode prefixes its own files: `NN-ANALYZE-<slug>.md`, `NN-CLARIFY-<slug>.md`, `NN-HANDOFF-<slug>.md`, `NN-PREPARE-<slug>.md`, `NN-TAKEOFF-<slug>.md`. The index counts every prefix. `<slug>` does not repeat the mode name. The modes run analyze-mode, then clarify-mode, then handoff-mode, then prepare-mode, then takeoff-mode. The date is the local `YYYY-MM-DD` when the conversation started, taken from its first message. A later turn on another calendar day keeps that same date and the same `$DIR`. If a directory whose name ends in `-$CURSOR_CONVERSATION_ID` already exists under `~/.cursor/dynamic-mode`, that directory is `$DIR`; when more than one exists, use the earliest date. Do not create a second folder because the current turn falls on a later day.

On iff `$DIR/PREPARE` exists (zero-byte sentinel). `$DIR/ANALYZE` means analyze-mode is on instead. `$DIR/CLARIFY` means clarify-mode is on instead. `$DIR/HANDOFF` means handoff-mode is on instead. `$DIR/TAKEOFF` means takeoff-mode is on instead. No sentinel means off — a folder or leftover markdown alone is off. The five sentinels are mutually exclusive. `/prepare-mode` toggles this mode (ignore extra words). `/analyze-mode`, `/clarify-mode`, `/handoff-mode`, and `/takeoff-mode` belong to the other skills: do not write a file and do not print a `[prepare-mode]` line for them.

Enabling while `ANALYZE`, `CLARIFY`, `HANDOFF`, or `TAKEOFF` exists swaps. Delete those sentinels, create `PREPARE`, keep every `NN-*.md`, and continue that index. The next choice about how to build uses prepare-mode’s shape. Do not implement the work in this conversation.

Chat is only these four lines, with a blank line between each, when this turn writes a file, enables, disables, swaps, or hits the cap. When this turn does none of those, answer in chat and do not print a `[prepare-mode]` line.

    [prepare-mode] <enabled|disabled|created a file|limit reached>

    <absolute $DIR>

    /takeoff-mode

    [usage-utc-date] <UTC time the prompt was sent>

`<short comment>` is one of those four words. A swap that turns prepare-mode on uses `enabled`. Nothing else (no titles, choices, file path, or section bodies). The line after `$DIR` is the next mode to swap to. The last line is the UTC time Cursor records for this model call on the usage dashboard: the time the user sent the prompt, not the time the response finishes. Take that prompt timestamp and convert it to UTC. Format it `[usage-utc-date] Oct 13, 06:47 PM`: the tag, then an abbreviated English month, day with no leading zero, a comma, then a zero-padded 12-hour clock and `AM` or `PM`. No year and no timezone label.

Off → on: mkdir `$DIR` if needed, create `PREPARE`, keep existing `NN-*.md`. If `ANALYZE`, `CLARIFY`, `HANDOFF`, or `TAKEOFF` is present, delete it first (swap).
On → off: delete `PREPARE` only.

While `PREPARE` exists, a turn that opens a way-to-build, updates one, or resolves one writes exactly one new `$DIR/<NN>-PREPARE-<slug>.md` (never edit prior files, including ones the other modes wrote). `NN` = count of `[0-9][0-9]-*.md` + 1, two digits. The `PREPARE` prefix is required so later turns can find the pin board. Slug is kebab-case from a 5–10 word summary of the file (lowercase, hyphens, no spaces). Do not write that summary as a heading. Example: `07-PREPARE-extend-the-existing-login-tracker.md`. At 100: write nothing and comment `limit reached`.

Before writing, read every `$DIR/[0-9][0-9]-HANDOFF-*.md`, every `$DIR/[0-9][0-9]-CLARIFY-*.md`, and every `$DIR/[0-9][0-9]-PREPARE-*.md`. The latest handoff file is what must become true and why. A body that starts with `Resolved,` in a clarify file is closed. Do not reopen it. The latest prepare file is the pin board. No prepare file means there are no pins yet. Look at the codebase only to see which existing way would satisfy the handoff.

Shape — one way-to-build per section. Never write a `##` heading. A heading that would have been `##` is `#`. No YAML frontmatter. No JSON sidecar. The first heading starts the file (no blank line before it). Blank line after every heading. Blank line before every heading after the first.

    # <5-10 word choice>

    <full section body>

    # ...

Each `#` section is one choice and one browser tab pin. The heading text is the tab label. Reuse it character for character while the pin stays. Do not rename a pin.

The heading is not how a message is matched. Which open pin the user means, and whether a new point is a choice already on the board, comes from the contents of their message and the pin bodies. Do not use answer order. Do not require them to name a heading. Do not open a second pin for a choice already on the board. Two headings that one message would settle are one pin; compare the bodies, not the headings.

A new pin is a way of building the handoff leaves open, where more than one way would change what takeoff edits. Do not pin a product intention. Do not pin a choice the handoff or a closed clarify decision already settles. No handoff file means no new pins. Append new pins after the carried pins. Keep carried pins in the same order.

- A heading on that board whose body does not start with `Resolved,` is open. Include it in this file, in the same order.
- A heading on that board whose body starts with `Resolved,` is closed. Do not include it.
- A heading that an older prepare-mode file had, and that the latest file omits, stays closed. Do not bring it back.
- A file that carries an open pin includes it even when this turn does not mention it.
- When this turn resolves an open pin, keep that heading in this file and set its body to `Resolved, <decision>`. `<decision>` is the way takeoff will build. Accepting the recommendation already written in the body is that choice. The next prepare-mode file omits that heading. The decision stays in the file that closed it.

While a pin is open, the body says what is undecided about how to build, what would settle it, and the way takeoff should build if the user accepts it. Prefer a way the codebase already uses when that way satisfies the handoff. Mark the pin `Blocking` or `Deferrable`. `Blocking` means close it before takeoff. `Deferrable` means it can stay open through takeoff. Update the body when this turn changes the choice. When nothing changed, copy the previous body.

Do not write a `Resolved,` body while a choice is still open. Settled means the user chose, they accepted the recommendation, or the codebase already has only one way that satisfies the handoff.

A turn that leaves the board unchanged — nothing new, nothing updated, nothing resolved — writes no file. Open pins stay on the latest prepare-mode file until a later file carries them.

Skip the file for toggle acks, the cap, and any turn that does not open, update, or resolve a choice. Those toggle and cap turns still print the four-line comment, and the UTC line stays last. A short ack that settles an open choice is a write, not a skip. The section in that file is `Resolved, <decision>`.
