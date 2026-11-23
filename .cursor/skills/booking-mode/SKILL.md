---
name: booking-mode
description: /booking-mode new, load, next, or join. One conversation file.
disable-model-invocation: true
---

# Booking mode

Call the Skill tool with `markdown-mode` for the folder, the ack, and the markdown file.

```
verb: new | load | next | join
root: ~/.cursor/booking-mode
sentinel: BOOKING
drop: -
load: 00-BOOKING.md
need: -
mark: BOOKING
step:
sect: heading
```

`new`, `load`, `next`, and `join` are accepted. This mode's file is `$DIR/00-BOOKING.md`. `00` is the file number because no later mode follows this one. The `step` line stays empty.

While `BOOKING` exists, create that file on the first substantive query and edit it after that. Read `$DIR/00-BOOKING.md` once when it exists. That file is the conversation. A later `load` continues from it.

One topic per heading. The heading is `# NN <5-10 word title>`. Number headings from `01` in file order. A message that continues a topic updates that heading. A new topic appends the next number. Do not rewrite an unchanged heading. Do not write a second file.

The body is the topic as it stands. Include what was asked, what was decided, and what stays open. Those three are the context a later `load` needs. The writing style comes from `markdown-mode`. This skill does not restate it.

`load` requires `00-BOOKING.md` in the absolute folder. A folder that has only `NN.md` does not match. The verb `join` requires a zero-byte `BOOKING` in the absolute folder. "Yes", "Done", and tool-only turns that are not this mode: no ack and no file.
