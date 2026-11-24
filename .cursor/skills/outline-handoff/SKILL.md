---
name: outline-handoff
description: /outline-handoff load, next, or join. Next: /outline-prepare next.
disable-model-invocation: true
---

# Outline handoff mode

Call the Skill tool with `markdown-mode` for the folder, the ack, and the markdown file.
    10|
```
verb: load | next | join
root: ~/.cursor/outline-mode
sentinel: OUTLINE_HANDOFF
drop: OUTLINE_ANALYZE,OUTLINE_CLARIFY,OUTLINE_PREPARE,OUTLINE_EXECUTE
load: 03-HANDOFF.md
need: 02-CLARIFY.md
mark: OUTLINE_CLARIFY
step: /outline-prepare next
    20|sect: heading
```

`load`, `next`, and `join` are accepted. This mode's file is `$DIR/03-HANDOFF.md`.

Do not write final document prose. While `OUTLINE_HANDOFF` exists, create that file when it is absent, including the toggle turn. A later agree or revise edits it. Read `$DIR/02-CLARIFY.md` and write each pin whose first line is `Resolved` into the intention it belongs to. Do not reopen it or list rejected options.

Each heading is one intention prepare or execute would miss without. The heading is `# NN <5-10 word intention>`. The body is prose: what must become true, and why. Do not say how to draft or structure the final document in this mode.

Include these boundaries in the set of handoff headings:
- Audience
- Objective
- Scope boundary
- Success definition

If one of those four is still unresolved, keep it as an explicit unresolved constraint in the heading body. Resolved clarify decisions override conflicting handoff statements.
