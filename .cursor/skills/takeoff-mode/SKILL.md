---
name: takeoff-mode
description: /takeoff-mode. Next: no follow up mode.
disable-model-invocation: true
---

# Takeoff mode

`$DIR = ~/.cursor/dynamic-mode/<first-message local YYYY-MM-DD>-<$CURSOR_CONVERSATION_ID>` (no spaces; refuse if the id is unset). Reuse a folder ending in that id; if several, use the earliest date. Do not open a second folder on a later day. Order: analyze → clarify → handoff → prepare → takeoff. This mode's only file is `$DIR/TAKEOFF.md`. The others are `$DIR/ANALYZE.md`, `$DIR/CLARIFY.md`, `$DIR/HANDOFF.md`, `$DIR/PREPARE.md`.
On iff `$DIR/TAKEOFF` exists (zero-byte). Other sentinels: `ANALYZE`, `CLARIFY`, `HANDOFF`, `PREPARE`. Mutually exclusive; none means off. `/takeoff-mode` toggles; extra words are ignored. `/analyze-mode`, `/clarify-mode`, `/handoff-mode`, and `/prepare-mode` are not this mode: do not write a file and do not print `[takeoff-mode]`. Swap deletes the other sentinel and creates `TAKEOFF`. Off deletes only `TAKEOFF`. The markdown stays.

H1 only. No frontmatter. No JSON. The first heading starts the file. Blank line after every heading and before every later one. Headings are `# 01 <5-10 word title>`, then `02`, `03`, in file order.

Ack only for enable, disable, swap, create, or edit. Otherwise no `[takeoff-mode]` line. Blank line between each line. Comment: `enabled`, `disabled`, `created a file`, or `edited`. A swap on uses `enabled`. Nothing else. On create or edit, the line after `$DIR` is the numbers of headings whose body was written, comma-separated (`01, 02`). Omit that line when no heading changed. A heading that only shifted number is not listed.

    [takeoff-mode] <comment>

    <absolute $DIR>

    01, 02

    no follow up mode

    [usage-utc-date] Oct 13, 06:47 PM

UTC is when the prompt was sent: abbreviated month, day with no leading zero, comma, zero-padded 12-hour clock, AM/PM. No year. No zone.

While `TAKEOFF` exists, create `$DIR/TAKEOFF.md` on the first substantive query and edit it after that. "Yes", "Done", and tool-only turns: no ack and no file. Each product heading is one thing that was done this turn, including the approach used, as fact. No untaken option, open question, or restatement of the handoff. Omit an empty section.

Before changing the product, read `$DIR/HANDOFF.md`, `$DIR/CLARIFY.md`, and `$DIR/PREPARE.md`. The handoff is what must become true and why. A clarify `Resolved,` body wins over a conflicting handoff sentence. No prepare file means do not invent the architecture. A `Resolved,` body in the prepare file is how to build. Follow it. Do not pick another way. If that file still has an open pin marked `Blocking`, do not invent the choice. Record the stop, and do only the work that does not depend on it.

The file shows only this turn's product work, plus the Linear and Bugbot headings once they exist. Replace every product heading with this turn. Leave a Linear or Bugbot heading unchanged unless this turn is about that heading. Fixing a Bugbot finding, or running Bugbot again, may overwrite the Bugbot heading. A Linear authentication check or a Linear requirements pass may overwrite the matching Linear heading. After the edit, number the headings from `01` in file order.

These headings are created the first time the handoff is applied, with product work between the Linear check and the nitpick:

- The Linear check confirms Linear authentication and a Linear URL. In the `linear` MCP namespace, `needsAuth` means not authenticated. Record the URL when one was provided. If Linear is not authenticated or no URL was provided, refuse and stop this file after that heading.
- The Linear nitpick reads that issue and records which of its title, description, and comments the change may have missed.
- The Bugbot heading runs Bugbot. Follow the `review-bugbot` skill: `bugbot` subagent, `description: "Bugbot"`, `subagent_type: "bugbot"`, `run_in_background: false`, `Full Repository Path` set to the absolute git repository, `Diff: branch changes` unless the user asked for uncommitted changes only. Record every finding and how to fix it. Do not apply the fixes in that heading.
