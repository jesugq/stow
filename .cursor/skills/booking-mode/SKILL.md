---
name: booking-mode
description: /booking-mode new, load, or next. Simple conversations in Simplified Technical English.
disable-model-invocation: true
---

# Booking mode

Call the Skill tool with `markdown-mode` for the folder, the ack, and the markdown file.

```
verb: new | load | next
root: ~/.cursor/booking-mode
sentinel: BOOKING
drop: -
load: NN
need: -
mark: BOOKING
then:
sect: file
```

`new`, `load`, and `next` are accepted. `new` creates the dated folder. `load` opens an existing booking folder. `next` follows a zero-byte `BOOKING` sentinel.

While `BOOKING` exists, the prose of each answer follows the STE definition below. Do not write the output-style frontmatter into the answer file. That frontmatter is `name: STE` and `keep-coding-instructions: true` on the Claude style file. It is not part of the answer.

Write prose in STE-flavored Simplified Technical English. Follow the structural rules of ASD-STE100. This file omits its approved dictionary. Treat word choice as a direction, not a verifiable rule.

## Scope

These rules govern all prose, including commit messages, code comments, and documentation.

They do not govern code, identifiers, paths, commands, or configuration. Never rename an identifier to satisfy them. Quote a file, a tool result, an error, or the user exactly. Drop them when the user asks for another voice.

## The three rules that fail most often

Check each sentence against these three before you write the next one. Scan the finished draft for all three before you send it.

**1. Name the actor.** Look for a form of `be` or `get` before a past participle. Name who acts, or rewrite. A state description is fine: nothing acts in "the file is corrupted".

- Wrong: "Code blocks are stripped." Right: "The script strips code blocks."

**2. One idea per sentence.** Look for `, and`, `, but`, or `, so` joining two clauses. Split the sentence. `, so` leaks most often.

- Wrong: "It spreads load, so no machine saturates." Right: "It spreads load. No machine saturates."

**3. Repeat the verb.** Never replace a verb you already used with `did`, `does`, or `is`.

- Wrong: "Topic changed at the same moment the style did." Right: "...the style changed."

## Sentence mechanics

- Cap an instruction at 20 words. Cap a description at 25.
- Use no semicolons. Write two sentences.
- Stack 3 nouns at most. Write "the handler for the retry backoff policy", not "request retry backoff policy handler".
- Use simple tenses. Keep a compound tense that carries information: "the build has finished" states current relevance.
- Put one topic in one paragraph. Cap it at 6 sentences.
- Use a numbered list for 3 or more steps. Use a bulleted list for 3 or more parallel items.

## Word choice

- Use one name for one thing. Do not rotate synonyms.
- Prefer the plain verb. Write "start", not "spin up". Write "read", not "dive into".
- Prefer the verb to its noun form. Write "analyze the log", not "perform an analysis of the log".
- Delete marketing adjectives: seamless, robust, powerful, blazing-fast, cutting-edge, effortless. Give the measurement that earns the claim, or write nothing.
- Delete stacked hedges. One hedge at true strength carries information. Three carry none.

## Brevity

Cut what carries no information. Delete a section before compressing every sentence in it.

- Preamble, self-narration, the closing offer.
- A point you already made in this response.
- Filler openers: "I will now", "let me", "it is worth noting that".
- Any adjective that states no measurement.

## Precision outranks brevity

- Keep every hedge at its original strength. "The test may have failed" is not "the test failed".
- Keep every condition, exception, number, and scope qualifier.
- Add no fact you have not verified. A sentence that reads better because it supplies a cause has stopped being true.
- Stop when the sentence is unambiguous, not when it is shortest.

Say what you kept and why.

## Response shape

Put the answer in the first sentence. Put the reasoning after it. Report what you did and what happened.
