---
name: plan-prepare
description: "/plan-prepare load, next, or join. Next: /plan-execute next."
disable-model-invocation: true
---

# Plan prepare mode

Call the Skill tool with `markdown-mode` for the folder, the ack, and the markdown file.
Hard rule: Before any response in this mode, run the `markdown-mode` workflow. Then output only the ack block or `refused`.
    10|
```
verb: load | next | join
root: ~/.cursor/plan-mode
sentinel: PLAN_PREPARE
drop: PLAN_ANALYZE,PLAN_CLARIFY,PLAN_EXECUTE
load: 04-PREPARE.md
need: 03-HANDOFF.md
mark: PLAN_HANDOFF
next: /plan-execute next
sect: heading
```

`load`, `next`, and `join` are accepted. This mode's file is `$DIR/04-PREPARE.md`.

Do not write the final document in this mode. While `PLAN_PREPARE` exists, a turn that opens, updates, or resolves a writing choice edits that file. Create it only when it is absent. One choice per heading. The heading is `# NN <5-10 word choice>`. Change only the pins this turn opens, updates, or resolves.

Read `$DIR/03-HANDOFF.md`, `$DIR/02-CLARIFY.md`, and `$DIR/04-PREPARE.md`. The handoff is what must become true and why. The prepare file is the writing plan board.

The first line of every body is the status alone: `Blocking`, `Deferrable`, or `Resolved`. Always write it. Open means that line is `Blocking` or `Deferrable`. Closing sets that line to `Resolved` and writes the accepted structure or content choice.

Resolve a section plan for the selected `doc_type` before execute. If `doc_type` is not resolved yet, open a `Blocking` pin for it. The plan must include:
- Required sections for this document
- Evidence plan (links, metrics, references, examples)
- Explicit omissions for non-applicable sections

Per-type minimum section map:
- `prd`: problem, demand/source, desired outcome, success criteria, scope, constraints, risks/caveats
- `tdd`: objective, background, goals/non-goals, overview/design, alternatives, caveats, testing/rollout
- `issue`: kind (`Bug` or `Work`), context/problem, scope, acceptance criteria, verification, references
