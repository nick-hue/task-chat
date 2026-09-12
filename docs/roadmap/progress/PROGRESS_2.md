# task-chat — Progress

> Live status panel. Claude keeps this in sync; it always shows **only the current phase**.
> Open beside your code in your editor's live-preview pane (e.g. VS Code `Ctrl+Shift+V`).

---

## 📍 Current phase: **Phase 2 — Minimal Echo Bot**

**Goal:** prove the whole loop works end to end — Telegram → your process → a reply — before any
parsing or database logic exists.

| # | Task | Status |
|---|------|--------|
| 1 | Add `python-telegram-bot` as a dependency | ✅ Done |
| 2 | Write `src/bot.py`: `Application` + `MessageHandler` + `run_polling()` | ✅ Done |
| 3 | Run it, send a message, confirm it's echoed back | ✅ Done |
| 4 | Explain `Application` / `MessageHandler` / `run_polling()` unprompted | ✅ Done |
| 5 | Confirm `.env`/`BOT_TOKEN` loads at runtime, not hardcoded in `src/bot.py` | ✅ Done |

**Done when:** `uv run python src/bot.py` starts a live bot, a message sent from Telegram is
echoed back verbatim, and you can explain the handler/dispatcher shape unprompted.

---

_Legend: ✅ Done · 🔧 Needs fix · ⬜ To do_
