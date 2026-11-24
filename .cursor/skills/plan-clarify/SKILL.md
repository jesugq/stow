---
name: plan-clarify
description: "/plan-clarify load, next, or join. Next: /plan-handoff next."
disable-model-invocation: true
---

# Plan clarify mode

Call the Skill tool with `markdown-mode` for the folder, the ack, and the markdown file.
Hard rule: Before any response in this mode, run the `markdown-mode` workflow. Then output only the ack block or `refused`.
    10|
```
verb: load | next | join
root: ~/.cursor/plan-mode
sentinel: PLAN_CLARIFY
drop: PLAN_ANALYZE,PLAN_HANDOFF,PLAN_PREPARE,PLAN_EXECUTE
load: 02-CLARIFY.md
need: 01-ANALYZE.md
mark: PLAN_ANALYZE
step: /plan-handoff next
    20|sect: heading
```

`load`, `next`, and `join` are accepted. This mode's file is `$DIR/02-CLARIFY.md`.

While `PLAN_CLARIFY` exists, a turn that opens, updates, or resolves an ambiguity edits that file. Create it only when it is absent. One ambiguity per heading. The heading is `# NN <5-10 word ambiguity>`. Change only the pins this turn opens, updates, or resolves. No board change: no ack and no file. A short ack that settles a pin is an edit.

Read `$DIR/01-ANALYZE.md` and `$DIR/02-CLARIFY.md`. The analyze file is the investigation. The clarify file is the board. Absent means no pins. A new pin is a choice the analyze file leaves open that would change the final document.

The heading text after the number is the tab. Reuse it exactly. Match the user's message to pin bodies, not heading text or answer order. One message that would settle two headings is one pin. The first line of every body is the status alone: `Blocking`, `Deferrable`, or `Resolved`. Always write it. Open means that line is `Blocking` or `Deferrable`. Closing sets that line to `Resolved` and writes the decision in the lines after, including an accepted recommendation, and leaves the heading in the file.

If document type is not already settled, open or resolve a pin for `doc_type` with exactly one of `prd`, `tdd`, or `issue`. `Blocking` pins must close before handoff. `Deferrable` pins may stay open through handoff.
