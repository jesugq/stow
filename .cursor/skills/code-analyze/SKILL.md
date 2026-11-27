---
name: code-analyze
description: "/code-analyze new <name> or load <folder>. Next: /code-clarify next <prompt>."
disable-model-invocation: true
---

# Analyze mode

Call the Skill tool with `markdown-mode` for the folder, the ack, and the markdown file.
Hard rule: Before any response in this mode, run the `markdown-mode` workflow. Then output only the ack or `refused`.
    10|
```
verb: new | load
root: /Users/jesus.gonzalez/Development/areas/codes
sentinel: ANALYZE
drop: CLARIFY,HANDOFF,PREPARE,EXECUTE
load: -
need: -
next: /code-clarify next
sect: heading
```

`new` and `load` are accepted. `load` accepts the folder with any sentinel. This mode's file is `$DIR/01-ANALYZE.md`.

Create that file on the first substantive query and edit it after that. Each heading is one finding clarify would decide differently without. The heading is `# NN <5-10 word title>`. Add or replace only that heading. Do not rewrite an unchanged heading, and do not write the rest of the investigation. "Yes", "Done", and tool-only turns that are not this mode: no ack and no file.
