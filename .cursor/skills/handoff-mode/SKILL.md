---
name: handoff-mode
description: Toggle with `/handoff-mode`. Enabling does not write a file. The next prompt agrees with the discussed implementation or revises it, then writes the next `NN-<slug>.md` under `$DIR`; chat only names the folder and the new file. No in-chat handoffs.
disable-model-invocation: true
---

# Handoff mode

Shared with outline-mode, takeoff-mode, and mermaid-mode. `$NAME` is `<local YYYY-MM-DD>-<$CURSOR_CONVERSATION_ID>`: the date, one hyphen, then the conversation id, with no spaces. `$DIR = ~/.cursor/dynamic-mode/$NAME` (refuse if the conversation id is unset). Example: `~/.cursor/dynamic-mode/2026-09-24-<id>`. All four modes use this one folder and the same `NN-*.md` sequence. The date is the local calendar date at the start of the turn; the same day and conversation always resolve to the same `$DIR`.

On iff `$DIR/HANDOFF` exists (zero-byte sentinel). `$DIR/OUTLINE` means outline-mode is on instead. `$DIR/TAKEOFF` means takeoff-mode is on instead. `$DIR/MERMAID` means mermaid-mode is on instead. Neither sentinel means off — a folder or leftover markdown alone is off. The four sentinels are mutually exclusive. `/handoff-mode` toggles this mode (ignore extra words). `/outline-mode`, `/takeoff-mode`, and `/mermaid-mode` belong to the other skills: do not write a file and do not print a handoff-mode comment for them.

Enabling while `OUTLINE`, `TAKEOFF`, or `MERMAID` exists swaps. Delete those sentinels, create `HANDOFF`, keep every `NN-*.md`, and continue that index. `/handoff-mode` never writes a `NN-*.md` — only the enable/disable ack.

Chat is only:

    [handoff-mode] <enabled|disabled|created a file|limit reached>
    <absolute $DIR>
    [<absolute new file, write turns only>]

Off → on: mkdir `$DIR` if needed, create `HANDOFF`, keep existing `NN-*.md`. If `OUTLINE`, `TAKEOFF`, or `MERMAID` is present, delete it first (swap).
On → off: delete `HANDOFF` only.

While `HANDOFF` exists, the next user prompt (and each later substantive prompt) writes exactly one new `$DIR/<NN>-<slug>.md` (never edit prior files, including ones the other modes wrote). `NN` = count of `[0-9][0-9]-*.md` + 1, two digits. Slug is kebab-case from a 5–10 word summary of the conversation’s task (H1 is always `Instructions`, so do not slug from the H1). At 100: write nothing, comment `limit reached`, tell the user to start a new conversation.

Interpret that prompt as one of two cases. Do not implement the work in this conversation.

- **Agree** — the user accepts the discussed implementation (including short acks: "Yes", "OK", "Looks good", "Do it"). Write the handoff from that implementation as discussed.
- **Revise** — the user told you to change the implementation. Apply those changes to the plan, then write the handoff from the revised implementation.

    # Instructions

    <instructions for the next agent>

    ## <5-10 word incremental change>

    <full section body>

    ## ...

`# Instructions` is always the first heading and always that title. Its body is for the agent receiving this file. It must tell that agent to stop after applying or reading each heading, even when the heading is only internal — `# Instructions` itself is internal: read it, then stop. Resume with the next heading only when asked. It must also tell that agent to readjust the implementation from changes the user made, and to do that internally: keep the revision at the top of its mind and change later steps to match, instead of updating documentation the user may or may not have provided. Each later heading is one small, reviewable change; apply or read that heading only, then stop again.

Each `##` is one small, reviewable, incremental change that builds on the previous heading and together completes the task from the conversation. Outline-mode shape: 5–10 word title, then a full section body. As many `##` headings as the task needs. One change per heading; do not bundle unrelated work. Order them so a later heading never depends on work a prior heading has not applied.

No YAML frontmatter. No JSON sidecar. The H1 starts the file (no blank line before it). Blank line after every heading, including `#`. Blank line before every `##`.

Skip the file for toggle/cap acks and tool-only turns. Agreement one-liners are writes, not skips.
