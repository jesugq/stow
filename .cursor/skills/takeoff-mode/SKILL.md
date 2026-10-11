---
name: takeoff-mode
description: Toggle with `/takeoff-mode`. While on, every substantive reply is written to the next `NN-<slug>.md` under `$DIR`; chat only names the folder and the new file. No in-chat responses.
disable-model-invocation: true
---

# Takeoff mode

Shared with outline-mode, mermaid-mode, and handoff-mode. `$NAME` is `<local YYYY-MM-DD>-<$CURSOR_CONVERSATION_ID>`: the date, one hyphen, then the conversation id, with no spaces. `$DIR = ~/.cursor/dynamic-mode/$NAME` (refuse if the conversation id is unset). Example: `~/.cursor/dynamic-mode/2026-09-24-<id>`. All four modes use this one folder and the same `NN-*.md` sequence. The date is the local calendar date at the start of the turn; the same day and conversation always resolve to the same `$DIR`.

On iff `$DIR/TAKEOFF` exists (zero-byte sentinel). `$DIR/OUTLINE` means outline-mode is on instead. `$DIR/MERMAID` means mermaid-mode is on instead. `$DIR/HANDOFF` means handoff-mode is on instead. Neither sentinel means off — a folder or leftover markdown alone is off. The four sentinels are mutually exclusive. `/takeoff-mode` toggles this mode (ignore extra words). `/outline-mode`, `/mermaid-mode`, and `/handoff-mode` belong to the other skills: do not write a file and do not print a takeoff-mode comment for them.

Enabling while `OUTLINE`, `MERMAID`, or `HANDOFF` exists swaps. Delete those sentinels, create `TAKEOFF`, keep every `NN-*.md`, and continue that index. The next substantive reply uses takeoff-mode’s shape.

Chat is only:

    [takeoff-mode] <enabled|disabled|created a file|limit reached>
    <absolute $DIR>
    [<absolute new file, write turns only>]

Off → on: mkdir `$DIR` if needed, create `TAKEOFF`, keep existing `NN-*.md`. If `OUTLINE`, `MERMAID`, or `HANDOFF` is present, delete it first (swap).
On → off: delete `TAKEOFF` only.

While `TAKEOFF` exists, each substantive query writes exactly one new `$DIR/<NN>-<slug>.md` (never edit prior files, including ones outline-mode, mermaid-mode, or handoff-mode wrote). `NN` = count of `[0-9][0-9]-*.md` + 1, two digits. Slug is kebab-case from the summary H1 (not from `# Next step`). At 100: write nothing, comment `limit reached`, tell the user to start a new conversation.

    # <5-10 word summary>

    ## Response

    <the full chat reply>

    ## Changes

    - <file>
      - <absolute path>
      - <path relative to the repository; omit a leading simplepractice/>
      - <comma-separated post-edit line ranges>

    ## Commands

    ```
    <assertion commands actually run>
    ```

    ## <5-10 word title>

    <full section body>

    ## ...

    # Next step

    <the next step the agent will take>

Include Response, Changes, and Commands only when that section has content. Omit the heading when it would be empty. Add further `##` sections when the reply has distinct topics those three do not cover. As many `##` sections as the reply needs. Each extra title is 5–10 words. Include `# Next step` only when the agent was explicitly asked to follow a plan, such as a file written by handoff-mode. Omit it otherwise. When present, it is the last heading, and its body is the next step the agent will take.

The summary H1 starts the file (no blank line before it). Blank line after every heading, including `#`. Blank line before every `##` and before `# Next step`. Changes: one parent bullet per written/edited/deleted/renamed file this round (not reads). Parent is the filename. Children, in order: absolute path, path relative to the repository (no `simplepractice/` prefix), then comma-separated line ranges (`10-21, 45-48`). New: filename `(new)`, ranges `1-N`. Deleted: filename `(deleted)`, no line child. Rename: `old → new` as the parent, then both paths and the new file’s ranges.

Commands: tests, lints, typechecks, builds — not discovery, edits, or git used only for Changes. Last run only. Prefix `cd <dir> &&` if not from the init cwd.

Skip the file for toggle/cap acks and trivial one-liners ("Yes", "Done", tool-only). Anything substantive still writes a file.
