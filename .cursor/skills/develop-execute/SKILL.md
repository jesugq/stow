---
name: develop-execute
description: /develop-execute load, next, or join.
disable-model-invocation: true
---

# Execute mode

Call the Skill tool with `markdown-mode` for the folder, the ack, and the markdown file.
    10|    10|
```
verb: load | next | join
root: ~/.cursor/dynamic-mode
sentinel: EXECUTE
drop: ANALYZE,CLARIFY
load: 05-EXECUTE.md
need: 04-PREPARE.md
mark: PREPARE
step:
    20|    20|sect: heading
```

`load`, `next`, and `join` are accepted. This mode's file is `$DIR/05-EXECUTE.md`. Keep `PREPARE` and `HANDOFF`.

While `EXECUTE` exists, one message that asks for work does the whole pass. Read `$DIR/03-HANDOFF.md`, `$DIR/02-CLARIFY.md`, and `$DIR/04-PREPARE.md` once. The handoff is what must become true and why. A clarify pin whose first line is `Resolved` wins over a conflicting handoff sentence. No prepare file means do not invent the architecture. A prepare pin whose first line is `Resolved` is how to build. Follow it. Do not pick another way. If Linear needs auth or no Linear URL was provided, stop after `# AA`. If a prepare pin is still `Blocking`, do not invent the choice, record the stop, and do only the work that does not depend on it. Those are the only stops. Do not stop between product headings.

Implement every product heading the prepare file and the user message require. Then write `# AA`, the product headings, `# AB`, `# AC`, `# AD`, and `# AE` in the same pass. On the Linear stop, write `# AA` only. Write `$DIR/05-EXECUTE.md` once at the end of the pass, not once per heading. Create that file when it is absent. Record each product heading as one thing that was done, including the approach used, as fact. No untaken option, open question, or restatement of the handoff. "Yes", "Done", and tool-only turns: no ack and no file.

The file shows `# AA`, the product headings, `# AB`, `# AC`, `# AD`, and `# AE`, with product work between `# AA` and `# AB`. Omit an empty section. Number product headings from `01` in file order. Do not change `# AA`, `# AB`, `# AC`, `# AD`, or `# AE`. A Linear authentication check may overwrite `# AA`. A Linear requirements pass may overwrite `# AB`. Fixing a Bugbot finding, or running Bugbot again, may overwrite `# AC`. A standards pass may overwrite `# AD`. A `# AE` pass may overwrite `# AE`.
    30|    30|
These headings appear in this order:

- `# AA` confirms Linear authentication and a Linear URL. In the `linear` MCP namespace, `needsAuth` means not authenticated. Record the URL when one was provided. If Linear is not authenticated or no URL was provided, refuse and stop this file after that heading.
- `# AB` reads that issue and records which of its title, description, and comments the change may have missed.
- `# AC` runs Bugbot. Follow the `review-bugbot` skill: `bugbot` subagent, `description: "Bugbot"`, `subagent_type: "bugbot"`, `run_in_background: false`, `Full Repository Path` set to the absolute git repository, `Diff: branch changes` unless the user asked for uncommitted changes only. Record every finding and how to fix it. Do not apply the fixes in that heading.
- `# AD` checks the current branch for a commit whose message is `[ENG-1234] Issue Title ([#{ISSUE_ID}] #{ISSUE_TITLE})` using the Linear Issue Id from the URL (`[IDT-9999]` when the id is `IDT-9999`). That commit may sit anywhere on the branch: it need not be the first or the last. Later commits or a staging merge do not fail the check. The branch name need not match Linear's Issue Branch Name. Record a miss only if no commit on the branch uses that `[ISSUE_ID]` form.
- `# AE` checks that `# AA` (Linear is authenticated and present), `# AB` (the change matches the scope of the issue, after the user's observations), `# AC` (Bugbot found no findings), and `# AD` (a `[ISSUE_ID]` commit exists on the branch) are fulfilled. If all are, write `Pull Request ready`. If any is not, write `Pull Request not ready` and the missing section ids.

After the ack, when this pass wrote the implementation, list the test commands. Do not run test suites or test runners. Do not run rspec, QUnit, ember test, pnpm test, `sp rspec`, `sp exec test:browser`, dockerized test containers, or a retry loop around those. Do not start, stop, or probe containers in order to test. After the implementation is written, the user-facing message lists every command needed to test the whole implementation, in the order to run them. Each command is copy-pasteable and scoped to the files this pass changed: spec paths for backend, the QUnit filter for frontend. Use the repo's `sp` runner. Do not include exploratory commands, docker logs, curl probes, or checksums. Bugbot for `# AC` stays. Do not put Bugbot in the test-command list.
    40|    40|
