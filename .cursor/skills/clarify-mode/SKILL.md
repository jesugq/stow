---
name: clarify-mode
description: /clarify-mode. Next: /handoff-mode.
disable-model-invocation: true
---

# Clarify mode

`$DIR = ~/.cursor/dynamic-mode/<first-message local YYYY-MM-DD>-<$CURSOR_CONVERSATION_ID>` (no spaces; refuse if the id is unset). Reuse a folder ending in that id; if several, use the earliest date. Do not open a second folder on a later day. Do not pick a folder by a `HANDOFF` sentinel. Order: analyze → clarify → handoff → prepare → takeoff. This mode's only file is `$DIR/02-CLARIFY.md`. The others are `$DIR/01-ANALYZE.md`, `$DIR/03-HANDOFF.md`, `$DIR/04-PREPARE.md`, `$DIR/05-TAKEOFF.md`.
On iff `$DIR/CLARIFY` exists (zero-byte). Other sentinels: `ANALYZE`, `HANDOFF`, `PREPARE`, `TAKEOFF`. Mutually exclusive; none means off. A mode command may sit anywhere in the message. If more than one of `/analyze-mode`, `/clarify-mode`, `/handoff-mode`, `/prepare-mode`, or `/takeoff-mode` appears, the last one is the mode for the whole message. Switch the sentinel first, using the swap rules already in that skill, then follow the new mode for the rest of that same message. Do not stop after creating the sentinel. Do not answer with only the `[mode]` ack when the message also asks for work. A message that is only the slash command still only toggles. `/clarify-mode` toggles this mode. Swap deletes the other sentinel and creates `CLARIFY`. Off deletes only `CLARIFY`. The markdown stays. When the last command is not `/clarify-mode`, do not write this mode's file and do not print `[mode]`.

H1 only. No frontmatter. No JSON. The first heading starts the file. Blank line after every heading and before every later one. Headings are `# 01 <5-10 word ambiguity>`, then `02`, `03`, in order. A heading keeps its number while it stays. When referring to a file, use one of two: a file in the agent cwd is `lua/libfuns/context.lua:26` (relative, colon, line on the right); a file outside that cwd is its absolute path, colon, line on the right; never `../`. A range is `file.rb:36-53`. Never put the line before the path (`26:file`, `36:53:file`). Keep each path in backticks so neovim `` yi` `` selects them; the cite for a fenced quote is that same backtick path, not the fence language. Quote source inline if it is one line, in a fenced block if it is larger; never as bare lines. Open a fence with backticks only; the first line inside is source.

A tool result already in the conversation is the file contents. Do not Read that path again. Re-read only when this conversation has edited that file since the last read and a later step needs the new contents, or the user says the file changed outside this conversation. After a successful StrReplace or Write, do not Read the file to confirm it. Do not re-read `$DIR/01-ANALYZE.md`, `$DIR/02-CLARIFY.md`, `$DIR/03-HANDOFF.md`, `$DIR/04-PREPARE.md`, or `$DIR/05-TAKEOFF.md` before each edit. Read each of them at most once per user message. Do not Read `SKILL.md` to resume a mode. To find a symbol, Grep first and Read only that line range. Do not read a large file to locate a few lines.

Ack only for enable, disable, swap, create, or edit. Otherwise no `[mode]` line. Comment: `enabled`, `disabled`, `created a file`, or `edited`. A swap on uses `enabled`. Nothing else. On create or edit, the line after `$DIR` is the numbers of headings whose body was written, comma-separated (`01, 02`). Omit that line when no heading changed.

    [mode] <comment>
    [path] <absolute $DIR>
    [sect] 01, 02
    [next] /handoff-mode
    [dutc] Oct 13, 06:47 PM

The user-facing message is only those five tagged lines. No other chat: no prose, code, findings, or summary. Put the work in the file.
UTC is when the prompt was sent: abbreviated month, day with no leading zero, comma, zero-padded 12-hour clock, AM/PM. No year. No zone.

While `CLARIFY` exists, a turn that opens, updates, or resolves an ambiguity edits `$DIR/02-CLARIFY.md`. Create it only when it is absent. One ambiguity per heading. Change only the pins this turn opens, updates, or resolves. No board change: no ack and no file. A short ack that settles a pin is an edit.

Read `$DIR/01-ANALYZE.md` and `$DIR/02-CLARIFY.md`. The analyze file is the investigation. The clarify file is the board; absent means no pins. A new pin is a choice the analyze file leaves open that would change the handoff. Do not pin what it already settles. No analyze file means no new pins. Leave code structure for prepare.

The heading text after the number is the tab. Reuse it exactly. Match the user's message to pin bodies, not heading text or answer order. One message that would settle two headings is one pin. The first line of every body is the status alone: `Blocking`, `Deferrable`, or `Resolved`. Always write it. Open means that line is `Blocking` or `Deferrable`. Closing sets that line to `Resolved` and writes the decision in the lines after, including an accepted recommendation, and leaves the heading in the file.

An open body after the status line says what is undecided in the handoff intention, what would settle it, and the option the handoff should use if accepted. `Blocking` must close before handoff. `Deferrable` may stay open through handoff. Do not write `Resolved` while a choice is open. Settled means the user chose, accepted the recommendation, or the implementation already decides it.
