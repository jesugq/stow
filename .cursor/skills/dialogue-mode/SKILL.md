---
name: dialogue-mode
description: "/dialogue-mode new <name>, load <folder>, or next <prompt>. One conversation file."
disable-model-invocation: true
---

# Dialogue mode

Call the Skill tool with `markdown-mode` for the folder, the ack, and the markdown file.
Hard rule: Before any response in this mode, run the `markdown-mode` workflow. Then output only the ack or `refused`.
```
verb: new | load | next
root: ~/.cursor/dialogue-mode
sentinel: DIALOGUE
drop: -
load: 00-DIALOGUE.md
need: -
next:
sect: heading
```

`new`, `load`, and `next` are accepted. This mode's file is `$DIR/00-DIALOGUE.md`. `00` is the file number because no later mode follows this one. The `next` line stays empty.

Create that file on the first substantive query and edit it after that. Read `$DIR/00-DIALOGUE.md` once when it exists. That file is the conversation. A later `load` continues from it.

One topic per heading. The heading is `# NN <5-10 word title>`. Number headings from `01` in file order. A message that continues a topic updates that heading. A new topic appends the next number. Do not rewrite an unchanged heading. Do not write a second file.

The body is the topic as it stands. Include what was asked, what was decided, and what stays open. Those three are the context a later `load` needs. The writing style comes from `markdown-mode`. This skill does not restate it.

`load` requires `00-DIALOGUE.md` in the named folder. A folder that has only `NN.md` does not match. "Yes", "Done", and tool-only turns that are not this mode: no ack and no file.
