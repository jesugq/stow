---
name: code-prioritize
description: "/code-prioritize load <folder> or next <prompt>. Next: /code-define next <prompt>."
disable-model-invocation: true
---

# Prioritize mode

Call the Skill tool with `markdown-mode` for the folder, the ack, and the markdown file.
Hard rule: Before any response in this mode, run the `markdown-mode` workflow. Then output only the ack or `refused`.
```
verb: load | next
root: /Users/jesus.gonzalez/Development/areas/codes
sentinel: PRIORITIZE
drop: DISCOVER,DEFINE,REFINE,EXECUTE
load: -
need: 01-DISCOVER.md
next: /code-define next
sect: heading
```

`load` and `next` are accepted. `load` accepts the folder with any sentinel. This mode's file is `$DIR/02-PRIORITIZE.md`.

A turn that opens, updates, or resolves an ambiguity edits that file. Create it only when it is absent. One ambiguity per heading. The heading is `# NN <5-10 word ambiguity>`. Change only the pins this turn opens, updates, or resolves. No board change: no ack and no file. A short ack that settles a pin is an edit.

Read `$DIR/01-DISCOVER.md` and `$DIR/02-PRIORITIZE.md`. The discover file is the investigation. The prioritize file is the board. Absent means no pins. A new pin is a choice the discover file leaves open that would change the define. Do not pin what it already settles. No discover file means no new pins. Leave code structure for refine.

The heading text after the number is the tab. Reuse it exactly. Match the user's message to pin bodies, not heading text or answer order. One message that would settle two headings is one pin. The first line of every body is the status alone: `Blocking`, `Deferrable`, or `Resolved`. Always write it. Open means that line is `Blocking` or `Deferrable`. Closing sets that line to `Resolved` and writes the decision in the lines after, including an accepted recommendation, and leaves the heading in the file.

An open body after the status line says what is undecided in the define intention, what would settle it, and the option the define should use if accepted. `Blocking` must close before define. `Deferrable` may stay open through define. Do not write `Resolved` while a choice is open. Settled means the user chose, accepted the recommendation, or the implementation already decides it.
