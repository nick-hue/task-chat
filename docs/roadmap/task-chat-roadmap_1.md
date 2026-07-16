# Roadmap: task-chat — a personal task list you talk to over Telegram

A hands-on path to learn bot API integration and lightweight database management by building a
Telegram bot that turns chat messages into rows in a database. Deliberately small in scope — the
point isn't to ship a product, it's to feel every layer (bot auth, message handling, schema design,
parsing, access control, deployment) yourself, once, end to end.

> **How to read each phase.** Every phase below has a goal, the concrete tasks, and a **"Repo after
> this phase"** tree plus a **"Tools introduced this phase"** block — what's new, why it's there,
> and what to look up to implement it. Detailed step-by-step checklists (with explanations of *why*
> each task matters) live in `docs/roadmap/phases/phase-<N>-*.md`, added one at a time as the
> project reaches that phase — this document is the full map, not the turn-by-turn directions.

This expands the original 10-step outline in `docs/roadmap.md` into the same phase structure
used for `CLAUDE.md` and `docs/roadmap/progress/`. The original file is kept as-is as the seed doc;
this is the authoritative, living version.

---

## The Project: "task-chat" — a Telegram bot backed by a database

You message a bot; the message becomes a task row. `@folder` and `#tag` tokens in the message
route/label it. Commands read the list back, mark things done, or delete them. Single user
(you), single small database, running first on your dev machine and eventually on your home server.

### Architecture

```
   You (Telegram client)
          │ message
          ▼
   Telegram Bot API (Telegram's servers)
          │ getUpdates (long polling)
          ▼
   ┌───────────────────┐
   │   src/bot.py       │  python-telegram-bot — message/command handlers
   └─────────┬─────────┘
             │
             ▼
   ┌───────────────────┐
   │   src/parser.py    │  pure function: text → {content, folder, tags}
   └─────────┬─────────┘
             │
             ▼
   ┌───────────────────┐
   │   src/db.py        │  sqlite3 — tasks.db
   └───────────────────┘
```

