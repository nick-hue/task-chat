# Phase 4 — Wire the database to the bot

**Goal:** replace the echo with a real write. By the end, a message sent to the bot is a row in
`tasks.db` that you can see with the `sqlite3` CLI, and `src/bot.py` no longer knows any SQL.

**Estimated time:** ~half a day

---

## Tasks

Complete every box before moving to Phase 5.

- [x] Write `src/db.py` with a `connect()` that opens `tasks.db` and turns foreign keys on.
- [x] Add `init_db()` that runs the DDL from `docs/SCHEMA.md`, safe to call on every start.
- [x] Add `insert_task(chat_id, content)` returning the new row's id.
- [x] Add `list_tasks(chat_id)` returning the undone rows for that chat.
- [x] Change the handler in `src/bot.py` to call `insert_task` instead of echoing, and reply with
      a confirmation.
- [x] Send a message, then open `tasks.db` with the `sqlite3` CLI and see the row.
- [x] Confirm `tasks.db` is gitignored and not staged.

**Done when:** a message sent from Telegram becomes a row in `tasks.db`, the bot confirms it, and
`src/bot.py` contains no SQL.

---

## What each task did

**`db.py` exists as a separate file** so that `bot.py` never holds a SQL string. That split is the
same one Phase 5 makes for parsing, and the reason is the same: each file should be testable
without starting the other two. You can `python -c "import db; db.insert_task(1, 'x')"` without a
Telegram token anywhere in sight.

**`init_db()` runs the DDL every start** rather than once by hand, using `CREATE TABLE IF NOT
EXISTS`. A fresh clone of the repo has no `tasks.db`, because it's gitignored, so the schema has to
be able to recreate itself. This is the cheapest possible version of a migration system, and it
works right up until you need to change a column.

**Parameterized queries** are the one non-negotiable in this phase. Every value goes in as a `?`
placeholder with a tuple of arguments, never an f-string. Task content comes from a chat message,
which is untrusted input by definition, and string-formatting it into SQL is how injection happens.
`sqlite3` also rejects multiple statements in one `execute()`, which blunts the classic attack, but
the habit is what matters: `?` always, no exceptions.

**Commits are explicit.** Python's `sqlite3` opens a transaction implicitly on the first write and
holds it until you call `commit()`. Forget it and the row exists in your process, vanishes on exit,
and you spend twenty minutes wondering why `SELECT` from the CLI returns nothing.

**The handler returns a confirmation** rather than staying silent, because a bot that swallows your
message without a word is indistinguishable from a bot that crashed. Echoing the row id back also
gives Phase 6's `/done <id>` something to refer to.
