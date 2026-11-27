---
name: plan-refine
description: "/plan-refine load <folder> or next <prompt>. Next: /plan-execute next <prompt>."
disable-model-invocation: true
---

# Plan refine mode

Call the Skill tool with `markdown-mode` for the folder, the ack, and the markdown file.
Hard rule: Before any response in this mode, run the `markdown-mode` workflow. Then output only the ack or `refused`.
```
verb: load | next
root: /Users/jesus.gonzalez/Development/areas/plans
sentinel: PLAN_REFINE
drop: PLAN_DISCOVER,PLAN_PRIORITIZE,PLAN_EXECUTE
load: -
need: 03-DEFINE.md
prev: plan-define
curr: Plan refine
next: plan-execute
sect: heading
```

`load` and `next` are accepted. `load` accepts the folder with any sentinel. This mode's file is `$DIR/04-REFINE.md`.

Do not write the final document in this mode. A turn that opens, updates, or resolves a writing choice edits that file. Create it only when it is absent. One choice per heading. The heading is `# NN <5-10 word choice>`. Change only the pins this turn opens, updates, or resolves.

Read `$DIR/03-DEFINE.md`, `$DIR/02-PRIORITIZE.md`, and `$DIR/04-REFINE.md`. The define is what must become true and why. The refine file is the writing plan board.

The first line of every body is the status alone: `Blocking`, `Deferrable`, or `Resolved`. Always write it. Open means that line is `Blocking` or `Deferrable`. Closing sets that line to `Resolved` and writes the accepted structure or content choice.

Resolve a section plan for the selected `doc_type` before execute. If `doc_type` is not resolved yet, open a `Blocking` pin for it. The plan must include:
- Required sections for this document
- Evidence plan (links, metrics, references, examples)
- Explicit omissions for non-applicable sections

Per-type minimum section map:
- `prd`: problem, demand/source, desired outcome, success criteria, scope, constraints, risks/caveats
- `tdd`: objective, background, goals/non-goals, overview/design, alternatives, caveats, testing/rollout
- `issue`: kind (`Bug` or `Work`), context/problem, scope, acceptance criteria, verification, references
