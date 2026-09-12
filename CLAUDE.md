# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What task-chat is

task-chat is a **Telegram bot backed by a database**, built as a hands-on learning project for bot
API integration and lightweight database management. You message the bot; the message becomes a
task row. Leading `@folder` tokens route it, `#tag` tokens label it. Commands read the list back,
mark tasks done, or delete them. Single user, single small database — no product ambitions here.

**Current state:** the application is built out phase by phase. **The authoritative source of
where things stand is `docs/roadmap/progress/` — read the highest-numbered `PROGRESS_<N>.md` at the
start of every session to learn the active phase**, rather than trusting any state described here
(this line drifts). As of writing, Phases 1 through 3 are done: the bot is registered, `src/bot.py`
runs a live echo bot over long polling, and `docs/SCHEMA.md` holds the agreed three-table schema
with its DDL. No `db.py` or `parser.py` yet. Phase 4 (wire the database to the bot) is active.

## How to work with me on this project

This is a **learning project**, same style as this user's other learning repos (e.g. `forge`). The
goal is for the user to build the intuition themselves, not to ship fast. Optimize for
understanding, not throughput.

**Run the `guided-build` skill for this repo.** Invoke it with the Skill tool at the start of every
session. It holds the working loop this project runs on: guide-don't-write, teach the "why" before
introducing a tool, the "check" review protocol, strict phase order, compact tool-choice answers,
and the rules for the progress panels. It also pulls in `teach` for explanations and `unslop` for
the prose. What follows is only the task-chat-specific part the skill can't know.

- **The user writes `bot.py`, `parser.py`, and `db.py`.** You explain, review, and track.
- **Progress panels live at `docs/roadmap/progress/PROGRESS_<N>.md`,** one per phase, and the user
  keeps the current one open in a live-preview pane. Read the highest-numbered one at the start of
  every session to learn the active phase, and trust it over the "Current state" note above.
- **Don't re-quiz the user on theory or reading checkpoints** (e.g. "read the API docs," "decide
  polling vs. webhook"). Take their word and tick the box. They asked for this directly ("don't be
  so strict about theory, I want to get stuff done"), and it's a standing request, not a one-off.
- **Concrete phase-order traps:** don't wire up commands (Phase 6) before the database is wired to
  the bot (Phase 4), and don't add access-control language before Phase 7 is reached.

## The roadmap is the spec

`docs/roadmap/` is the authoritative source of *what to build and in what order*. **Read it before
adding anything new.**

- `docs/roadmap/task-chat-roadmap_1.md` — the full 10-phase plan, the target architecture diagram,
  the stack decisions (Python, `python-telegram-bot`, SQLite, long polling), and the
  rationale/toolchain for every phase. This is the master document, written up front.
  `docs/roadmap.md` is the original terse seed doc this was expanded from — kept for reference,
  not maintained further.
- `docs/roadmap/phases/phase-<N>-*.md` — detailed task checklist for each phase, **added one at a
  time as the project reaches that phase** (later phases are not pre-written). Present so far:
  `phase-1-bot-registration-api-basics_1.md`.
- `docs/roadmap/progress/PROGRESS_<N>.md` — the live, per-phase status panels you maintain (see
  "Maintain the live progress panels" above).

The phases are deliberately sequential and the *order is pedagogical* — e.g. parsing (Phase 5) is
kept isolated from the database (Phase 4) so it's testable on its own before either touches the
other; access control (Phase 7) comes right before real-world testing (Phase 8) so the bot is never
left open while running unattended. Do not skip ahead unless asked.

### Target architecture

```
You (Telegram client) → Telegram Bot API → src/bot.py (handlers) → src/parser.py (@folder/#tag) → src/db.py (SQLite: tasks.db)
```

Long polling, not webhooks — no public HTTPS endpoint required, which matters once this moves to
the user's home server in Phase 9. See the master roadmap doc for the full rationale.

Intended final layout (grows one phase at a time — see the roadmap for details), following the
existing `src/` layout `uv init` already created: `src/main.py` (entrypoint), `src/bot.py`
(handlers + polling loop), `src/parser.py` (pure text→task parsing), `src/db.py` (SQLite access),
`.env` (bot token, allowed user id — gitignored), `tasks.db` (gitignored, created at runtime).

## Tooling and commands

Stack is decided (**Python**, **uv** for env/deps, **python-telegram-bot**, stdlib **sqlite3**).
`python-telegram-bot` and `python-dotenv` are installed. No linter or test runner yet:

- `uv sync` — install deps into `.venv` from `pyproject.toml`.
- `uv run src/bot.py` — start the bot. Blocks on `run_polling()`, Ctrl-C to stop.
- `uv add <pkg>` — add a runtime dependency.

Update this section as real commands (linting, tests, the actual bot entrypoint) get added —
don't let it go stale.

## Conventions

- Keep parsing (`src/parser.py`), storage (`src/db.py`), and Telegram handling (`src/bot.py`) in
  separate files rather than collapsing them — the roadmap's Phase 5 explicitly relies on parsing
  being testable in isolation from both the bot and the database.
- Never commit `.env` or `tasks.db` — both must be in `.gitignore` before the first real commit.
