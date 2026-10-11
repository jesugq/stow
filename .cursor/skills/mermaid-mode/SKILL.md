---
name: mermaid-mode
description: Toggle with `/mermaid-mode`. While on, every substantive reply is written to the next `NN-<slug>.md` under `$DIR`, with one standalone `.mmd` per diagram beside it as `NN-MM-<description>.mmd`; chat only names the folder and the new files. No in-chat graphs or mermaid source.
disable-model-invocation: true
---

# Mermaid mode

Shared with outline-mode, takeoff-mode, and handoff-mode. `$NAME` is `<local YYYY-MM-DD>-<$CURSOR_CONVERSATION_ID>`: the date, one hyphen, then the conversation id, with no spaces. `$DIR = ~/.cursor/dynamic-mode/$NAME` (refuse if the conversation id is unset). Example: `~/.cursor/dynamic-mode/2026-09-24-<id>`. All four modes use this one folder and the same `NN-*.md` sequence. The date is the local calendar date at the start of the turn; the same day and conversation always resolve to the same `$DIR`.

On iff `$DIR/MERMAID` exists (zero-byte sentinel). `$DIR/OUTLINE` means outline-mode is on instead. `$DIR/TAKEOFF` means takeoff-mode is on instead. `$DIR/HANDOFF` means handoff-mode is on instead. Neither sentinel means off — a folder or leftover markdown alone is off. The four sentinels are mutually exclusive. `/mermaid-mode` toggles this mode (ignore extra words). `/outline-mode`, `/takeoff-mode`, and `/handoff-mode` belong to the other skills: do not write a file and do not print a mermaid-mode comment for them.

Enabling while `OUTLINE`, `TAKEOFF`, or `HANDOFF` exists swaps. Delete those sentinels, create `MERMAID`, keep every `NN-*.md`, and continue that index. The next substantive reply uses mermaid-mode’s shape.

Chat is only:

    [mermaid-mode] <enabled|disabled|created a file|limit reached>
    <absolute $DIR>
    [<absolute new markdown file, write turns only>]
    [<absolute new .mmd path, one per diagram, write turns only>]

Off → on: mkdir `$DIR` if needed, create `MERMAID`, keep existing `NN-*.md`. If `OUTLINE`, `TAKEOFF`, or `HANDOFF` is present, delete it first (swap).
On → off: delete `MERMAID` only.

While `MERMAID` exists, each substantive query writes exactly one new `$DIR/<NN>-<slug>.md` and, for each diagram, one `$DIR/<NN>-<MM>-<description>.mmd` in that same directory (never edit prior files, including ones outline-mode, takeoff-mode, or handoff-mode wrote, and never edit an existing `.mmd`). Do not create `$DIR/mermaid` and do not put diagrams in a subdirectory. `NN` = count of `[0-9][0-9]-*.md` directly in `$DIR` + 1, two digits. `.mmd` files do not count. The markdown slug is kebab-case from the H1. `MM` is that diagram’s order among diagram sections in the markdown, two digits starting at `01`. `<description>` is kebab-case from that diagram’s heading. At 100: write nothing, comment `limit reached`, tell the user to start a new conversation.

    # <5-10 word summary>

    ## <5-10 word diagram title>

    <detailed explanation of this graph>

    [<NN>-<MM>-<description>.mmd](<NN>-<MM>-<description>.mmd)

    ## <5-10 word title>

    <full section body>

    ## ...

Never write a `Response` heading. Each diagram gets exactly one `##`: a 5–10 word title, then a detailed explanation of what the graph shows, then one relative link to its `.mmd`, and nothing else. One such heading per diagram, in the order the graphs appear. When part of the reply is not covered by a graph, add an outline-style `##` for it: a 5–10 word title and a full section body, with no `.mmd`. As many of those as the reply needs.

The H1 starts the file (no blank line before it). Blank line after every heading, including `#`. Blank line before every `##`.

## Node shapes

A diagram explains the flow of data. It does not draw the shape of components. Pick each shape from the block’s role in that flow. A service, database, queue, or box that merely resembles a shape does not get that shape.

Write every node as `id@{ shape: <name>, label: "text" }`. Use that name when the block represents this meaning:

| Name | Use when the block is |
| --- | --- |
| `rect` | a step or action |
| `rounded` | an event |
| `stadium` | a start or an end |
| `circle` | a start point |
| `dbl-circ` | a stop |
| `diam` | a decision |
| `hex` | a preparation or a condition |
| `lean-r` | input or output |
| `lean-l` | input or output in the other direction |
| `cyl` | a database |
| `fr-rect` | a subprocess |
| `doc` | a document |

A step that only moves data stays `rect`, including a step that runs inside a database or another service. Use `cyl`, `doc`, `lean-r`, or `lean-l` when the block itself is the store, the document, or data crossing the boundary.

## Diagram files

Each diagram `##` explains that graph and links one standalone `.mmd`. The link target is `<NN>-<MM>-<description>.mmd` beside the markdown. `<NN>` is the accompanying markdown file’s `NN`. `<MM>` counts diagram sections only, in the order those sections appear.

Write the diagram source to `$DIR/<NN>-<MM>-<description>.mmd`. The `.mmd` file is mermaid source alone: no markdown fence, no heading, no SVG, PNG, HTML, font data, or license. Do not render. Do not call `mmdc` or `scripts/print-graph`. Do not install packages or browsers. Do not run `command -v mmdc`.

`$DIR` gains the new `NN-*.md` and those `.mmd` files. Do not write a temp file, an `.svg`, or any other file.

Skip the file for toggle/cap acks and trivial one-liners ("Yes", "Done", tool-only). Anything substantive still writes a file.
