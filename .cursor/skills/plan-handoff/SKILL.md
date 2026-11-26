---
name: plan-handoff
description: "/plan-handoff load <folder>, next <prompt>, or join <folder>. Next: /plan-prepare next <prompt>."
disable-model-invocation: true
---

# Plan handoff mode

Call the Skill tool with `markdown-mode` for the folder, the ack, and the markdown file.
Hard rule: Before any response in this mode, run the `markdown-mode` workflow. Then output only the ack block or `refused`.
    10|
```
verb: load | next | join
root: ~/.cursor/plan-mode
sentinel: PLAN_HANDOFF
drop: PLAN_ANALYZE,PLAN_CLARIFY,PLAN_PREPARE,PLAN_EXECUTE
load: 03-HANDOFF.md
need: 02-CLARIFY.md
mark: PLAN_CLARIFY
next: /plan-prepare next
sect: heading
```

`load`, `next`, and `join` are accepted. This mode's file is `$DIR/03-HANDOFF.md`.

Do not write final document prose. While `PLAN_HANDOFF` exists, create that file when it is absent, including the toggle turn. A later agree or revise edits it. Read `$DIR/02-CLARIFY.md` and write each pin whose first line is `Resolved` into the intention it belongs to. Do not reopen it or list rejected options.

Each heading is one intention prepare or execute would miss without. The heading is `# NN <5-10 word intention>`. The body is prose: what must become true, and why. Do not say how to draft or structure the final document in this mode.

Include these boundaries in the set of handoff headings:
- Audience
- Objective
- Scope boundary
- Success definition

If one of those four is still unresolved, keep it as an explicit unresolved constraint in the heading body. Resolved clarify decisions override conflicting handoff statements.
