---
name: takeoff-mode
description: Toggle with `/takeoff-mode`. While on, every substantive reply is written to the next `NN-<slug>.md` under `$DIR`; chat only names the folder and the new file. No in-chat responses.
disable-model-invocation: true
---

# Takeoff mode

Shared with outline-mode and handoff-mode. `$NAME` is `<local YYYY-MM-DD>-<$CURSOR_CONVERSATION_ID>`: the date, one hyphen, then the conversation id, with no spaces. `$DIR = ~/.cursor/dynamic-mode/$NAME` (refuse if the conversation id is unset). Example: `~/.cursor/dynamic-mode/2026-09-24-<id>`. All three modes use this one folder and the same `NN-*.md` sequence. The date is the local `YYYY-MM-DD` when the conversation started, taken from its first message. A later turn on another calendar day keeps that same date and the same `$DIR`. If a directory whose name ends in `-$CURSOR_CONVERSATION_ID` already exists under `~/.cursor/dynamic-mode`, that directory is `$DIR`; when more than one exists, use the earliest date. Do not create a second folder because the current turn falls on a later day.

On iff `$DIR/TAKEOFF` exists (zero-byte sentinel). `$DIR/OUTLINE` means outline-mode is on instead. `$DIR/HANDOFF` means handoff-mode is on instead. Neither sentinel means off — a folder or leftover markdown alone is off. The three sentinels are mutually exclusive. `/takeoff-mode` toggles this mode (ignore extra words). `/outline-mode` and `/handoff-mode` belong to the other skills: do not write a file and do not print a takeoff-mode comment for them.

Enabling while `OUTLINE` or `HANDOFF` exists swaps. Delete those sentinels, create `TAKEOFF`, keep every `NN-*.md`, and continue that index. The next substantive reply uses takeoff-mode’s shape.

Chat is only these sections, with a blank line between each:

    [takeoff-mode] <enabled|disabled|created a file|limit reached>

    <absolute $DIR>

    [<absolute new file, write turns only>]

    [usage-utc-date] <UTC time the prompt was sent>

The last line is the UTC time Cursor records for this model call on the usage dashboard: the time the user sent the prompt, not the time the response finishes. Take that prompt timestamp and convert it to UTC. Format it `[usage-utc-date] Oct 13, 06:47 PM`: the tag, then an abbreviated English month, day with no leading zero, a comma, then a zero-padded 12-hour clock and `AM` or `PM`. No year and no timezone label.

Off → on: mkdir `$DIR` if needed, create `TAKEOFF`, keep existing `NN-*.md`. If `OUTLINE` or `HANDOFF` is present, delete it first (swap).
On → off: delete `TAKEOFF` only.

While `TAKEOFF` exists, each substantive query writes exactly one new `$DIR/<NN>-<slug>.md` (never edit prior files, including ones outline-mode or handoff-mode wrote). `NN` = count of `[0-9][0-9]-*.md` + 1, two digits. Slug is kebab-case from the opening summary heading, not from `# Response`, `# Adjustment`, `# Commands`, `# Next step`, or a later topic heading. At 100: write nothing, comment `limit reached`, tell the user to start a new conversation.

    # <5-10 word summary>

    # Response

    <the full chat reply>

    # Adjustment

    <what this step changed relative to the original plan>

    # Commands

    ```
    <this response’s assertion commands, then every earlier assertion command, oldest first>
    ```

    # <5-10 word title>

    <full section body>

    # ...

    # Next step

    <the next step the agent will take>

Every heading in the file is an H1. Never write a `##` heading. A heading that would have been `##`, including one inside `# Response`, is `#`.

Include Response, Adjustment, and Commands only when that section has content. Omit the heading when it would be empty. Adjustment states what this step changed relative to the original plan. Add further `#` sections when the reply has distinct topics those three do not cover. As many `#` sections as the reply needs. Each extra title is 5–10 words. Include `# Next step` only when the agent was explicitly asked to follow a plan, such as a file written by handoff-mode. Omit it otherwise. When present, it is the last heading, and its body is the next step the agent will take.

The summary heading starts the file (no blank line before it). Blank line after every heading. Blank line before every heading after the summary.

Commands: tests, lints, typechecks, builds — not discovery, edits, or git. Write this response’s commands and every such command from earlier turns, oldest first. Read earlier `# Commands` fences in `$DIR` so commands from previous files are included. Prefix `cd <dir> &&` if not from the init cwd.

Skip the file for toggle/cap acks and trivial one-liners ("Yes", "Done", tool-only). Anything substantive still writes a file.
