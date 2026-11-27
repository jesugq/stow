---
name: markdown-mode
description: "/markdown-mode new <name>, load <folder>, or next <prompt>."
disable-model-invocation: true
---

# Markdown mode

`CURSOR_CONVERSATION_ID` and `AGENT_TRANSCRIPTS` are exported. This skill is the command. Call the Skill tool with `markdown-mode` for the folder, the ack, and the markdown file. A caller passes parameters and does not restate this file. Read this file once, after `begin`. Do not Read it before `begin`. Do not Read it again.
Hard rule: Before any response in this mode, run the `markdown-mode` workflow. Then output only the ack or `refused`.

The first tool is the timer. Run it alone, before any Read, search, or edit.

```
python3 ~/.cursor/skills/markdown-mode/mode.py begin
```

`begin` prints `timer`. It records the start for this conversation. A later `begin` keeps that start. An interrupt keeps that start. The mode shell stops the timer. Run `cancel` with that script when you print `refused` and you do not run the mode shell. `cancel` prints `timer` and drops the open timer.

`/markdown-mode new`, `/markdown-mode load`, and `/markdown-mode next` run it with the direct parameters. `new` takes a name and creates a folder. `load` takes a folder name. A `load` value of `-` requires no markdown file. `next` takes a prompt and stays on the known `$DIR`. A verb with no argument prints `refused` and stops.

## Parameters

Direct commands use these values. A caller replaces the ones it names.

```
verb: new | load | next
root: ~/.cursor/markdown-mode
sentinel: MARKDOWN
drop: -
load: -
need: -
next:
sect: file
```

`verb` is the word immediately after the mode command. `new`, `load`, and `next` are accepted. Anything else, including no word, prints `refused` and stops. That reply has no folder, no file, and no ack. A caller may accept a subset. A verb outside that subset is `refused`.

`root` is the parent of the conversation folders. `sentinel` names a file the shell does not create. `drop` is the sentinels to delete when this mode turns on, comma-separated, or `-`. `load` is `-`, or a file name the folder must contain. `-` requires no markdown file. `NN` means a file named `[0-9][0-9].md`. `need` is a markdown file `next` requires, or `-`. The `next` line is the `[next]` ack. Empty omits `[next]`. `sect` is `file` or `heading`.

`$DIR` is `<root>/<folder>`. The folder name is `YYYY-MM-DD_Name`. One example is `2026-11-26_Passkey_error`. The date is the local calendar date. The name is the argument to `new`. Turn each space in that name into `_` before the shell, so `dir` is one token and the path needs no quotes. After that, the name matches `[A-Za-z0-9][A-Za-z0-9_-]*`. A slash, a quote, or any other character outside that set prints `refused`. The folder name does not contain the conversation id. Do not print a resolved `/Users/...` path. Copy `root` as the caller wrote it, tilde included.

`new` requires the name. Pass that name as `dir`. `load` requires the folder name, one token. Pass that folder name as `dir`. An absolute path, a missing token, or a second token prints `refused`. `new` and `load` do not take a prompt. The message is only the command and that argument. Follow Common and Only the command, then stop.

`next` requires the prompt. The prompt is every word after the verb. No prompt prints `refused` and does not run the shell. The prompt is the work. Follow Common and Work. `next` takes no folder. A folder written beside `next` does not count. `next` is allowed only when an earlier message in this conversation already set `$DIR` with `new` or `load`. The first user message cannot be `next`. Do not use a `[name]` line to discover a folder. No known `$DIR`: pass `-` as `dir`. Do not read the transcript to learn which verb ran.

When the message is `new` or `load` plus its argument, follow Common and Only the command, then stop. Do not read Work. Do not write markdown for that message, including when the caller's skill describes a file. A `next` with a prompt follows Common and Work. The prompt is the message that asks for an answer.

If the message contains more than one of `/markdown-mode`, `/booking-mode`, `/code-discover`, `/code-prioritize`, `/code-define`, `/code-refine`, `/code-execute`, `/plan-discover`, `/plan-prioritize`, `/plan-define`, `/plan-refine`, `/plan-execute`, or `/snap-perform`, the last one is the caller for the whole message. Use that caller's parameters. Write that caller's file and print that ack. A caller may append lines after the ack only when its own skill says so.

A folder this conversation already set stays `$DIR` until a later `new` or `load`. `next` keeps that folder. `next` does not set `$DIR` on its own.

## Common

The prompt timestamp is local. The folder date is that local calendar date, before the offset is applied. Use the local date of the earliest user message whose timestamp you can see. When `new` is the first user message, the folder date is the current stamp's local date.

