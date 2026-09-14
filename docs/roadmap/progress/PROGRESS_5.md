# task-chat — Progress

> Live status panel. Claude keeps this in sync; it always shows **only the current phase**.
> Open beside your code in your editor's live-preview pane (e.g. VS Code `Ctrl+Shift+V`).

---

## 📍 Current phase: **Phase 5 — Parsing logic**

**Goal:** pull `@folder` and `#tag` out of message text with a pure, testable function.

| # | Task | Status |
|---|------|--------|
| 1 | Edge-case rules written down | ✅ Done |
| 2 | `parse()` in `src/parser.py` | ✅ Done |
| 3 | Tested without bot or database | ✅ Done |
| 4 | `insert_task()` takes folder + tags | ✅ Done |
| 5 | Handler calls `parse()` | ✅ Done |
| 6 | Tagged message lands end to end | ✅ Done |

**Done when:** a tagged message from Telegram produces one `tasks` row with the right folder, one
`tags` row per distinct tag, and matching `task_tags` rows. `parser.py` imports neither `telegram`
nor `sqlite3`.

---

_Legend: ✅ Done · 🔧 Needs fix · ⬜ To do_
