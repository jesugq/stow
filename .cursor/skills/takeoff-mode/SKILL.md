---
name: takeoff-mode
description: Toggle with `/takeoff-mode`. While on, every substantive reply is written to the next `NN-TAKEOFF-<slug>.md` under `$DIR`. Prepare has chosen how. This mode does the work. Chat prints only the `[takeoff-mode]` line, the absolute directory, `no follow up mode`, and the `[usage-utc-date]` line. No in-chat responses.
disable-model-invocation: true
---

# Takeoff mode

Shared with analyze-mode, clarify-mode, handoff-mode, and prepare-mode. `$NAME` is `<local YYYY-MM-DD>-<$CURSOR_CONVERSATION_ID>`: the date, one hyphen, then the conversation id, with no spaces. `$DIR = ~/.cursor/dynamic-mode/$NAME` (refuse if the conversation id is unset). Example: `~/.cursor/dynamic-mode/2026-09-24-<id>`. All five modes use this one folder and the same `NN-*.md` sequence. Each mode prefixes its own files: `NN-ANALYZE-<slug>.md`, `NN-CLARIFY-<slug>.md`, `NN-HANDOFF-<slug>.md`, `NN-PREPARE-<slug>.md`, `NN-TAKEOFF-<slug>.md`. The index counts every prefix. `<slug>` does not repeat the mode name. The modes run analyze-mode, then clarify-mode, then handoff-mode, then prepare-mode, then takeoff-mode. The date is the local `YYYY-MM-DD` when the conversation started, taken from its first message. A later turn on another calendar day keeps that same date and the same `$DIR`. If a directory whose name ends in `-$CURSOR_CONVERSATION_ID` already exists under `~/.cursor/dynamic-mode`, that directory is `$DIR`; when more than one exists, use the earliest date. Do not create a second folder because the current turn falls on a later day.

On iff `$DIR/TAKEOFF` exists (zero-byte sentinel). `$DIR/ANALYZE` means analyze-mode is on instead. `$DIR/CLARIFY` means clarify-mode is on instead. `$DIR/HANDOFF` means handoff-mode is on instead. `$DIR/PREPARE` means prepare-mode is on instead. No sentinel means off — a folder or leftover markdown alone is off. The five sentinels are mutually exclusive. `/takeoff-mode` toggles this mode (ignore extra words). `/analyze-mode`, `/clarify-mode`, `/handoff-mode`, and `/prepare-mode` belong to the other skills: do not write a file and do not print a `[takeoff-mode]` line for them.

Enabling while `ANALYZE`, `CLARIFY`, `HANDOFF`, or `PREPARE` exists swaps. Delete those sentinels, create `TAKEOFF`, keep every `NN-*.md`, and continue that index. The next substantive reply uses takeoff-mode’s shape.

Chat is only these four lines, with a blank line between each:

    [takeoff-mode] <enabled|disabled|created a file|limit reached>

    <absolute $DIR>

    no follow up mode

    [usage-utc-date] <UTC time the prompt was sent>

The line after `$DIR` is `no follow up mode`. The last line is the UTC time Cursor records for this model call on the usage dashboard: the time the user sent the prompt, not the time the response finishes. Take that prompt timestamp and convert it to UTC. Format it `[usage-utc-date] Oct 13, 06:47 PM`: the tag, then an abbreviated English month, day with no leading zero, a comma, then a zero-padded 12-hour clock and `AM` or `PM`. No year and no timezone label.

Off → on: mkdir `$DIR` if needed, create `TAKEOFF`, keep existing `NN-*.md`. If `ANALYZE`, `CLARIFY`, `HANDOFF`, or `PREPARE` is present, delete it first (swap).
On → off: delete `TAKEOFF` only.

While `TAKEOFF` exists, each substantive query writes exactly one new `$DIR/<NN>-TAKEOFF-<slug>.md` (never edit prior files, including ones the other modes wrote). `NN` = count of `[0-9][0-9]-*.md` + 1, two digits. Slug is kebab-case from a 5–10 word summary of the file, not from a section heading. Do not write that summary as a heading. Example: `08-TAKEOFF-forwarded-passkey-failure-reasons.md`. At 100: write nothing and comment `limit reached`.

Before changing the product, read every `$DIR/[0-9][0-9]-HANDOFF-*.md`, every `$DIR/[0-9][0-9]-CLARIFY-*.md`, and every `$DIR/[0-9][0-9]-PREPARE-*.md`. The latest handoff file is what must become true and why. A `Resolved,` body in a clarify file wins over a conflicting handoff sentence. No prepare file means do not invent the architecture. A `Resolved,` body in the latest prepare file is how to build it. Follow that way. Do not pick a different one. If that prepare file still has an open pin marked `Blocking`, do not invent the choice. Record the stop, and do only the work that does not depend on it.

    # <5-10 word title>

    <what was done>

    # ...

Every heading in the file is an H1. Never write a `##` heading. A heading that would have been `##` is `#`.

The first heading starts the file (no blank line before it). Blank line after every heading. Blank line before every heading after the first.

Each `#` is one thing that was done. The 5–10 word title names that work. The body states what was done, including the approach that was used, as fact. Do not write an option that was not taken, an open question, or a restatement of the handoff. As many `#` sections as the reply needs. Omit a section that has nothing to say.

The first turn that applies the handoff records these headings, in this order. The product work sits between the Linear check and the nitpick. A later turn records only the new work.

- The first `#` checks that Linear is authenticated and a Linear URL was provided. Check the `linear` MCP namespace: `needsAuth` means Linear is not authenticated. Record the URL when one was provided. If Linear is not authenticated, or no Linear URL was provided, refuse to proceed and stop this file after that heading.
- The second-to-last `#` reads that Linear issue and records which of its title, description, and comments the change may have missed.
- The last `#` runs Cursor's Bugbot on the changes. Follow the `review-bugbot` skill: launch the `bugbot` subagent (`description: "Bugbot"`, `subagent_type: "bugbot"`, `run_in_background: false`) with `Full Repository Path` set to the absolute git repository and `Diff: branch changes`, unless the user asked for uncommitted changes only. Record every finding and how to fix it. Do not edit code or otherwise apply those fixes.

Skip the file for toggle/cap acks and trivial one-liners ("Yes", "Done", tool-only). Anything substantive still writes a file.
