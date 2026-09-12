# Phase 2 — Minimal Echo Bot

**Goal:** prove the whole loop works end to end — Telegram → your process → a reply — before any
parsing or database logic exists. By the end, sending the bot a message gets you the same text
echoed back, driven by real Python code you wrote and understand.

**Estimated time:** ~half a day

---

## Tasks

Complete every box before moving to Phase 3.

- [x] Add **`python-telegram-bot`** as a project dependency (`uv add python-telegram-bot`).
- [x] Write `src/bot.py`: build an `Application` with your bot token, register a `MessageHandler`
      that replies with the same text it received, and start it with `run_polling()`.
- [x] Run it (`uv run python src/bot.py`), send the bot a message from the Telegram app, and
      confirm you get your own text echoed back.
- [x] Be able to explain, in your own words, what `Application`, `MessageHandler`, and
      `run_polling()` are each responsible for — this shape is what every later handler
      (Phase 4's db write, Phase 6's commands) hangs off of.
- [x] Confirm `.env` (with `BOT_TOKEN`) is loaded at runtime without the token appearing in
      `src/bot.py` itself.

**Done when:** `uv run python src/bot.py` starts a live bot, a message sent from Telegram is
echoed back verbatim, and you can explain the handler/dispatcher shape unprompted.

---

## What each task did

**`python-telegram-bot`** exists so you don't hand-roll the `getUpdates` HTTP loop, JSON parsing,
and retry/backoff logic yourself — none of that teaches you anything Phase 1's raw `curl` call
didn't already. What the library *does* teach is the handler/dispatcher pattern: an `Application`
owns the polling loop, and you register handlers that get called with an `Update` object whenever
one matches (a `MessageHandler` for plain text, later a `CommandHandler` for `/list` etc. in
Phase 6). This is the same "framework calls your function" shape you'll see in most bot/webhook
libraries, not something specific to Telegram.

The **echo** behavior is deliberately the simplest possible handler — `update.message.reply_text(update.message.text)` — because the point of this phase isn't the behavior, it's confirming
the plumbing: token → `Application` → polling → handler → reply, all working together, so that
when Phase 4 swaps the echo for a database insert, you're changing one line inside a handler
you've already seen work, not debugging the plumbing and the new logic at the same time.

Loading the token from **`.env`** rather than hardcoding it keeps the separation Phase 1 already
set up (token never in code or a commit) intact now that the token is actually being used.
