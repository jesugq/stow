---
name: plan-define
description: "/plan-define load <folder> or next <prompt>. Next: /plan-refine next <prompt>."
disable-model-invocation: true
---

# Plan define mode

Call the Skill tool with `markdown-mode` for the folder, the ack, and the markdown file.
Hard rule: Before any response in this mode, run the `markdown-mode` workflow. Then output only the ack or `refused`.
```
verb: load | next
root: /Users/jesus.gonzalez/Development/areas/plans
sentinel: PLAN_DEFINE
drop: PLAN_DISCOVER,PLAN_PRIORITIZE,PLAN_REFINE,PLAN_EXECUTE
load: -
need: 02-PRIORITIZE.md
next: /plan-refine next
sect: heading
```

`load` and `next` are accepted. `load` accepts the folder with any sentinel. This mode's file is `$DIR/03-DEFINE.md`.

Do not write final document prose. Create that file when it is absent, including the toggle turn. A later agree or revise edits it. Read `$DIR/02-PRIORITIZE.md` and write each pin whose first line is `Resolved` into the intention it belongs to. Do not reopen it or list rejected options.

Each heading is one intention refine or execute would miss without. The heading is `# NN <5-10 word intention>`. The body is prose: what must become true, and why. Do not say how to draft or structure the final document in this mode.

Include these boundaries in the set of define headings:
- Audience
- Objective
- Scope boundary
- Success definition

If one of those four is still unresolved, keep it as an explicit unresolved constraint in the heading body. Resolved prioritize decisions override conflicting define statements.
