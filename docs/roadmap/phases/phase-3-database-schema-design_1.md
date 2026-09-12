# Phase 3 — Database schema design

**Goal:** decide what a task row holds, and write the decision down. No code this phase. No
`sqlite3` import, no `tasks.db`, no `CREATE TABLE` executed. The output is a document.

**Estimated time:** ~1 hour

---

## Tasks

Complete every box before moving to Phase 4.

- [x] Write the `tasks` table's columns down: name, SQLite type, nullable or not, default.
      Minimum set is `id`, `chat_id`, `content`, `folder`, `done`, `created_at`.
- [x] Decide how tags are stored. Two candidates: a comma-separated `tags` column on `tasks`, or a
      separate `tags` table plus a `task_tags` join table. Write down which you picked and the
      tradeoff you accepted.
- [x] Decide the type and constraints for `done`, and whether `folder` can be null or defaults to
      an inbox value.
- [x] Put the result in `docs/SCHEMA.md` as a table plus the `CREATE TABLE` statement you intend
      to run in Phase 4.

**Done when:** `docs/SCHEMA.md` exists, names every column with its type and nullability, states
the tags decision with its tradeoff, and contains the `CREATE TABLE` you'll execute in Phase 4.

---

## What each task did

**Designing on paper first** is the point of the phase existing at all. Schema mistakes are the
expensive kind: once rows exist, changing a column means a migration, and SQLite's `ALTER TABLE`
is famously limited (it can add a column, it cannot drop or retype one without rebuilding the
table). An hour spent here is cheaper than the rebuild.

**The tags decision** is the real content of this phase, and it's a normalization question dressed
in a small example. The comma-separated column is one table and trivial inserts, but
"show me everything tagged #urgent" becomes a `LIKE '%urgent%'` that also matches `#urgently` and
can't use an index. The join table is two extra tables and a multi-row insert per task, but the
query is an exact-match join that indexes cleanly. Neither is wrong at this size. What matters is
that you can say which cost you chose.

**Column types** matter differently in SQLite than elsewhere, because SQLite is dynamically typed:
a column declared `INTEGER` will happily store the string `'yes'`. The declared type is a
preference, not a guarantee. That is why constraints (`NOT NULL`, `CHECK (done IN (0,1))`,
`DEFAULT`) carry the weight that types carry in Postgres. Designing with that in mind now saves
you from trusting a type that isn't enforcing anything.

**`chat_id` is in the minimum set** even though this is a single-user bot, because it costs one
column now and is the difference between "works for me" and "works if I ever add a second chat".
Phase 7's access control reads the same id from `update.effective_user.id`.