The live clock is UTC. The parentheses hold the offset in hours, west when negative, east when positive. Subtract the offset from the local clock: offset `-6` adds 6 hours, offset `+2` subtracts 2 hours. Roll the day when the clock crosses midnight. Format: abbreviated month, day with no leading zero, comma, zero-padded 12-hour clock, AM/PM. No year. No zone. A local stamp of Oct 13, 12:47 PM with offset `-6` is `Oct 13, 06:47 PM`. The script prints that clock for the current user message.

The shell does not create a sentinel. A sentinel file whose size is not 0 prints `refused` and writes no markdown.

The mode shell is the last tool. Do not list the environment. Do not Read `~/.cursor/skills/markdown-mode/mode.py`. Do not Read the transcript jsonl. The script checks the folder, stops the timer, prepends the clock and the span to `TIMESTAMPS`, and prints the rows.

```
python3 ~/.cursor/skills/markdown-mode/mode.py <kind> <root> <date> <dir> <sentinel> <load> <need> <drop>
```

Args, in order: `kind`, `root`, `date`, `dir`, `sentinel`, `load`, `need`, `drop`. `kind` is `new`, `load`, `next`, or `count`. `date` is the folder date for `new`, otherwise `-`. `dir` is the name for `new`, the folder name for `load`, `next`, and `count`, and `-` when `next` has no known `$DIR`. Pass `root` as the caller wrote it. `count` is the kind when this conversation already has `$DIR` and the message is work with no `new`, `load`, or `next`.

The first stdout line decides the reply.

- `refused` — print `refused` and stop.
- `ok` — line 2 is the folder name, line 3 the clock and the span (`Nov 26, 07:02 PM | 4m 12s`), line 4 the prompt label (`Prompts 8 | Timestamps 12`). `$DIR` is `<root>/<line 2>`. The script prepends line 3 to `$DIR/TIMESTAMPS` before it prints. One clock per line. Newest first. The span is the open timer. `n/a` means `begin` did not run.

`new` creates `$DIR` as `<root>/<local YYYY-MM-DD>_<name>` and refuses when that folder exists. It does not use the conversation id. `load` uses the folder name from the message. `load` creates no folder. `load` requires a file only when the parameter is not `-`. `next` uses the known folder name and requires `need` when `need` is not `-`. The shell does not create `sentinel`. It deletes each `drop` name. It does not truncate a sentinel that exists. It does not delete markdown.

The speaking message is the next message after this shell. It does not run the shell again and it does not open the jsonl. `[user]` is line 4. `[time]` is line 3. `[name]` is line 2. The clock is the current prompt. The span is the timer. Line 4 counts user messages in this conversation and lines in `TIMESTAMPS`. Print line 4, then line 3. Do not compute a second clock, a second span, or a second count. Do not write `TIMESTAMPS` again.

The user-facing message is only the ack. Print `[user]`, `[time]`, `[make]`, `[edit]`, `[next]`, then `[name]` as plain lines. Do not wrap the ack in a fence. A fence makes the client add line numbers. `[name]` is the folder name from line 2. `[next]` is the `next` line. Omit `[next]` when that line is empty. Omit `[make]` when this turn creates nothing. Omit `[edit]` when this turn updates nothing. `[make]` is the noun, then the numbers. `[edit]` is the noun, then the numbers. `sect: file` uses `Files`. `sect: heading` uses `Headings`. The noun stays plural for one number. A heading that only shifted number is not listed.

Example, as plain lines:

[user] Prompts 8 | Timestamps 12
[time] Nov 26, 07:02 PM | 4m 12s
[make] Headings 01
[edit] Headings 02, 03
[next] /code-prioritize next
[name] 2026-11-23_Passkey_error

## Only the command

Run `begin` first. Run the mode shell once. The speaking message prints the ack or `refused`. It writes no markdown. It deletes nothing.

Stop.

## Work

Run `begin` before any research tool. The mode shell from Common is the last tool invocation before the speaking message. Research tools run after `begin` and before that shell. Do not run a tool after that shell returns.

The speaking message writes the caller's file and prints the ack. Do not end before that file when the message asked for work and the file was not written. Do not take another turn to check the write, lint, or restate the answer.

Each message that asks for an answer writes that file. Once `$DIR` is set, read the markdown files there once and continue from them. Do not read another conversation's transcript. Read each file in `$DIR` at most once per user message. Do not Read a skill file to resume a mode.

A tool result already in the conversation is the file contents. Do not Read that path again. Re-read only when this conversation has edited that file since the last read and a later step needs the new contents, or the user says the file changed outside this conversation. After a successful Write, do not Read the file to confirm it. Do not Read the transcript jsonl. To find a symbol, Grep first and Read only that line range. Do not read a large file to locate a few lines.

