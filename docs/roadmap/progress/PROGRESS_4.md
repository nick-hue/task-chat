# task-chat — Progress

> Live status panel. Claude keeps this in sync; it always shows **only the current phase**.
> Open beside your code in your editor's live-preview pane (e.g. VS Code `Ctrl+Shift+V`).

---

## 📍 Current phase: **Phase 4 — Wire the database to the bot**

**Goal:** replace the echo with a real write. A message becomes a row in `tasks.db`.

| # | Task | Status |
|---|------|--------|
| 1 | `connect()` in `src/db.py` | ✅ Done |
| 2 | `init_db()` runs the DDL | ✅ Done |
| 3 | `insert_task()` | ✅ Done |
| 4 | `list_tasks()` | ✅ Done |
| 5 | Handler inserts, not echoes | ✅ Done |
| 6 | Row visible in `sqlite3` CLI | ✅ Done |
| 7 | `tasks.db` gitignored | ⬜ To do |

**Done when:** a message from Telegram becomes a row in `tasks.db`, the bot confirms it, and
`src/bot.py` contains no SQL.

---

_Legend: ✅ Done · 🔧 Needs fix · ⬜ To do_
