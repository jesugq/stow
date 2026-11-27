---
name: plan-discover
description: "/plan-discover new <name> or load <folder>. Next: /plan-prioritize next <prompt>."
disable-model-invocation: true
---

# Plan discover mode

Call the Skill tool with `markdown-mode` for the folder, the ack, and the markdown file.
Hard rule: Before any response in this mode, run the `markdown-mode` workflow. Then output only the ack or `refused`.
```
verb: new | load
root: /Users/jesus.gonzalez/Development/areas/plans
sentinel: PLAN_DISCOVER
drop: PLAN_PRIORITIZE,PLAN_DEFINE,PLAN_REFINE,PLAN_EXECUTE
load: -
need: -
prev: none
curr: Plan discover
next: plan-prioritize
sect: heading
```

`new` and `load` are accepted. `load` accepts the folder with any sentinel. This mode's file is `$DIR/01-DISCOVER.md`.

Create that file on the first substantive query and edit it after that. Each heading is one finding that could change the documentation quality or direction. The heading is `# NN <5-10 word title>`. Add or replace only that heading. Do not rewrite an unchanged heading, and do not write the rest of the investigation.

Do not write solutions, implementation steps, or final document prose in this mode. Write findings, evidence, and unknowns only. For each non-trivial claim, include a source when available. If no source is available, mark it as `Unverified`.

Track unknowns that could affect the final document quality as explicit statements in the finding body. "Yes", "Done", and tool-only turns that are not this mode: no ack and no file.
