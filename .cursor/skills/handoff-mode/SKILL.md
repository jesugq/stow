---
name: handoff-mode
description: Toggle with `/handoff-mode`. Enabling does not write a file. The next prompt agrees with the discussed intentions or revises them, then writes the next `NN-HANDOFF-<slug>.md` under `$DIR`. The file is prose about what must become true and why. Chat prints only the `[handoff-mode]` line, the absolute directory, `/prepare-mode`, and the `[usage-utc-date]` line. No in-chat handoffs.
disable-model-invocation: true
---

# Handoff mode

Shared with analyze-mode, clarify-mode, prepare-mode, and takeoff-mode. `$NAME` is `<local YYYY-MM-DD>-<$CURSOR_CONVERSATION_ID>`: the date, one hyphen, then the conversation id, with no spaces. `$DIR = ~/.cursor/dynamic-mode/$NAME` (refuse if the conversation id is unset). Example: `~/.cursor/dynamic-mode/2026-09-24-<id>`. All five modes use this one folder and the same `NN-*.md` sequence. Each mode prefixes its own files: `NN-ANALYZE-<slug>.md`, `NN-CLARIFY-<slug>.md`, `NN-HANDOFF-<slug>.md`, `NN-PREPARE-<slug>.md`, `NN-TAKEOFF-<slug>.md`. The index counts every prefix. `<slug>` does not repeat the mode name. The modes run analyze-mode, then clarify-mode, then handoff-mode, then prepare-mode, then takeoff-mode. The date is the local `YYYY-MM-DD` when the conversation started, taken from its first message. A later turn on another calendar day keeps that same date and the same `$DIR`. If a directory whose name ends in `-$CURSOR_CONVERSATION_ID` already exists under `~/.cursor/dynamic-mode`, that directory is `$DIR`; when more than one exists, use the earliest date. Do not create a second folder because the current turn falls on a later day.

On iff `$DIR/HANDOFF` exists (zero-byte sentinel). `$DIR/ANALYZE` means analyze-mode is on instead. `$DIR/CLARIFY` means clarify-mode is on instead. `$DIR/PREPARE` means prepare-mode is on instead. `$DIR/TAKEOFF` means takeoff-mode is on instead. No sentinel means off — a folder or leftover markdown alone is off. The five sentinels are mutually exclusive. `/handoff-mode` toggles this mode (ignore extra words). `/analyze-mode`, `/clarify-mode`, `/prepare-mode`, and `/takeoff-mode` belong to the other skills: do not write a file and do not print a `[handoff-mode]` line for them.

Enabling while `ANALYZE`, `CLARIFY`, `PREPARE`, or `TAKEOFF` exists swaps. Delete those sentinels, create `HANDOFF`, keep every `NN-*.md`, and continue that index. `/handoff-mode` never writes a `NN-*.md` — only the enable/disable ack.

Chat is only these four lines, with a blank line between each:

    [handoff-mode] <enabled|disabled|created a file|limit reached>

    <absolute $DIR>

    /prepare-mode

    [usage-utc-date] <UTC time the prompt was sent>

The line after `$DIR` is the next mode to swap to. The last line is the UTC time Cursor records for this model call on the usage dashboard: the time the user sent the prompt, not the time the response finishes. Take that prompt timestamp and convert it to UTC. Format it `[usage-utc-date] Oct 13, 06:47 PM`: the tag, then an abbreviated English month, day with no leading zero, a comma, then a zero-padded 12-hour clock and `AM` or `PM`. No year and no timezone label.

Off → on: mkdir `$DIR` if needed, create `HANDOFF`, keep existing `NN-*.md`. If `ANALYZE`, `CLARIFY`, `PREPARE`, or `TAKEOFF` is present, delete it first (swap).
On → off: delete `HANDOFF` only.

While `HANDOFF` exists, the next user prompt (and each later substantive prompt) writes exactly one new `$DIR/<NN>-HANDOFF-<slug>.md` (never edit prior files, including ones the other modes wrote). `NN` = count of `[0-9][0-9]-*.md` + 1, two digits. Slug is kebab-case from a 5–10 word summary of the intentions, not from a heading. Do not write that summary as a heading. Example: `06-HANDOFF-passkey-failures-reach-the-login-funnel.md`. At 100: write nothing and comment `limit reached`.

Context is short by this point. Do not re-investigate the codebase. Read every `$DIR/[0-9][0-9]-CLARIFY-*.md` and carry forward each body that starts with `Resolved,`. Interpret the prompt as one of two cases. Do not implement the work in this conversation.

- **Agree** — the user accepts the discussed intentions (including short acks: "Yes", "OK", "Looks good", "Do it"). Write the handoff from those intentions.
- **Revise** — the user told you to change the intentions. Apply those changes, then write the handoff from the revised intentions.

    # <5-10 word intention>

    <prose: what must become true, and why>

    # ...

Each `#` is one intention. The title names the intention. The body is prose: what must become true, and why. That is the instruction. Do not say how. Do not name components, edit order, calls, or a procedure. Do not tell the receiving agent how to read the file. As many `#` headings as the intentions need. Never write a `##` heading. A heading that would have been `##` is `#`. One intention per heading. A later heading may depend on an earlier intention being true. It does not depend on an earlier edit having been applied.

Write each closed clarify decision into the intention it belongs to. Do not reopen it and do not list rejected options.

No YAML frontmatter. No JSON sidecar. The first heading starts the file (no blank line before it). Blank line after every heading. Blank line before every heading after the first.

Skip the file for toggle/cap acks and tool-only turns. Agreement one-liners are writes, not skips.
