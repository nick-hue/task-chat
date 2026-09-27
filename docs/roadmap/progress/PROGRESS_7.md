# task-chat — Progress

> Live status panel. Claude keeps this in sync; it always shows **only the current phase**.
> Open beside your code in your editor's live-preview pane (e.g. VS Code `Ctrl+Shift+V`).

---

## 📍 Current phase: **Phase 7 — Access control**

**Goal:** the bot answers you and nobody else, before Phase 8 leaves it running unattended.

| # | Task | Status |
|---|------|--------|
| 1 | Find your numeric user id | ✅ Done |
| 2 | `ALLOWED_USER_ID` in `.env` | ✅ Done |
| 3 | Load + validate at startup | ✅ Done |
| 4 | Enforce: filter or per-handler check | ✅ Done |
| 5 | Decide unauthorized response | ✅ Done |
| 6 | Test with a wrong id | ✅ Done |

**Done when:** a message from any id other than yours produces no task row, and the bot still works
normally for you.

---

_Legend: ✅ Done · 🔧 Needs fix · ⬜ To do_
