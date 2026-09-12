# task-chat — Progress

> Live status panel. Claude keeps this in sync; it always shows **only the current phase**.
> Open beside your code in your editor's live-preview pane (e.g. VS Code `Ctrl+Shift+V`).

---

## 📍 Current phase: **Phase 3 — Database Schema Design**

**Goal:** decide what a task row holds and write it down. Paper only, no code.

| # | Task | Status |
|---|------|--------|
| 1 | Column table | ✅ Done |
| 2 | Tag storage decision | ✅ Done |
| 3 | `done` + `folder` constraints | ✅ Done |
| 4 | DDL in `docs/SCHEMA.md` | ✅ Done |

**Done when:** `docs/SCHEMA.md` exists, names every column with its type and nullability, states
the tags decision with its tradeoff, and contains the `CREATE TABLE` you'll execute in Phase 4.

---

_Legend: ✅ Done · 🔧 Needs fix · ⬜ To do_
