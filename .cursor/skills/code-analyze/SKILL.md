---
name: code-analyze
description: "/code-analyze new <name> or load <folder>. Next: /code-clarify next <prompt>."
disable-model-invocation: true
---

# Analyze mode

Call the Skill tool with `markdown-mode` for the folder, the ack, and the markdown file.
Hard rule: Before any response in this mode, run the `markdown-mode` workflow. Then output only the ack block or `refused`.
    10|
```
verb: new | load
root: ~/.cursor/dynamic-mode
sentinel: ANALYZE
drop: CLARIFY,HANDOFF,PREPARE,EXECUTE
load: 01-ANALYZE.md
need: -
mark: -
next: /code-clarify next
sect: heading
```

`new` and `load` are accepted. This mode's file is `$DIR/01-ANALYZE.md`.

While `ANALYZE` exists, create that file on the first substantive query and edit it after that. Each heading is one finding clarify would decide differently without. The heading is `# NN <5-10 word title>`. Add or replace only that heading. Do not rewrite an unchanged heading, and do not write the rest of the investigation. "Yes", "Done", and tool-only turns that are not this mode: no ack and no file.
