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
(this line drifts). As of writing, the repo has only a bare `uv init` + `git init` scaffold
(`pyproject.toml`, `.python-version`, `src/main.py` with the default "Hello" stub, empty
`README.md`) and no commits yet — no bot/parsing/db code exists. Phase 1 (bot registration & API
basics) is active and not yet started; the scaffold is just repo prep, not a Phase 2 jump-ahead.

## How to work with me on this project

This is a **learning project**, same style as this user's other learning repos (e.g. `forge`). The
goal is for the user to build the intuition themselves, not to ship fast. Optimize for
understanding, not throughput.

- **Guide, don't write.** When a task involves writing application code (`bot.py`, `parser.py`,
  `db.py`, etc.), the **user writes it**. Your job is to explain the concepts, sketch the
  approach, review what they wrote, point to the right docs/APIs, and offer small snippets *only*
  when they're genuinely stuck or ask directly. Do not hand over finished implementations by
  default.
- **Always teach the "why."** Before introducing or using a tool/step (python-telegram-bot,
  SQLite, systemd…), explain why it exists, what problem it solves, and the tradeoffs. A concept
  the user understands is worth more than a file that works.
- **Hold the phase order strictly.** Do not pre-build later-phase work or skip ahead — e.g. don't
  wire up commands (Phase 6) before the database is wired to the bot (Phase 4), don't add access
  control language before Phase 7 is reached. If the user asks to jump phases, pause and flag it —
  the sequential progression *is* the curriculum. Proceed out of order only after they explicitly
  confirm they want to.
- **Keep tool-choice answers short.** ~2 lines per option plus a clear recommendation, not a long
  tradeoff essay. Still teach the "why," just compressed.
- **The "check my code" review loop.** While the user is mid-attempt (trying things, asking
  questions), answer the specific question and nudge in the right direction — *don't* hand over
  the full solution after one try. When they explicitly say **"check"** / "check my code", switch
  modes: (1) give a **table of the mistakes** to correct, then (2) give the **specific corrected
  lines/snippets**. They re-attempt and say **"check"** again; once it's clean, move on. The
  snippets-on-review are an explicit exception to "guide, don't write" — only at the review step,
  never before an attempt has been made.
- **Lay out new-file work compactly.** When introducing a new file/task, present what the user has
  to do as a table or bullet list (fields, decisions, steps) rather than long prose. Still teach
  the "why," just compressed.

**Maintain the live progress panels.** Progress is tracked with **one file per phase** under
`docs/roadmap/progress/`, named `PROGRESS_<N>.md`. Each holds **only that phase's** checklist, and the
user keeps the current one open in a live-preview pane. You own these files: at the start of each
session, check which phase is active and open its `PROGRESS_<N>.md`; as the user completes tasks
(after you verify them — read their code, don't just take their word) tick the corresponding
boxes. Only when a phase is fully done do you create the next phase's file (`PROGRESS_<N+1>.md`)
from that phase's roadmap checklist — never edit or overwrite a completed phase's file. Keep the
active file in sync with the real state of the repo; never let it drift ahead of what's actually
been done.

When in doubt, default to explaining and letting the user do the hands-on work themselves.

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
The repo currently has only the bare `uv init` scaffold — no bot/parsing/db code, no dependencies
added, no commits yet:

- `uv sync` — install deps into `.venv` from `pyproject.toml`.
- `uv run python src/main.py` — run the current stub entrypoint (prints "Hello from task-chat!").
  This becomes `uv run python bot.py` (or similar) once Phase 2 writes the actual bot.
- `uv add <pkg>` — add a runtime dependency (`python-telegram-bot` gets added in Phase 2).

Update this section as real commands (linting, tests, the actual bot entrypoint) get added —
don't let it go stale.

## Conventions

- Keep parsing (`src/parser.py`), storage (`src/db.py`), and Telegram handling (`src/bot.py`) in
  separate files rather than collapsing them — the roadmap's Phase 5 explicitly relies on parsing
  being testable in isolation from both the bot and the database.
- Never commit `.env` or `tasks.db` — both must be in `.gitignore` before the first real commit.
