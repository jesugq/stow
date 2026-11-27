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
load: -
need: 03-DEFINE.md
prev: plan-define
curr: Plan refine
next: plan-execute
sect: heading
```

`load` and `next` are accepted. `load` accepts the folder name. A work message with no verb uses `count`. This mode's file is `$DIR/04-REFINE.md`.

Do not write the final document in this mode. A turn that opens, updates, or resolves a writing choice edits that file. Create it only when it is absent. One choice per heading. The heading is `# NN <5-10 word choice>`. Change only the pins this turn opens, updates, or resolves. No board change: no ack and no file. A short ack that settles a pin is an edit.

Read `$DIR/03-DEFINE.md`, `$DIR/02-PRIORITIZE.md`, and `$DIR/04-REFINE.md`. The define is what must become true and why. A prioritize pin whose first line is `Resolved` is closed. Do not reopen it. The refine file is the writing plan board. Absent means no pins. A new pin is a writing choice the define leaves open that would change the final document. Do not pin an intention, or a choice the define or a closed prioritize decision already settles. No define file means no new pins.

The heading text after the number is the tab. Reuse it exactly. Match the user's message to pin bodies, not heading text or answer order. One message that would settle two headings is one pin. The first line of every body is the status alone: `Blocking`, `Deferrable`, or `Resolved`. Always write it. Open means that line is `Blocking` or `Deferrable`. Closing sets that line to `Resolved` and writes the accepted structure or content choice, including an accepted recommendation, and leaves the heading in the file. Do not write `Resolved` while a choice is open. Settled means the user chose, accepted the recommendation, or the selected `doc_type` has only one structure that satisfies the define.

Resolve a section plan for the selected `doc_type` before execute. If `doc_type` is not resolved yet, open a `Blocking` pin for it. The plan must include:
- Required sections for this document
- Evidence plan (links, metrics, references, examples)
- Explicit omissions for non-applicable sections

Per-type minimum section map:
- `prd`: problem, demand/source, desired outcome, success criteria, scope, constraints, risks/caveats
- `tdd`: objective, background, goals/non-goals, overview/design, alternatives, caveats, testing/rollout
- `issue`: kind (`Bug` or `Work`), context/problem, scope, acceptance criteria, verification, references
