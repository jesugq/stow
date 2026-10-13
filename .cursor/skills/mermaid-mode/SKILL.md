---
name: mermaid-mode
description: Toggle with `/mermaid-mode`. While on, every substantive reply is written to the next `NN-<slug>.md` under `$DIR`, with one standalone `.mmd` per diagram beside it as `NN-MM-<description>.mmd`; chat only names the folder and the new files. No in-chat graphs or mermaid source.
disable-model-invocation: true
---

# Mermaid mode

Shared with outline-mode, takeoff-mode, and handoff-mode. `$NAME` is `<local YYYY-MM-DD>-<$CURSOR_CONVERSATION_ID>`: the date, one hyphen, then the conversation id, with no spaces. `$DIR = ~/.cursor/dynamic-mode/$NAME` (refuse if the conversation id is unset). Example: `~/.cursor/dynamic-mode/2026-09-24-<id>`. All four modes use this one folder and the same `NN-*.md` sequence. The date is the local calendar date at the start of the turn; the same day and conversation always resolve to the same `$DIR`.

On iff `$DIR/MERMAID` exists (zero-byte sentinel). `$DIR/OUTLINE` means outline-mode is on instead. `$DIR/TAKEOFF` means takeoff-mode is on instead. `$DIR/HANDOFF` means handoff-mode is on instead. Neither sentinel means off — a folder or leftover markdown alone is off. The four sentinels are mutually exclusive. `/mermaid-mode` toggles this mode (ignore extra words). `/outline-mode`, `/takeoff-mode`, and `/handoff-mode` belong to the other skills: do not write a file and do not print a mermaid-mode comment for them.

Enabling while `OUTLINE`, `TAKEOFF`, or `HANDOFF` exists swaps. Delete those sentinels, create `MERMAID`, keep every `NN-*.md`, and continue that index. The next substantive reply uses mermaid-mode’s shape.

Chat is only these sections. A blank line separates each section. A section that prints several lines, such as one `.mmd` path per diagram, puts each line directly under the last.

    [mermaid-mode] <enabled|disabled|created a file|limit reached>

    <absolute $DIR>

    [<absolute new markdown file, write turns only>]

    [<absolute new .mmd path, one per line, write turns only>]

    [usage-utc-date] <UTC time the prompt was sent>

The last section is the UTC time Cursor records for this model call on the usage dashboard: the time the user sent the prompt, not the time the response finishes. Take that prompt timestamp and convert it to UTC. Format it `[usage-utc-date] Oct 13, 06:47 PM`: the tag, then an abbreviated English month, day with no leading zero, a comma, then a zero-padded 12-hour clock and `AM` or `PM`. No year and no timezone label.

Off → on: mkdir `$DIR` if needed, create `MERMAID`, keep existing `NN-*.md`. If `OUTLINE`, `TAKEOFF`, or `HANDOFF` is present, delete it first (swap).
On → off: delete `MERMAID` only.

While `MERMAID` exists, each substantive query writes exactly one new `$DIR/<NN>-<slug>.md` and, for each diagram, one `$DIR/<NN>-<MM>-<description>.mmd` in that same directory (never edit prior files, including ones outline-mode, takeoff-mode, or handoff-mode wrote, and never edit an existing `.mmd`). Do not create `$DIR/mermaid` and do not put diagrams in a subdirectory. `NN` = count of `[0-9][0-9]-*.md` directly in `$DIR` + 1, two digits. `.mmd` files do not count. The markdown slug is kebab-case from the H1. `MM` is that diagram’s order among diagram sections in the markdown, two digits starting at `01`. `<description>` is kebab-case from that diagram’s heading. At 100: write nothing, comment `limit reached`, tell the user to start a new conversation.

    # <5-10 word summary>

    ## <5-10 word diagram title>

    <what this diagram represents, and what the user will be looking at when they open it>

    [<NN>-<MM>-<description>.mmd](<NN>-<MM>-<description>.mmd)

    ## <5-10 word title>

    <full section body>

    ## ...

Never write a `Response` heading. Each diagram gets exactly one `##`: a 5–10 word title, then a short summary of what that diagram represents and which data, components, and methods the user will be looking at when they open it, then one relative link to its `.mmd`, and nothing else. That summary orients the user. It does not retell the numbered steps. One such heading per diagram, in the order the graphs appear. When part of the reply is not covered by a graph, add an outline-style `##` for it: a 5–10 word title and a full section body, with no `.mmd`. As many of those as the reply needs.

The H1 starts the file (no blank line before it). Blank line after every heading, including `#`. Blank line before every `##`.

## Node shapes

A diagram shows the flow of data. Choose the sources from the user's prompt, and include every source that prompt makes relevant. Every node is one of three kinds: a path taken, a data source, or a transformation. The graph opens on one or more data sources and closes on one or more data sources: the data that enters, and the data that leaves. A data source may also sit between those ends when the flow names it again.

Number every node in that diagram `01`, `02`, `03`, and so on, in the order the graph reads them. Two digits. Each diagram starts again at `01`.

The diagram carries every step. Write each description for the node itself; do not copy it from the markdown, and do not copy the markdown summary onto the node.

Write every node as `id@{ shape: <name>, label: "01<br>line two<br>line three<br><br>description" }`. The number is its own line, followed by `<br>`. After the name and the type or method, write `<br><br>`, then what that step does as one string. Do not break or shorten the description.

    step@{ shape: stadium, label: "01<br>name<br>type<br><br>what this step does" }

| Name | Kind | Use when the block is |
| --- | --- | --- |
| `fr-rect` | path taken | the subroutine shape. A component method the data passes through. Second line is the component's own name, never a relative or absolute path. Third line is the method. |
| `stadium` | data source | the stadium shape. Data entering, named again inside the flow, or leaving: a variable, an environment variable, a data structure, a file, or another source. Second line is the source name. Third line is the type it has at this point. Every diagram starts on one or more of these and ends on one or more of these. |
| `diam` | transformation | the rhombus. The data changes from one type to another, usually immediately after a path-taken node. Second line is the type it had. Third line is the type it becomes. |

These three shapes are the only ones. Add a `diam` only when the type changes.

## Diagram files

Each diagram `##` summarizes what that graph represents and links one standalone `.mmd`. The steps live on the diagram. The link target is `<NN>-<MM>-<description>.mmd` beside the markdown. `<NN>` is the accompanying markdown file’s `NN`. `<MM>` counts diagram sections only, in the order those sections appear.

Write the diagram source to `$DIR/<NN>-<MM>-<description>.mmd`. The `.mmd` file is mermaid source alone: no markdown fence, no heading, no SVG, PNG, HTML, font data, or license. Do not render. Do not call `mmdc` or `scripts/print-graph`. Do not install packages or browsers. Do not run `command -v mmdc`.

`$DIR` gains the new `NN-*.md` and those `.mmd` files. Do not write a temp file, an `.svg`, or any other file.

Skip the file for toggle/cap acks and trivial one-liners ("Yes", "Done", tool-only). Anything substantive still writes a file.
