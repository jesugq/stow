---
name: pathway-mode
description: Toggle with `/pathway-mode`. While on, every substantive reply is written to the next `NN-<slug>.md` under `$DIR`, with one standalone `.mmd` per diagram beside it as `NN-MM-<description>.mmd`; chat only names the folder and the new files. No in-chat graphs or mermaid source.
disable-model-invocation: true
---

# Pathway mode

`$DIR = ~/.cursor/dynamic-mode/<local YYYY-MM-DD of the conversation’s first message>-<$CURSOR_CONVERSATION_ID>` (no spaces; refuse if the id is unset). If a directory under `~/.cursor/dynamic-mode` already ends in `-$CURSOR_CONVERSATION_ID`, that is `$DIR`; if several, use the earliest date. A later calendar day does not create a second folder. Outline, takeoff, pathway, and handoff share this folder and the `NN-*.md` sequence.

On iff zero-byte `$DIR/PATHWAY` exists. `OUTLINE`, `TAKEOFF`, and `HANDOFF` are the other modes. No sentinel means off — a folder or leftover markdown alone is off. The four sentinels are mutually exclusive. `/pathway-mode` toggles this mode (ignore extra words). `/outline-mode`, `/takeoff-mode`, and `/handoff-mode`: do not write a file and do not print a pathway-mode comment.

Off → on: mkdir `$DIR` if needed, delete any other sentinel, create `PATHWAY`, keep existing `NN-*.md`, and continue that index. The next substantive reply uses this shape.
On → off: delete `PATHWAY` only.

Chat is only these sections. A blank line separates each section. A section that prints several lines, such as one `.mmd` path per diagram, puts each line directly under the last.

    [pathway-mode] <enabled|disabled|created a file|limit reached>

    <absolute $DIR>

    [<absolute new markdown file, write turns only>]

    [<absolute new .mmd path, one per line, write turns only>]

    [usage-utc-date] <UTC time the prompt was sent>

The last section is the UTC time Cursor records for this model call on the usage dashboard: the prompt-send time, not the response time. Format `[usage-utc-date] Oct 13, 06:47 PM`: abbreviated English month, day with no leading zero, comma, zero-padded 12-hour clock, `AM` or `PM`. No year and no timezone label.

While `PATHWAY` exists, each substantive query writes exactly one new `$DIR/<NN>-<slug>.md` and, for each diagram, one `$DIR/<NN>-<MM>-<description>.mmd` in that same directory — not in `$DIR/pathway` or any other subdirectory. Never edit an existing file, including ones the other modes wrote. `NN` = count of `[0-9][0-9]-*.md` directly in `$DIR` + 1, two digits. `.mmd` files do not count. The markdown slug is kebab-case from the H1. `MM` is that diagram’s order among diagram sections, two digits from `01`. `<description>` is kebab-case from that diagram’s heading. At 100: write nothing, comment `limit reached`, tell the user to start a new conversation.

    # <5-10 word summary of what happened to the data>

    ## <5-10 word diagram title of what happened to the data>

    <what happened to the data>

    [<NN>-<MM>-<description>.mmd](<NN>-<MM>-<description>.mmd)

    ## <5-10 word title of what happened to the data>

    <full section body>

    ## ...

The H1 starts the file (no blank line before it). Blank line after every heading, including `#`. Blank line before every `##`. Never write a `Response` heading. Each diagram is one `##`: a 5–10 word title, a short summary that orients the user and does not retell the steps, then one relative `.mmd` link. The steps live on the diagram. One such heading per diagram, in the order the graphs appear. When part of the reply is not covered by a graph, add an outline-style `##` (5–10 word title and a full section body, no `.mmd`), as many as the reply needs.

Wording restriction, on the H1, every `##` title, the diagram summary, every other section body, both slugs, link text, and comment labels: say only what happened to the data. Leave out where the data went. Name no component, method, variable, or other item in memory that can be called. A component name of any type is forbidden in the markdown — a class, module, service, file, package, screen, or any other named part of the program. Write link text and comment labels for those nodes; do not copy them from the markdown. Do not break or shorten a comment. Link text is three or four words, written `idA-- words ---idB` (`set to zero`, `cleared of entries`, `narrowed to matches`). When that wording cannot be said accurately on a link, choose another link. Do not reorder the nodes to make the wording fit. A comment link is dotted and has no text, written `idA-.-idB`.

## Nodes

A diagram shows the flow of data. Choose the sources from the user's prompt, and include every source that prompt makes relevant. A data source is a variable, an environment variable, a data structure, a file, or another source. One diagram holds at most eight data sources. When more sources are relevant, create a separate diagram for the rest. Split each branch into its own diagram. A branch is a separate path the data can take, and each branch gets its own `##` and its own `.mmd`.

One start node and one end node. A start may arrive from another diagram, and an end may leave for another diagram. The start node links to the title node. Each data node has a comment node. Only node syntax: `id@{ shape: <name>, label: "<text>" }`.

| Kind | Shape | Label |
| --- | --- | --- |
| start | `hex` | `start`, or the `##` title of the diagram this branch arrives from |
| title | `notch-pent` | the diagram's `##` title |
| end | `hex` | `end`, or the `##` title of the diagram this branch leaves for |
| data | `datastore` | `{{data_source}}<br>{{data_type}}<br><br>{{relevant_values}}` |
| comment | `comment` | `{{description}}` |
| path | `rounded` | `{{method}}` |

The type is `Boolean`, `Integer`, `Class`, `JSON`, or another type. The relevant values can be many, each on its own line. A Boolean prints `true` or `false`. An Integer prints the number. A complex type, such as a Class, an Object, or JSON, prints each relevant part with its name and value, as in `id: 1<br>name: Cursor`. The original source is not printed. Each data source has one border color, and every data node of that source uses it. Assign the colors in this order, and do not reuse a color in the same diagram: `#FFADAD`, `#FFD6A5`, `#FDFFB6`, `#CAFFBF`, `#9BF6FF`, `#A0C4FF`, `#BDB2FF`, `#FFC6FF`. Color a data node with `style <id> stroke:<color>,stroke-width:4px`. Only data nodes are colored.

A path node names only the method, or another representation of the part of the component that was called. It does not name the component. Every path node sits in a subgraph named after the component it is inside: `subgraph id [Component]`. Path nodes of the same component share that subgraph. The subgraph title is the component's own name, never a relative or absolute path. A path node has no data source lines and no description. Do not color a subgraph.

    startNode@{ shape: hex, label: "start" }
    title@{ shape: notch-pent, label: "stored count becomes zero" }
    src@{ shape: datastore, label: "counter<br>Integer<br><br>0" }
    note@{ shape: comment, label: "nothing remains of the previous count" }
    subgraph parser [Parser]
        edge@{ shape: rounded, label: "parse" }
    end
    finish@{ shape: hex, label: "matching entries remain" }
    startNode --> title
    src-- set to zero ---edge
    src-.-note
    style src stroke:#FFADAD,stroke-width:4px

The `.mmd` file is mermaid source alone: no markdown fence, no heading, no SVG, PNG, HTML, font data, or license. Do not render, install packages or browsers, or run `mmdc`, `scripts/print-graph`, or `command -v mmdc`. Do not write a temp file, an `.svg`, or any other file.

Skip the file for toggle/cap acks and trivial one-liners ("Yes", "Done", tool-only). Anything substantive still writes a file.