A file in the agent cwd is `lua/libfuns/context.lua:26` (relative, colon, line on the right). A file outside that cwd is its absolute path, colon, line on the right. Never `../`. A range is `file.rb:36-53`. Never put the line before the path (`26:file`, `36:53:file`, `254:258:app/policies/practice_policy.rb`). Keep each path in backticks so neovim `` yi` `` selects them. The cite for a fenced quote is that same backtick path, not the fence language. Quote source inline if it is one line, in a fenced block if it is larger, never as bare lines. Open a fence with backticks only. The first line inside is source. Nothing follows those backticks: no language, no line numbers, no path. The lines always go to the right (`app/policies/practice_policy.rb:254-258`). Do not open a fence with `254:258:app/policies/practice_policy.rb`.

## Writing style

The caller decides the sections, the headings, and the focus. This style decides the sentences in those sections. A caller does not restate this style. Do not add a heading for the style. Do not write the output-style frontmatter into the answer file. That frontmatter is `name: STE` and `keep-coding-instructions: true` on the Claude style file. It is not part of the answer.

Write prose in STE-flavored Simplified Technical English. Follow the structural rules of ASD-STE100. This file omits its approved dictionary. Treat word choice as a direction, not a verifiable rule. Drop the style when the user asks for another voice.

The caller's required first line stays the first line. A fixed phrase the caller requires stays as the caller wrote it. The style does not govern code, identifiers, paths, commands, or configuration. Never rename an identifier to satisfy the style. Quote a file, a tool result, an error, or the user exactly.

These rules govern prose in the caller's file, and commit messages, code comments, and documentation.

Check each sentence against these three before you write the next one. Scan the finished draft for all three before you send it.

1. Name the actor. Look for a form of `be` or `get` before a past participle. Name who acts, or rewrite. A state description is fine: nothing acts in "the file is corrupted". Wrong: "Code blocks are stripped." Right: "The script strips code blocks."
2. One idea per sentence. Look for `, and`, `, but`, or `, so` joining two clauses. Split the sentence. `, so` leaks most often. Wrong: "It spreads load, so no machine saturates." Right: "It spreads load. No machine saturates."
3. Repeat the verb. Never replace a verb you already used with `did`, `does`, or `is`. Wrong: "Topic changed at the same moment the style did." Right: "Topic changed at the same moment the style changed."

Cap an instruction at 20 words. Cap a description at 25. Use no semicolons. Write two sentences. Stack 3 nouns at most. Write "the handler for the retry backoff policy", not "request retry backoff policy handler". Use simple tenses. Keep a compound tense that carries information: "the build has finished" states current relevance. Put one topic in one paragraph. Cap it at 6 sentences. Use a numbered list for 3 or more steps. Use a bulleted list for 3 or more parallel items.

Use one name for one thing. Do not rotate synonyms. Prefer the plain verb. Write "start", not "spin up". Write "read", not "dive into". Prefer the verb to its noun form. Write "analyze the log", not "perform an analysis of the log". Delete marketing adjectives: seamless, robust, powerful, blazing-fast, cutting-edge, effortless. Give the measurement that earns the claim, or write nothing. Delete stacked hedges. One hedge at true strength carries information. Three carry none.

Cut what carries no information. Delete a section before compressing every sentence in it. Cut preamble, self-narration, and the closing offer. Cut a point you already made. Cut filler openers: "I will now", "let me", "it is worth noting that". Cut any adjective that states no measurement.

Keep every hedge at its original strength. "The test may have failed" is not "the test failed". Keep every condition, exception, number, and scope qualifier. Add no fact you have not verified. A sentence that reads better because it supplies a cause has stopped being true. Stop when the sentence is unambiguous, not when it is shortest. Say what you kept and why. Put that sentence in the section you changed. When the caller forbids a sentence that is not the section's focus, keep the qualifier in the required sentence and add no extra sentence.

In the file, put the answer in the first sentence after any required first line. The chat message stays the ack.

`sect: file` writes one new file, `$DIR/NN.md`. `NN` is `01`, then `02`, in the order written. The first line is `# NN`, the file number alone (`# 01` in `01.md`). A blank line follows. The rest is the whole answer. That prose follows Writing style. Do not add another heading. Do not split the answer into more than one file. Do not change an earlier file. One speaking message writes that one file, then stops. Do not run test suites or test runners. Do not run rspec, QUnit, ember test, pnpm test, `sp rspec`, `sp exec test:browser`, dockerized test containers, or a retry loop around those. Do not start, stop, or probe containers. Do not run checksums, docker logs, or curl probes.

`sect: heading` writes the caller's named file. H1 only. No frontmatter. No JSON. The first heading starts the file. A blank line follows every heading, and a blank line precedes every later heading. A heading keeps its number while it stays. The caller names the headings and the bodies. Prose in a body follows Writing style. Do not delete the markdown. One speaking message writes that file, then stops.

No other chat: no prose, code, findings, or summary. Put the answer in the file.
