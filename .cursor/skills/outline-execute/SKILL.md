---
name: outline-execute
description: /outline-execute load, next, or join.
disable-model-invocation: true
---

# Outline execute mode

Call the Skill tool with `markdown-mode` for the folder, the ack, and the markdown file.
    10|
```
verb: load | next | join
root: ~/.cursor/outline-mode
sentinel: OUTLINE_EXECUTE
drop: OUTLINE_ANALYZE,OUTLINE_CLARIFY
load: 05-EXECUTE.md
need: 04-PREPARE.md
mark: OUTLINE_PREPARE
step:
    20|sect: heading
```

`load`, `next`, and `join` are accepted. This mode's file is `$DIR/05-EXECUTE.md`.

While `OUTLINE_EXECUTE` exists, one message that asks for documentation work does the whole pass. Read `$DIR/03-HANDOFF.md`, `$DIR/02-CLARIFY.md`, and `$DIR/04-PREPARE.md` once. Resolved clarify pins override conflicting handoff or prepare text.

Do not write partial final output in multiple passes unless the user asked for a revision. Create `05-EXECUTE.md` when it is absent. Write it once per pass at the end.

The file structure is:
- `# AA` readiness checks
- document sections from the resolved plan
- `# AZ` final readiness verdict

`# AA` must verify:
- `doc_type` is resolved to one of `prd`, `tdd`, or `issue`
- all `Blocking` prepare pins are resolved
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
