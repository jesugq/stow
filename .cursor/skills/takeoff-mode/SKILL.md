---
name: takeoff-mode
description: /takeoff-mode. Next: no follow up mode.
disable-model-invocation: true
---

# Takeoff mode

`$DIR` is a directory under `~/.cursor/dynamic-mode` that has a `TAKEOFF` sentinel, else one that has a `PREPARE` sentinel. Prefer `TAKEOFF` so a new conversation can resume after Linear is not authenticated. Walk dates descending, newest first. If several of that kind, use the newest. Refuse if none. Do not choose by conversation id, and do not create a new folder. Order: analyze → clarify → handoff → prepare → takeoff. This mode's only file is `$DIR/05-TAKEOFF.md`. The others are `$DIR/01-ANALYZE.md`, `$DIR/02-CLARIFY.md`, `$DIR/03-HANDOFF.md`, `$DIR/04-PREPARE.md`.
On iff `$DIR/TAKEOFF` exists (zero-byte). Other mode sentinels: `ANALYZE`, `CLARIFY`. Mutually exclusive with those; none of them and no `TAKEOFF` means this mode is off. Keep `PREPARE` and `HANDOFF`; do not delete them. `/takeoff-mode` enables or resumes; extra words are ignored. If `TAKEOFF` already exists, resume: do not delete it. `/analyze-mode`, `/clarify-mode`, `/handoff-mode`, and `/prepare-mode` are not this mode: do not write a file and do not print `[mode]`. Swap deletes `ANALYZE` or `CLARIFY` and creates `TAKEOFF` if absent. Off deletes only `TAKEOFF`. The markdown stays. Each turn this mode is on, after `$DIR` exists, `shasum -a 256` this `SKILL.md` and compare the 64 hex to `$DIR/takeoff-mode.sha256`. If that file is missing or the digest differs, Read this `SKILL.md`, write the 64 hex there, and follow the Read. If it matches, do not Read this file.

H1 only. No frontmatter. No JSON. The first heading starts the file. Blank line after every heading and before every later one. Headings are `# 01 <5-10 word title>`, then `02`, `03`, in file order. When referring to a file, use one of two: a file in the agent cwd is `lua/libfuns/context.lua:26` (relative, colon, line on the right); a file outside that cwd is its absolute path, colon, line on the right; never `../`. A range is `file.rb:36-53`. Never put the line before the path (`26:file`, `36:53:file`). Keep each path in backticks so neovim `` yi` `` selects them; the cite for a fenced quote is that same backtick path, not the fence language. Quote source inline if it is one line, in a fenced block if it is larger; never as bare lines. Open a fence with backticks only; the first line inside is source.

Ack only for enable, disable, swap, create, or edit. Otherwise no `[mode]` line. Comment: `enabled`, `disabled`, `created a file`, or `edited`. A swap on uses `enabled`. Nothing else. On create or edit, the line after `$DIR` is the headings whose body was written, comma-separated (`01, 02`). Omit that line when no heading changed. A heading that only shifted number is not listed.

    [mode] <comment>
    [path] <absolute $DIR>
    [sect] 01, 02
    [next] <next section>
    [dutc] Oct 13, 06:47 PM

The user-facing message is only those five tagged lines. No other chat: no prose, code, findings, or summary. Put the work in the file. One heading per turn; stop after it. Do not run a later heading in the same turn. `[next]` is the next heading id. At `# AE`, it is `AE`.
UTC is when the prompt was sent: abbreviated month, day with no leading zero, comma, zero-padded 12-hour clock, AM/PM. No year. No zone.

While `TAKEOFF` exists, create `$DIR/05-TAKEOFF.md` when it is absent, including the enable or resume turn, and run only `# AA`. Stop after that heading. A new conversation that finds `TAKEOFF` resumes the same way: only `# AA`, then stop. Edit it after that. "Yes", "Done", and tool-only turns: no ack and no file. "next step" runs only the heading named in `[next]`, then stops. At `# AE`, that is `# AE` again. Each product heading is one thing that was done this turn, including the approach used, as fact. No untaken option, open question, or restatement of the handoff. Omit an empty section. Never write `# AB`, `# AC`, `# AD`, or `# AE` until that heading is the one `[next]` named.

Before changing the product, read `$DIR/03-HANDOFF.md`, `$DIR/02-CLARIFY.md`, and `$DIR/04-PREPARE.md`. The handoff is what must become true and why. A clarify pin whose first line is `Resolved` wins over a conflicting handoff sentence. No prepare file means do not invent the architecture. A prepare pin whose first line is `Resolved` is how to build. Follow it. Do not pick another way. If that file still has a pin whose first line is `Blocking`, do not invent the choice. Record the stop, and do only the work that does not depend on it.

The file shows only this turn's one product heading, plus `# AA`, `# AB`, `# AC`, `# AD`, and `# AE` once they exist. Replace the product heading this turn ran. Leave `# AA`, `# AB`, `# AC`, `# AD`, and `# AE` unchanged unless this turn is about that heading. Fixing a Bugbot finding, or running Bugbot again, may overwrite `# AC`. A Linear authentication check may overwrite `# AA`. A Linear requirements pass may overwrite `# AB`. A standards pass may overwrite `# AD`. A `# AE` pass may overwrite `# AE`. After the edit, number product headings from `01` in file order. Do not change `# AA`, `# AB`, `# AC`, `# AD`, or `# AE`.

These headings appear in this order in the file, with product work between `# AA` and `# AB`. Create only the heading this turn runs. Do not create the rest in advance:

- `# AA` confirms Linear authentication and a Linear URL. In the `linear` MCP namespace, `needsAuth` means not authenticated. Record the URL when one was provided. If Linear is not authenticated or no URL was provided, refuse and stop this file after that heading.
- `# AB` reads that issue and records which of its title, description, and comments the change may have missed.
- `# AC` runs Bugbot. Follow the `review-bugbot` skill: `bugbot` subagent, `description: "Bugbot"`, `subagent_type: "bugbot"`, `run_in_background: false`, `Full Repository Path` set to the absolute git repository, `Diff: branch changes` unless the user asked for uncommitted changes only. Record every finding and how to fix it. Do not apply the fixes in that heading.
- `# AD` checks the current branch for a commit whose message is `[ENG-1234] Issue Title ([#{ISSUE_ID}] #{ISSUE_TITLE})` using the Linear Issue Id from the URL (`[IDT-9999]` when the id is `IDT-9999`). That commit may sit anywhere on the branch: it need not be the first or the last. Later commits or a staging merge do not fail the check. The branch name need not match Linear's Issue Branch Name. Record a miss only if no commit on the branch uses that `[ISSUE_ID]` form.
- `# AE` checks that `# AA` (Linear is authenticated and present), `# AB` (the change matches the scope of the issue, after the user's observations), `# AC` (Bugbot found no findings), and `# AD` (a `[ISSUE_ID]` commit exists on the branch) are fulfilled. If all are, write `Pull Request ready`. If any is not, write `Pull Request not ready` and the missing section ids. Write `# AE` only when this step runs. After `# AA`, `[next]` is `01` if product work remains, else `AB`. After `# AD`, `[next]` is `AE`. At `# AE`, `[next]` is `AE`. "next step" does this check again, even if the last write was `Pull Request ready`.
