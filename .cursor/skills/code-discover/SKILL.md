---
name: code-discover
description: "/code-discover new <name> or load <folder>. Next: /code-prioritize next <prompt>."
disable-model-invocation: true
---

# Discover mode

Call the Skill tool with `markdown-mode` for the folder, the ack, and the markdown file.
Hard rule: Before any response in this mode, run the `markdown-mode` workflow. Then output only the ack or `refused`.
```
verb: new | load
root: /Users/jesus.gonzalez/Development/areas/codes
sentinel: DISCOVER
drop: PRIORITIZE,DEFINE,REFINE,EXECUTE
load: -
need: -
prev: None
curr: Discover
next: Prioritize
sect: heading
```

`new` and `load` are accepted. `load` accepts the folder with any sentinel. This mode's file is `$DIR/01-DISCOVER.md`.

Create that file on the first substantive query and edit it after that. Each heading is one finding prioritize would decide differently without. The heading is `# NN <5-10 word title>`. Add or replace only that heading. Do not rewrite an unchanged heading, and do not write the rest of the investigation. "Yes", "Done", and tool-only turns that are not this mode: no ack and no file.
