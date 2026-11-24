---
name: outline-analyze
description: /outline-analyze new or load. Next: /outline-clarify next.
disable-model-invocation: true
---

# Outline analyze mode

Call the Skill tool with `markdown-mode` for the folder, the ack, and the markdown file.
    10|
```
verb: new | load
root: ~/.cursor/outline-mode
sentinel: OUTLINE_ANALYZE
drop: OUTLINE_CLARIFY,OUTLINE_HANDOFF,OUTLINE_PREPARE,OUTLINE_EXECUTE
load: 01-ANALYZE.md
need: -
mark: -
step: /outline-clarify next
    20|sect: heading
```

`new` and `load` are accepted. This mode's file is `$DIR/01-ANALYZE.md`.

While `OUTLINE_ANALYZE` exists, create that file on the first substantive query and edit it after that. Each heading is one finding that could change the documentation quality or direction. The heading is `# NN <5-10 word title>`. Add or replace only that heading. Do not rewrite an unchanged heading, and do not write the rest of the investigation.

Do not write solutions, implementation steps, or final document prose in this mode. Write findings, evidence, and unknowns only. For each non-trivial claim, include a source when available. If no source is available, mark it as `Unverified`.

Track unknowns that could affect the final document quality as explicit statements in the finding body. "Yes", "Done", and tool-only turns that are not this mode: no ack and no file.
