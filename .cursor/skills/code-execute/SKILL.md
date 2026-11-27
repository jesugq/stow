---
name: code-execute
description: "/code-execute load <folder> or next <prompt>."
disable-model-invocation: true
---

# Execute mode

Call the Skill tool on the `markdown-mode` skill. That skill sets the folder, the ack, and the markdown file.
Hard rule: Before any response in this mode, run the `markdown-mode` workflow. Then output only the ack or `refused`.
```
verb: load | next
root: areas/codes
load: -
need: 04-REFINE.md
prev: code-refine
curr: Execute
next: none
sect: heading
```

`load` and `next` are accepted. `load` accepts the folder name. A work message with no verb uses `count`. This mode's file is `$DIR/05-EXECUTE.md`.

One message that asks for the work, or agrees to it, does the whole pass. Any wording counts. A turn that only runs commands writes nothing. Read `$DIR/03-DEFINE.md`, `$DIR/02-PRIORITIZE.md`, and `$DIR/04-REFINE.md` once. The define is what must become true and why. A prioritize pin whose first line is `Resolved` wins over a conflicting define sentence. No refine file means do not invent the architecture. A refine pin whose first line is `Resolved` is how to build. Follow it. Do not pick another way. If Linear needs auth or no Linear URL was provided, stop after `# AA`. If a refine pin is still `Blocking`, do not invent the choice, record the stop, and do only the work that does not depend on it. Those are the only stops. Do not stop between product headings.

Implement every product heading the refine file and the user message require. Then write `# AA`, the product headings, `# AB`, `# AC`, `# AD`, `# AE`, and `# AF` in the same pass. On the Linear stop, write `# AA` only. Write `$DIR/05-EXECUTE.md` once at the end of the pass, not once per heading. Create that file when it is absent. Record each product heading as one thing that was done, including the approach used, as fact. No untaken option, open question, or restatement of the define.

The file shows `# AA`, the product headings, `# AB`, `# AC`, `# AD`, `# AE`, and `# AF`, with product work between `# AA` and `# AB`. Omit an empty section. Number product headings from `01` in file order. Do not change `# AA`, `# AB`, `# AC`, `# AD`, `# AE`, or `# AF`. A Linear authentication check may overwrite `# AA`. A Linear requirements pass may overwrite `# AB`. Fixing a Bugbot finding, or running Bugbot again, may overwrite `# AC`. A standards pass may overwrite `# AD`. A `# AE` pass may overwrite `# AE`. A test-file pass may overwrite `# AF`.

These headings appear in this order:

- `# AA` confirms Linear authentication and a Linear URL. In the `linear` MCP namespace, `needsAuth` means not authenticated. Record the URL when one was provided. If Linear is not authenticated or no URL was provided, refuse and stop this file after that heading.
- `# AB` reads that issue and records which of its title, description, and comments the change may have missed.
- `# AC` runs Bugbot. Follow the `review-bugbot` skill: `bugbot` subagent, `description: "Bugbot"`, `subagent_type: "bugbot"`, `run_in_background: false`, `Full Repository Path` set to the absolute git repository, `Diff: branch changes` unless the user asked for uncommitted changes only. Record every finding and how to fix it. Do not apply the fixes in that heading.
- `# AD` checks the current branch for a commit whose message is `[ENG-1234] Issue Title ([#{ISSUE_ID}] #{ISSUE_TITLE})` using the Linear Issue Id from the URL (`[IDT-9999]` when the id is `IDT-9999`). That commit may sit anywhere on the branch: it need not be the first or the last. Later commits or a staging merge do not fail the check. The branch name need not match Linear's Issue Branch Name. Record a miss only if no commit on the branch uses that `[ISSUE_ID]` form.
- `# AE` checks that `# AA` (Linear is authenticated and present), `# AB` (the change matches the scope of the issue, after the user's observations), `# AC` (Bugbot found no findings), and `# AD` (a `[ISSUE_ID]` commit exists on the branch) are fulfilled. If all are, write `Pull Request ready`. If any is not, write `Pull Request not ready` and the missing section ids.
- `# AF` lists each test file this pass added or changed. Under each file, write a short description of what that file tests. Do not run those tests. Do not list the tests after the ack.

Do not run test suites or test runners. Do not run rspec, QUnit, ember test, pnpm test, `sp rspec`, `sp exec test:browser`, dockerized test containers, or a retry loop around those. Do not start, stop, or probe containers in order to test. Bugbot for `# AC` stays.
