---
name: plan-prioritize
description: "/plan-prioritize load <folder> or next <prompt>. Next: /plan-define next <prompt>."
disable-model-invocation: true
---

# Plan prioritize mode

Call the Skill tool with `markdown-mode` for the folder, the ack, and the markdown file.
Hard rule: Before any response in this mode, run the `markdown-mode` workflow. Then output only the ack or `refused`.
```
verb: load | next
root: /Users/jesus.gonzalez/Development/areas/plans
load: -
need: 01-DISCOVER.md
prev: plan-discover
curr: Plan prioritize
next: plan-define
sect: heading
```

`load` and `next` are accepted. `load` accepts the folder name. A work message with no verb uses `count`. This mode's file is `$DIR/02-PRIORITIZE.md`.

A turn that opens, updates, or resolves an ambiguity edits that file. Create it only when it is absent. One ambiguity per heading. The heading is `# NN <5-10 word ambiguity>`. Change only the pins this turn opens, updates, or resolves. No board change: no ack and no file. A short ack that settles a pin is an edit.

Read `$DIR/01-DISCOVER.md` and `$DIR/02-PRIORITIZE.md`. The discover file is the investigation. The prioritize file is the board. Absent means no pins. A new pin is a choice the discover file leaves open that would change the final document. Do not pin what it already settles. No discover file means no new pins. Leave the section plan for refine.

The heading text after the number is the tab. Reuse it exactly. Match the user's message to pin bodies, not heading text or answer order. One message that would settle two headings is one pin. The first line of every body is the status alone: `Blocking`, `Deferrable`, or `Resolved`. Always write it. Open means that line is `Blocking` or `Deferrable`. Closing sets that line to `Resolved` and writes the decision in the lines after, including an accepted recommendation, and leaves the heading in the file.

If document type is not already settled, open or resolve a pin for `doc_type` with exactly one of `prd`, `tdd`, or `issue`. `Blocking` pins must close before define. `Deferrable` pins may stay open through define.
