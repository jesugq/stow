---
name: handoff-mode
description: /handoff-mode load, next, or join. Next: /prepare-mode next.
disable-model-invocation: true
---

# Handoff mode

Call the Skill tool with `markdown-mode` for the folder, the ack, and the markdown file.

```
verb: load | next | join
root: ~/.cursor/dynamic-mode
sentinel: HANDOFF
drop: ANALYZE,CLARIFY,PREPARE,TAKEOFF
load: 03-HANDOFF.md
need: 02-CLARIFY.md
mark: CLARIFY
step: /prepare-mode next
sect: heading
```

`load`, `next`, and `join` are accepted. This mode's file is `$DIR/03-HANDOFF.md`. `HANDOFF` also means the implementation is incomplete and not started. Prepare and takeoff keep that sentinel.

Do not implement. Do not re-investigate the codebase. While `HANDOFF` exists, create that file when it is absent, including the toggle turn. A later agree or revise edits it. Read `$DIR/02-CLARIFY.md` and write each pin whose first line is `Resolved` into the intention it belongs to. Do not reopen it or list rejected options. "Yes", "OK", "Looks good", and "Do it" accept the discussed intentions and are writes. A revision changes only the intentions the user changed. Tool-only turns write nothing.

Each heading is one intention prepare or takeoff would miss without. The heading is `# NN <5-10 word intention>`. The body is prose: what must become true, and why. Do not say how. Do not name components, edit order, calls, or a procedure. Do not say how to read the file. A later heading may depend on an earlier intention being true, not on an earlier edit.
