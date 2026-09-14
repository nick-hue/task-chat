# Phase 6 — Command set

**Goal:** four slash commands, added one at a time, each tested from Telegram before the next one
is written. By the end the bot is usable: you can file a task, read the list back, tick one off,
and throw one away.

**Estimated time:** ~1-2 days

---

## Tasks

Complete every box before moving to Phase 7. The order matters, `/list` first because every other
command needs you to be able to see what changed.

- [ ] `/list` — a `list_tasks` read, formatted, with tags joined in.
- [ ] `/list @folder` and `/list #tag` — the filtered forms.
- [ ] `/done <id>` — set `done = 1`, with a `db.py` function behind it.
- [ ] `/delete <id>` — remove the row, and confirm the `task_tags` rows go with it.
- [ ] `/folders` — the distinct folders in use, with a count each.
- [ ] Decide and handle the bad-input cases: missing id, non-numeric id, id that does not exist.

**Done when:** all four commands work from Telegram, a wrong or missing argument gets a useful
reply instead of a traceback, and `/delete` leaves no orphaned rows in `task_tags`.

---

## What each task did

**`CommandHandler` is the sibling of the `MessageHandler`** you already registered. Same
dispatcher, different predicate: it matches `/list` rather than plain text. This is why Phase 2's
`filters.TEXT & ~filters.COMMAND` mattered. Without that `~filters.COMMAND`, your message handler
would swallow `/list` and file it as a task.

**Arguments arrive pre-split in `context.args`.** For `/done 3` you get `["3"]`, strings, always.
That is where the `context` parameter you have been ignoring since Phase 2 finally earns its place
in the signature.

**`/list` is first because it is the instrument.** Every other command changes state, and without a
way to read state back you are checking your work in the `sqlite3` CLI for the rest of the phase.

**The join finally pays.** Showing a task with its tags means the three-table `LEFT JOIN` from
Phase 3, and `/list #urgent` means filtering on `tags.tag_name` with an exact match. The
comma-separated design would be a `LIKE` here, and `#urgent` would match `#urgently`.

**`/delete` is where `ON DELETE CASCADE` gets tested for real.** You declared it in Phase 3 and
turned foreign keys on in `connect()`. Deleting a tagged task and finding no leftover `task_tags`
rows is the proof both halves work. If foreign keys were off, the orphans would accumulate
silently and nothing would ever tell you.

**Bad input is the bulk of the work.** `/done`, `/done abc`, and `/done 999` are three different
failures needing three different replies. A command set that only handles the happy path is one
typo away from a traceback in your terminal and silence in the chat.
