---
name: code-define
description: "/code-define load <folder> or next <prompt>. Next: /code-refine next <prompt>."
disable-model-invocation: true
---

# Define mode

Call the Skill tool on the `markdown-mode` skill. That skill sets the folder, the ack, and the markdown file.
Hard rule: Before any response in this mode, run the `markdown-mode` workflow. Then output only the ack or `refused`.
```
verb: load | next
root: areas/codes
load: -
need: 02-PRIORITIZE.md
prev: code-prioritize
curr: Define
next: code-refine
sect: heading
```

`load` and `next` are accepted. `load` accepts the folder name. A work message with no verb uses `count`. This mode's file is `$DIR/03-DEFINE.md`.

Do not implement. Do not re-investigate the codebase. Create that file when it is absent, including the toggle turn. When the user agrees to the intentions, or asks for them to be done, that is a write. Any wording counts. Read `$DIR/02-PRIORITIZE.md` and write each pin whose first line is `Resolved` into the intention it belongs to. Do not reopen it or list rejected options. A revision changes only the intentions the user changed. A turn that only runs commands writes nothing.

Each heading is one intention refine or execute would miss without. The heading is `# NN <5-10 word intention>`. The body is prose: what must become true, and why. Do not say how. Do not name components, edit order, calls, or a procedure. Do not say how to read the file. A later heading may depend on an earlier intention being true, not on an earlier edit.
