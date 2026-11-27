---
name: code-define
description: "/code-define load <folder> or next <prompt>. Next: /code-refine next <prompt>."
disable-model-invocation: true
---

# Define mode

Call the Skill tool with `markdown-mode` for the folder, the ack, and the markdown file.
Hard rule: Before any response in this mode, run the `markdown-mode` workflow. Then output only the ack or `refused`.
```
verb: load | next
root: /Users/jesus.gonzalez/Development/areas/codes
sentinel: DEFINE
drop: DISCOVER,PRIORITIZE,REFINE,EXECUTE
load: -
need: 02-PRIORITIZE.md
prev: Prioritize
curr: Define
next: Refine
sect: heading
```

`load` and `next` are accepted. `load` accepts the folder with any sentinel. This mode's file is `$DIR/03-DEFINE.md`. `DEFINE` also means the implementation is incomplete and not started. Refine and execute keep that sentinel.

Do not implement. Do not re-investigate the codebase. Create that file when it is absent, including the toggle turn. A later agree or revise edits it. Read `$DIR/02-PRIORITIZE.md` and write each pin whose first line is `Resolved` into the intention it belongs to. Do not reopen it or list rejected options. "Yes", "OK", "Looks good", and "Do it" accept the discussed intentions and are writes. A revision changes only the intentions the user changed. Tool-only turns write nothing.

Each heading is one intention refine or execute would miss without. The heading is `# NN <5-10 word intention>`. The body is prose: what must become true, and why. Do not say how. Do not name components, edit order, calls, or a procedure. Do not say how to read the file. A later heading may depend on an earlier intention being true, not on an earlier edit.
