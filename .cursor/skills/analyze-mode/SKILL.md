---
name: analyze-mode
description: /analyze-mode new or load. Next: /clarify-mode next.
disable-model-invocation: true
---

# Analyze mode

The argument is the word immediately after `/analyze-mode`. `new` and `load` are accepted. Anything else, including no word, refuses. The message is `/analyze-mode new` or `/analyze-mode load`. No ack. No file. No folder. `new` sets `$DIR` to `~/.cursor/dynamic-mode/<first-message local YYYY-MM-DD>-<$CURSOR_CONVERSATION_ID>` (no spaces; refuse if the id is unset). Create that directory when absent. Do not search. `load` finds `01-ANALYZE.md` under `~/.cursor/dynamic-mode`. One file: its directory is `$DIR`. More than one: ask which conversation. The message is `Which conversation?` and the absolute paths, each in backticks. No ack. No file write. Stop. The reply picks one path. Then that file's directory is `$DIR` and setup continues. No file: refuse. Do not create a folder. A folder this conversation already set stays `$DIR` until a later `new` or `load`. Once `$DIR` is set, read the mode files that are present once and continue from them. Do not read another conversation's transcript. Order: analyze → clarify → handoff → prepare → takeoff. This mode's only file is `$DIR/01-ANALYZE.md`. The others are `$DIR/02-CLARIFY.md`, `$DIR/03-HANDOFF.md`, `$DIR/04-PREPARE.md`, `$DIR/05-TAKEOFF.md`.
On iff `$DIR/ANALYZE` exists (zero-byte). Other sentinels: `CLARIFY`, `HANDOFF`, `PREPARE`, `TAKEOFF`. Mutually exclusive; none means off. A mode command may sit anywhere in the message. If more than one of `/analyze-mode`, `/clarify-mode`, `/handoff-mode`, `/prepare-mode`, or `/takeoff-mode` appears, the last one is the mode for the whole message. Its argument is the one that is checked. Switch the sentinel first, using the swap rules already in that skill, then follow the new mode for the rest of that same message. Do not stop after creating the sentinel. A message that is only the mode command and an accepted argument sets the sentinel and prints the ack. It does not write the markdown. The turn that sets `$DIR` leaves an existing `ANALYZE` in place and creates it when absent. Swap deletes the other sentinel and creates `ANALYZE`. Do not delete the markdown. When the last command is not `/analyze-mode`, do not write this mode's file and do not print the ack.

H1 only. No frontmatter. No JSON. The first heading starts the file. Blank line after every heading and before every later one. Headings are `# 01 <5-10 word title>`, then `02`, `03`, in order. A heading keeps its number while it stays. When referring to a file, use one of two: a file in the agent cwd is `lua/libfuns/context.lua:26` (relative, colon, line on the right); a file outside that cwd is its absolute path, colon, line on the right; never `../`. A range is `file.rb:36-53`. Never put the line before the path (`26:file`, `36:53:file`). Keep each path in backticks so neovim `` yi` `` selects them; the cite for a fenced quote is that same backtick path, not the fence language. Quote source inline if it is one line, in a fenced block if it is larger; never as bare lines. Open a fence with backticks only; the first line inside is source.

A tool result already in the conversation is the file contents. Do not Read that path again. Re-read only when this conversation has edited that file since the last read and a later step needs the new contents, or the user says the file changed outside this conversation. After a successful StrReplace or Write, do not Read the file to confirm it. Do not re-read `$DIR/01-ANALYZE.md`, `$DIR/02-CLARIFY.md`, `$DIR/03-HANDOFF.md`, `$DIR/04-PREPARE.md`, or `$DIR/05-TAKEOFF.md` before each edit. Read each of them at most once per user message. Do not Read `SKILL.md` to resume a mode. To find a symbol, Grep first and Read only that line range. Do not read a large file to locate a few lines.

On create or edit, the line after `$DIR` is `created` or `updated`, then `heading` or `headings`, then the numbers whose body was written (`created heading 01`, `updated headings 02, 03`). One number uses `heading`. More than one uses `headings`. A turn that both creates and updates lists created first, then updated (`created heading 01, updated headings 02, 03`). Omit that line when no heading changed.

    [path] <absolute $DIR>
    [sect] created heading 01, updated headings 02, 03
    [next] /clarify-mode next
    [dutc] Oct 13, 06:47 PM
    [call] Prompts: 4, Callbacks: 11

The user-facing message is only those five tagged lines. A file question is the exception: that message is `Which conversation?` and the paths. No ack. No file. No other chat: no prose, code, findings, or summary. Put the work in the file.
UTC is when the prompt was sent: abbreviated month, day with no leading zero, comma, zero-padded 12-hour clock, AM/PM. No year. No zone.
`[call]` is `Prompts: <n>, Callbacks: <n>`: user prompts in this conversation, then model callbacks. Count `user` lines and `assistant` lines in `$AGENT_TRANSCRIPTS/$CURSOR_CONVERSATION_ID/$CURSOR_CONVERSATION_ID.jsonl`. Include this message. The current callback is not in the file yet; add one.

While `ANALYZE` exists, create `$DIR/01-ANALYZE.md` on the first substantive query and edit it after that. Each heading is one finding clarify would decide differently without. Add or replace only that heading. Do not rewrite an unchanged heading, and do not write the rest of the investigation. "Yes", "Done", and tool-only turns that are not this mode: no ack and no file.
