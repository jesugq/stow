---
name: takeoff-mode
description: /takeoff-mode. Next: no follow up mode.
disable-model-invocation: true
---

# Takeoff mode

`$DIR = ~/.cursor/dynamic-mode/<first-message local YYYY-MM-DD>-<$CURSOR_CONVERSATION_ID>` (no spaces; refuse if the id is unset). Reuse a folder ending in that id; if several, use the earliest date. Do not open a second folder on a later day. Order: analyze → clarify → handoff → prepare → takeoff. This mode's only file is `$DIR/05-TAKEOFF.md`. The others are `$DIR/01-ANALYZE.md`, `$DIR/02-CLARIFY.md`, `$DIR/03-HANDOFF.md`, `$DIR/04-PREPARE.md`.
On iff `$DIR/TAKEOFF` exists (zero-byte). Other sentinels: `ANALYZE`, `CLARIFY`, `HANDOFF`, `PREPARE`. Mutually exclusive; none means off. `/takeoff-mode` toggles; extra words are ignored. `/analyze-mode`, `/clarify-mode`, `/handoff-mode`, and `/prepare-mode` are not this mode: do not write a file and do not print `[mode]`. Swap deletes the other sentinel and creates `TAKEOFF`. Off deletes only `TAKEOFF`. The markdown stays.

H1 only. No frontmatter. No JSON. The first heading starts the file. Blank line after every heading and before every later one. Headings are `# 01 <5-10 word title>`, then `02`, `03`, in file order. When referring to a file, use one of two: a file in the agent cwd is `lua/libfuns/context.lua:26` (relative, colon, line); a file outside that cwd is its absolute path, colon, line; never `../`. Keep each path in backticks so neovim `` yi` `` selects them. Quote source inline if it is one line, in a fenced block if it is larger; never as bare lines.

Ack only for enable, disable, swap, create, or edit. Otherwise no `[mode]` line. Comment: `enabled`, `disabled`, `created a file`, or `edited`. A swap on uses `enabled`. Nothing else. On create or edit, the line after `$DIR` is the headings whose body was written, comma-separated (`01, 02`). Omit that line when no heading changed. A heading that only shifted number is not listed.

    [mode] <comment>
    [path] <absolute $DIR>
    [sect] 01, 02
    [next] <next section>
    [dutc] Oct 13, 06:47 PM

The user-facing message is only those five tagged lines. No other chat: no prose, code, findings, or summary. Put the work in the file. `[next]` is the next heading id. At `# AE`, it is `AE`.
UTC is when the prompt was sent: abbreviated month, day with no leading zero, comma, zero-padded 12-hour clock, AM/PM. No year. No zone.

While `TAKEOFF` exists, create `$DIR/05-TAKEOFF.md` on the first substantive query and edit it after that. "Yes", "Done", and tool-only turns: no ack and no file. "next step" runs the heading named in `[next]`. At `# AE`, that is `# AE` again. Each product heading is one thing that was done this turn, including the approach used, as fact. No untaken option, open question, or restatement of the handoff. Omit an empty section.

Before changing the product, read `$DIR/03-HANDOFF.md`, `$DIR/02-CLARIFY.md`, and `$DIR/04-PREPARE.md`. The handoff is what must become true and why. A clarify pin whose first line is `Resolved` wins over a conflicting handoff sentence. No prepare file means do not invent the architecture. A prepare pin whose first line is `Resolved` is how to build. Follow it. Do not pick another way. If that file still has a pin whose first line is `Blocking`, do not invent the choice. Record the stop, and do only the work that does not depend on it.

The file shows only this turn's product work, plus `# AA`, `# AB`, `# AC`, `# AD`, and `# AE` once they exist. Replace every product heading with this turn. Leave `# AA`, `# AB`, `# AC`, `# AD`, and `# AE` unchanged unless this turn is about that heading. Fixing a Bugbot finding, or running Bugbot again, may overwrite `# AC`. A Linear authentication check may overwrite `# AA`. A Linear requirements pass may overwrite `# AB`. A standards pass may overwrite `# AD`. A `# AE` pass may overwrite `# AE`. After the edit, number product headings from `01` in file order. Do not change `# AA`, `# AB`, `# AC`, `# AD`, or `# AE`.

These headings are created the first time the handoff is applied, with product work between `# AA` and `# AB`:

- `# AA` confirms Linear authentication and a Linear URL. In the `linear` MCP namespace, `needsAuth` means not authenticated. Record the URL when one was provided. If Linear is not authenticated or no URL was provided, refuse and stop this file after that heading.
- `# AB` reads that issue and records which of its title, description, and comments the change may have missed.
- `# AC` runs Bugbot. Follow the `review-bugbot` skill: `bugbot` subagent, `description: "Bugbot"`, `subagent_type: "bugbot"`, `run_in_background: false`, `Full Repository Path` set to the absolute git repository, `Diff: branch changes` unless the user asked for uncommitted changes only. Record every finding and how to fix it. Do not apply the fixes in that heading.
- `# AD` checks the first commit message and the current branch against these standards. The first commit message is `[ENG-1234] Issue Title ([#{ISSUE_ID}] #{ISSUE_TITLE})` and must match Linear's Issue Id and Issue Title. The branch is `feature/#{issue-id}-#{issue_title}` and must match Linear's Issue Branch Name. Record each miss.
- `# AE` checks that `# AA` (Linear is authenticated and present), `# AB` (the change matches the scope of the issue, after the user's observations), `# AC` (Bugbot found no findings), and `# AD` (the commit and branch name are correct) are fulfilled. If all are, write `Pull Request ready`. If any is not, write `Pull Request not ready` and the missing section ids. Always write `# AE`. `[next]` is `AE`. "next step" does this check again, even if the last write was `Pull Request ready`.