**Stack decisions (made up front so later phases don't relitigate them):** Python, the
[`python-telegram-bot`](https://docs.python-telegram-bot.org/) library, and **SQLite** (stdlib
`sqlite3`, single file `tasks.db`) — plenty for a single-user bot, trivial to back up or move when
you deploy it. **Long polling**, not webhooks — a home server usually has no public HTTPS endpoint
sitting in front of it, and polling avoids needing one. Phase 1 still has you read up on *why*
this trade-off exists rather than taking it on faith.

---

## Phase 1 — Bot registration & API basics (~1–2 hours)

**Principle:** *Understand what you're driving before you build on it.*

- Register a bot with `@BotFather`, get a token.
- Read enough of the Telegram Bot API docs to know what an `Update` and a `Message` object look
  like, and what fields you'll actually need (`chat.id`, `message.text`, `from.id`).
- Understand the **polling vs. webhook** trade-off well enough to explain it back, and know why
  this project uses polling.

### Repo after this phase

```
task-chat/
├── docs/
│   ├── roadmap/               (already exists)
│   ├── roadmap.md             (already exists — original seed doc)
│   └── TEACHING_RECAP.md      (already exists)
├── pyproject.toml              (already exists — bare uv scaffold)
├── .python-version             (already exists)
├── src/main.py                 (already exists — default stub)
└── .env                       ← new  (BOT_TOKEN=..., gitignored — created once you have a token)
```

### Tools introduced this phase

- **Telegram Bot API** — the HTTP API Telegram exposes for bots; everything else in this project
  is a client of it. *Why now:* you can't design around an API you haven't read. *Look up:* the
  official Bot API docs' "Getting updates" and "Authorizing your bot" pages.
- **@BotFather** — the meta-bot used to register new bots and get a token. *Look up:* `/newbot` in
  a chat with @BotFather.

---

## Phase 2 — Minimal echo bot (~half a day)

**Principle:** *Prove the loop works before adding complexity.*

- Set up the Python project (`uv init`, a virtualenv, `.gitignore` covering `.venv/`, `.env`,
  `*.db`).
- Add `python-telegram-bot` as a dependency.
- Write a `src/bot.py` that starts polling and replies to any message with the same text back.
- Confirm it runs, and that you understand the message-handler/dispatcher shape — this is the
  skeleton every later handler hangs off.

### Repo after this phase

```
task-chat/
├── src/
│   ├── main.py
│   └── bot.py                ← new  (polling loop + one echo handler)
├── .env                       (BOT_TOKEN=...)
├── .gitignore                  (already exists)
├── pyproject.toml              (already exists, dependency added)
└── docs/
```

### Tools introduced this phase

- **uv** — Python package/env manager. *Why now:* one-command reproducible environment, same
  reason it was used in Forge. *Look up:* `uv init`, `uv add python-telegram-bot`.
- **python-telegram-bot** — the Python wrapper around the Bot API (handlers, polling loop, update
  dispatch). *Why now:* hand-rolling `getUpdates` HTTP calls teaches you nothing extra; this is
  the standard, well-documented choice. *Look up:* the library's "Quickstart" — `Application`,
  `MessageHandler`, `run_polling()`.
- **python-dotenv** (optional) — loads `.env` into environment variables. *Why now:* keeps the bot
  token out of source. *Look up:* `load_dotenv()`.

---

## Phase 3 — Database schema design (~1 hour, paper only)

**Principle:** *Design before you code.* This phase produces no code — only a decision written
down, e.g. in `docs/roadmap/phases/phase-3-*.md` or a short `SCHEMA.md`.

- Decide the `tasks` table's columns: at minimum `id`, `chat_id`, `content`, `folder`, `done`,
  `created_at`.
- Decide how tags are stored — a comma-separated column on `tasks` vs. a separate `tags` table
  plus a `task_tags` join table — and write down the tradeoff (simplicity vs. queryability: "show
  me all tasks tagged #urgent" is a `LIKE` hack in the first design, a clean join in the second).
- Decide the type/constraints for `done` (`INTEGER` 0/1 is the natural SQLite choice) and whether
  `folder` can be null (an "inbox" default).

### Tools introduced this phase

- **SQLite** — no server process, one file (`tasks.db`), enough for a single-user bot. *Why now:*
  this phase is where you commit to it and design around its type system (SQLite is dynamically
  typed — worth knowing before you design columns). *Look up:* SQLite's data types page, and
  "normalization" if the tags decision is unfamiliar.

---

## Phase 4 — Wire the database to the bot (~half a day)

**Principle:** *Replace the echo with a real write, one path at a time.*

- Write `src/db.py`: connect to `tasks.db`, create the `tasks` table (and `tags`/`task_tags` if you
  went that route) if it doesn't exist, and add `insert_task()` / `list_tasks()` functions.
- Change the bot's message handler to insert a row instead of echoing.
- Confirm end-to-end: send a message, then inspect `tasks.db` (e.g. with the `sqlite3` CLI) and
  see the row.

### Repo after this phase

```
task-chat/
├── src/
│   ├── main.py
│   ├── bot.py
│   └── db.py                 ← new
├── tasks.db                   (gitignored, created at runtime)
└── ...
```

---

## Phase 5 — Parsing logic (~half a day)

**Principle:** *Keep parsing isolated so it's testable on its own, independent of Telegram or the
database.*

- Write `src/parser.py`: a pure function `parse(text) -> {content, folder, tags}` that pulls a leading
  `@folder` and any `#tag` tokens out of the message text, leaving the rest as `content`.
- Test it directly (a quick script or `pytest`) with a handful of example messages *before* wiring
  it into `src/bot.py` — this phase is exactly why it was kept separate from `src/db.py` in Phase 4.
- Wire it in: the handler calls `parse()`, then passes the result to `insert_task()`.

---

## Phase 6 — Command set (~1–2 days)

**Principle:** *Add one command at a time, testing each before the next.*

- `/list` — show open tasks (optionally filtered by folder).
- `/done <id>` — mark a task complete.
- `/delete <id>` — remove a task.
- `/folders` — list distinct folders in use.
- Each is a small `CommandHandler` calling a matching `src/db.py` function — resist the urge to build
  all four before testing the first.

---

## Phase 7 — Access control (~1 hour)

**Principle:** *Close the door before you forget it's open.*

- Store your own Telegram numeric user ID (from `from.id` on any message you send it) as
  `ALLOWED_USER_ID` in `.env`.
- Every handler checks `update.effective_user.id == ALLOWED_USER_ID` and silently ignores (or
  replies "not authorized") otherwise — do this before Phase 8's real-world testing, since that's
  the point where the bot is running unattended for days.

---

## Phase 8 — Local run, real-world testing (~a few days, elapsed)

**Principle:** *Use it before you deploy it.*

- Run the bot from your dev machine and actually use it day to day — add real tasks, mark things
  done, hit whatever commands you built.
- Keep a short friction list (missing command, annoying parsing edge case, etc.) — this is your
  backlog for Phase 10, not stuff to fix mid-flight unless it blocks daily use.

---

## Phase 9 — Deployment (~half a day)

**Principle:** *Deployment means it survives without you watching it.*

- Move the code (and a fresh or copied `tasks.db`) to your home server.
- Make it persistent: a **systemd** user/system service with `Restart=on-failure` and enabled at
  boot, so it survives both crashes and reboots — this is the actual "deployment" learning goal,
  distinct from just running `python src/bot.py` in a terminal and leaving it.
- Confirm: reboot the server (or kill the process) and see it come back on its own.

### Tools introduced this phase

- **systemd** — Linux's init/service manager; used here for `Restart=` and boot-time start, not
  containers/orchestration (that's Forge's territory, not this project's). *Look up:* writing a
  unit file, `systemctl enable --now`.

---

## Phase 10 — Iterate (open-ended)

**Principle:** *Only layer on extras once the core loop is solid and deployed.*

- Work from the Phase 8 friction list and whatever else comes up in real use: due dates, a daily
  digest message, editing a task's folder/tags, etc.
- Ping for a sanity check at the end of any phase, or whenever stuck on something specific — this
  applies throughout, not just here.
