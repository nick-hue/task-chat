# task-chat — Progress

> Live status panel. Claude keeps this in sync; it always shows **only the current phase**.
> Open beside your code in your editor's live-preview pane (e.g. VS Code `Ctrl+Shift+V`).

---

## 📍 Current phase: **Phase 6 — Command set**

**Goal:** four slash commands, one at a time, each tested from Telegram before the next.

| # | Task | Status |
|---|------|--------|
| 1 | `/list` with tags | ✅ Done |
| 2 | `/list @folder` and `/list #tag` | ✅ Done |
| 3 | `/done <id>` | ✅ Done |
| 4 | `/delete <id>` | ✅ Done |
| 5 | `/folders` | ✅ Done |
| 6 | Bad-input handling | ✅ Done |

**Done when:** all four commands work from Telegram, a wrong or missing argument gets a useful
reply instead of a traceback, and `/delete` leaves no orphaned rows in `task_tags`.

---

_Legend: ✅ Done · 🔧 Needs fix · ⬜ To do_
