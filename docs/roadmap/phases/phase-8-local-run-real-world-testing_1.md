# Phase 8 — Local run, real-world testing

**Goal:** use the bot instead of building it. For a few days it runs from your dev machine and you
file real tasks into it. The output of this phase is not code, it is a list of what annoys you.

**Estimated time:** a few days, elapsed rather than spent

---

## Tasks

- [ ] Clear the leftover test rows so what is in `tasks.db` is real.
- [ ] Run the bot daily from your machine and file actual tasks, not `test`.
- [ ] Use every command in anger: `/list`, the `@folder` and `#tag` filters, `/done`, `/rm`,
      `/folders`.
- [ ] Keep a friction list at `docs/FRICTION.md`, one line per annoyance.
- [ ] Leave it running overnight at least once and check the terminal in the morning.
- [ ] Sort the friction list: blocks daily use, or Phase 10 backlog.

**Done when:** you have used the bot for real for several days and the friction list has entries you
did not have to invent.

---

## What each task did

**The friction list is the deliverable.** Building for three phases straight gives you a mental
model of what the bot does, and using it gives you a model of what it is like to use. Those differ.
The things that will annoy you are not the things you spent time on.

**Fix almost nothing mid-phase.** Only what blocks daily use. Every other item waits for Phase 10.
A bug you fix on day one is a bug you never find out whether you cared about, and this phase's whole
value is that the list is filtered by real use rather than by what you noticed while writing the
code.

**Clear the test rows first.** `buy milk` and `old finished thing` came from testing `/done` and the
`LEFT JOIN`. Leaving them means `/list` always has noise in it and you never see what the bot looks
like with only your real tasks in it.

**Overnight tells you about the polling loop.** An exception inside a handler does not kill
`run_polling()`, `python-telegram-bot` catches it, logs it, and carries on. That is good for uptime
and bad for discovery: a command that breaks on one weird input keeps working afterwards, and the
only trace is a traceback in a terminal you were not watching. Reading the morning scrollback is
how you find those. `Application.add_error_handler` is the tool for routing them somewhere better,
and Phase 9 is where that starts to matter, since a service on the home server has no terminal at
all.

**`logging.basicConfig(level=logging.INFO)` will get loud.** PTB logs its polling on the root
logger, so days of uptime means thousands of lines. When it stops being useful, drop the root to
`WARNING` and raise your own logger to `INFO`. That is a friction item too, write it down rather
than fixing it the moment it irritates you.

**Known quirk to watch for.** Handlers see edited messages as well as new ones by default, and on
an edited-message update `update.message` is `None` while `update.effective_message` holds the
message. Every handler here reads `update.message`, so editing a task gets you silence in Telegram
and an `AttributeError` in the log. No row is written and no reply is sent.
Fixed during this phase by splitting the filter constants: `ONLY_ME` holds the identity check and
is the only one ever negated, while `MINE = ONLY_ME & filters.UpdateType.MESSAGE` guards the six
handlers. Edits from you now match nothing at all, so editing a task is silently ignored.

Making an edit actually rewrite the task is a Phase 10 feature, not a fix. It needs a `message_id`
column on `tasks` to find the row, which means an `ALTER TABLE`, since `init_db` uses
`CREATE TABLE IF NOT EXISTS` and will not add a column to a table that already exists.
