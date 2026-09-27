# task-chat — Progress

> Live status panel. Claude keeps this in sync; it always shows **only the current phase**.
> Open beside your code in your editor's live-preview pane (e.g. VS Code `Ctrl+Shift+V`).

---

## 📍 Current phase: **Phase 9 — Deployment**

**Goal:** the bot survives a crash and a reboot on the home server, with nobody watching.

| # | Task | Status |
|---|------|--------|
| 1 | Push, then clone on the server | ⬜ To do |
| 2 | Install `uv`, `uv sync` | ⬜ To do |
| 3 | Create `.env` on the server | ⬜ To do |
| 4 | Copy `tasks.db` or start fresh | ⬜ To do |
| 5 | Manual run, laptop bot stopped | ⬜ To do |
| 6 | Write the systemd unit | ⬜ To do |
| 7 | `enable --now`, read `journalctl` | ⬜ To do |
| 8 | Kill it, then reboot | ⬜ To do |

**Done when:** you reboot the server, do nothing, and the bot answers you.

---

## Still open: Phase 8 — real-world testing

Carried over, and continues after deployment:

| # | Task | Status |
|---|------|--------|
| 2 | Run daily, file real tasks | ⬜ To do |
| 3 | Use every command in anger | ⬜ To do |
| 4 | Keep `docs/FRICTION.md` | ⬜ To do |
| 5 | Leave running overnight once | ⬜ To do |
| 6 | Sort friction: blocker or backlog | ⬜ To do |

---

## In flight: Phase 10 item — edit a message, update the task

Pulled forward ahead of the friction list, by request.

Built as `/edit <id> <new text>` rather than as a message edit. The `message_id` column is
populated but unused, and is what a message-edit path would key on later.

| # | Task | Status |
|---|------|--------|
| 1 | `message_id` column + unique index | ✅ Done |
| 2 | `insert_task` stores it | ✅ Done |
| 3 | `db.edit_task`, `_set_tags` helper | ✅ Done |
| 4 | `/edit` handler | ✅ Done |
| 5 | Try it from Telegram | ⬜ To do |

---

_Legend: ✅ Done · 🔧 Needs fix · ⬜ To do_
