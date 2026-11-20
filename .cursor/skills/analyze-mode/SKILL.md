---
name: analyze-mode
description: /analyze-mode new or load. Next: /clarify-mode next.
disable-model-invocation: true
---

# Analyze mode

Call the Skill tool with `markdown-mode` for the folder, the ack, and the markdown file.

```
verb: new | load
root: ~/.cursor/dynamic-mode
sentinel: ANALYZE
drop: CLARIFY,HANDOFF,PREPARE,TAKEOFF
load: 01-ANALYZE.md
need: -
mark: -
then: /clarify-mode next
sect: heading
```

`new` and `load` are accepted. This mode's file is `$DIR/01-ANALYZE.md`.

While `ANALYZE` exists, create that file on the first substantive query and edit it after that. Each heading is one finding clarify would decide differently without. The heading is `# NN <5-10 word title>`. Add or replace only that heading. Do not rewrite an unchanged heading, and do not write the rest of the investigation. "Yes", "Done", and tool-only turns that are not this mode: no ack and no file.
