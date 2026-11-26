---
name: code-prepare
description: "/code-prepare load <folder>, next <prompt>, or join <folder>. Next: /code-execute next <prompt>."
disable-model-invocation: true
---

# Prepare mode

Call the Skill tool with `markdown-mode` for the folder, the ack, and the markdown file.
Hard rule: Before any response in this mode, run the `markdown-mode` workflow. Then output only the ack block or `refused`.
    10|
```
verb: load | next | join
root: ~/.cursor/dynamic-mode
sentinel: PREPARE
drop: ANALYZE,CLARIFY,EXECUTE
load: 04-PREPARE.md
need: 03-HANDOFF.md
mark: HANDOFF
next: /code-execute next
sect: heading
```

`load`, `next`, and `join` are accepted. This mode's file is `$DIR/04-PREPARE.md`. Keep `HANDOFF`.

Do not implement. While `PREPARE` exists, a turn that opens, updates, or resolves a way to build edits that file. Create it only when it is absent. One choice per heading. The heading is `# NN <5-10 word choice>`. Change only the pins this turn opens, updates, or resolves. No board change: no ack and no file. A short ack that settles a pin is an edit.

Read `$DIR/03-HANDOFF.md`, `$DIR/02-CLARIFY.md`, and `$DIR/04-PREPARE.md`. The handoff is what must become true and why. A clarify pin whose first line is `Resolved` is closed. Do not reopen it. The prepare file is the board. Absent means no pins. Look at the codebase only to see which existing way would satisfy the handoff.

A new pin is a way of building the handoff leaves open that would change what execute edits. Do not pin a product intention, or a choice the handoff or a closed clarify decision already settles. No handoff file means no new pins.
    30|
The heading text after the number is the tab. Reuse it exactly. Match the user's message to pin bodies, not heading text or answer order. One message that would settle two headings is one pin. The first line of every body is the status alone: `Blocking`, `Deferrable`, or `Resolved`. Always write it. Open means that line is `Blocking` or `Deferrable`. Closing sets that line to `Resolved` and writes the way execute will build in the lines after, including an accepted recommendation, and leaves the heading in the file.

An open body after the status line says what is undecided about how to build, what would settle it, and the way execute should build if accepted. Prefer a way the codebase already uses when it satisfies the handoff. `Blocking` must close before execute. `Deferrable` may stay open through execute. Do not write `Resolved` while a choice is open. Settled means the user chose, accepted the recommendation, or the codebase has only one way that satisfies the handoff.
