---
name: plan-execute
description: "/plan-execute load <folder> or next <prompt>."
disable-model-invocation: true
---

# Plan execute mode

Call the Skill tool on the `markdown-mode` skill. That skill sets the folder, the ack, and the markdown file.
Hard rule: Before any response in this mode, run the `markdown-mode` workflow. Then output only the ack or `refused`.
```
verb: load | next
root: areas/plans
load: -
need: 04-REFINE.md
prev: plan-refine
curr: Plan execute
next: none
sect: heading
```

`load` and `next` are accepted. `load` accepts the folder name. A work message with no verb uses `count`. This mode's file is `$DIR/05-EXECUTE.md`.

One message that asks for the document, or agrees to it, does the whole pass. Any wording counts. A turn that only runs commands writes nothing. Read `$DIR/03-DEFINE.md`, `$DIR/02-PRIORITIZE.md`, and `$DIR/04-REFINE.md` once. Resolved prioritize pins override conflicting define or refine text.

Do not write partial final output in multiple passes unless the user asked for a revision. Create `05-EXECUTE.md` when it is absent. Write it once per pass at the end.

The file structure is:
- `# AA` readiness checks
- document sections from the resolved plan
- `# AZ` final readiness verdict

`# AA` must verify:
- `doc_type` is resolved to one of `prd`, `tdd`, or `issue`
- all `Blocking` refine pins are resolved
- required section map for selected `doc_type` is satisfied

If `# AA` fails, stop after `# AA` and list what is missing.

`# AZ` must write one of:
- `Document ready`
- `Document not ready`

If not ready, list the missing or unresolved requirements by section name.

Per-type acceptance checks:
- `prd`: includes problem, source of demand, desired outcome, measurable success criteria, scope boundary, constraints, and risks/caveats
- `tdd`: includes objective, background, goals/non-goals, design overview, alternatives considered, caveats, testing plan, and rollout strategy
- `issue`: includes issue kind (`Bug` or `Work`), clear scope, actionable acceptance criteria, verification details, and references

Global writing guardrails:
- No PHI or sensitive customer content
- Prefer omission over filler
- Mark unknowns as `Unknown: ...`
