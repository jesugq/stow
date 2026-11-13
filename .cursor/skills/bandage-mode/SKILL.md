---
name: bandage-mode
description: /bandage-mode new or load.
disable-model-invocation: true
---

# Bandage mode

The argument is the word immediately after `/bandage-mode`. `new` and `load` are accepted. Anything else, including no word, refuses. The message is `/bandage-mode new` or `/bandage-mode load`. No ack. No file. No folder. `new` sets `$DIR` to `~/.cursor/bandage-mode/<first-message local YYYY-MM-DD>-<$CURSOR_CONVERSATION_ID>` (no spaces; refuse if the id is unset). Create that directory when absent. Do not search. `load` finds a directory under `~/.cursor/bandage-mode` that contains an `NN.md` file. A `BANDAGE` file with no `NN.md` is not a conversation. One directory: that directory is `$DIR`. More than one: ask which conversation. The message is `Which conversation?` and the absolute paths, each in backticks. No ack. No file write. Stop. The reply picks one path. Then that file's directory is `$DIR` and setup continues. No directory: refuse. Do not create a folder. A folder this conversation already set stays `$DIR` until a later `new` or `load`. Once `$DIR` is set, read the `NN.md` files there once and continue from them. Do not read another conversation's transcript. The next number is one higher than the highest `NN.md` in `$DIR`.
On iff `$DIR/BANDAGE` exists (zero-byte). The turn that sets `$DIR` leaves an existing `BANDAGE` in place and creates it when absent. The command may sit anywhere in the message. A message that is only the mode command and an accepted argument sets the sentinel and prints the ack. It does not write an answer. Do not delete the markdown. If the message also asks for work, create the sentinel first, then write the answer in that same message. Do not stop after creating the sentinel.
The answer is one new file, `$DIR/NN.md`. `NN` is `01`, then `02`, in the order written. The first line is `# NN`, the file number alone (`# 01` in `01.md`). A blank line follows. The rest is the whole answer. Do not add another heading. Do not split the answer into more than one file. Do not change an earlier file. When referring to a file, use one of two: a file in the agent cwd is `lua/libfuns/context.lua:26` (relative, colon, line on the right); a file outside that cwd is its absolute path, colon, line on the right; never `../`. A range is `file.rb:36-53`. Never put the line before the path (`26:file`, `36:53:file`, `254:258:app/policies/practice_policy.rb`). Keep each path in backticks so neovim `` yi` `` selects them; the cite for a fenced quote is that same backtick path, not the fence language. Quote source inline if it is one line, in a fenced block if it is larger; never as bare lines. Open a fence with backticks only; the first line inside is source. Nothing follows those backticks: no language, no line numbers, no path. The lines always go to the right (`app/policies/practice_policy.rb:254-258`). Do not open a fence with `254:258:app/policies/practice_policy.rb`.

A tool result already in the conversation is the file contents. Do not Read that path again. Re-read only when this conversation has edited that file since the last read and a later step needs the new contents, or the user says the file changed outside this conversation. After a successful Write, do not Read the file to confirm it. After the setup read, do not Read an earlier `NN.md` again. Do not Read `SKILL.md` again. Do not Read the transcript jsonl. To find a symbol, Grep first and Read only that line range. Do not read a large file to locate a few lines.

One message writes one file, then stops. Do not take another turn to check the write, lint, or restate the answer. Batch the `[call]` count with any search. `[call]` counts `user` lines and `assistant` lines in `$AGENT_TRANSCRIPTS/$CURSOR_CONVERSATION_ID/$CURSOR_CONVERSATION_ID.jsonl`. Use one command whose only output is those two counts. Include this message. The current callback is not in the file yet; add one.

Do not run test suites or test runners. Do not run rspec, QUnit, ember test, pnpm test, `sp rspec`, `sp exec test:browser`, dockerized test containers, or a retry loop around those. Do not start, stop, or probe containers. Do not run checksums, docker logs, or curl probes.

On create, the line after `$DIR` is `created file` and the file number (`created file 01`). Omit that line when no file was written.

    [path] <absolute $DIR>
    [sect] created file 01
    [dutc] Oct 13, 06:47 PM
    [call] Prompts: 4, Callbacks: 11

The user-facing message is only those tagged lines. A file question is the exception: that message is `Which conversation?` and the paths. No ack. No file. No other chat: no prose, code, findings, or summary. Put the answer in the file.
UTC is when the prompt was sent: abbreviated month, day with no leading zero, comma, zero-padded 12-hour clock, AM/PM. No year. No zone.
`[call]` is `Prompts: <n>, Callbacks: <n>`: user prompts in this conversation, then model callbacks.

While `BANDAGE` exists, each message that asks for an answer creates the next `NN.md`. Create `$DIR` when it is absent.
