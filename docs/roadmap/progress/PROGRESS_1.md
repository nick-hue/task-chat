# task-chat — Progress

> Live status panel. Claude keeps this in sync; it always shows **only the current phase**.
> Open beside your code in your editor's live-preview pane (e.g. VS Code `Ctrl+Shift+V`).

---

## 📍 Current phase: **Phase 1 — Bot Registration & API Basics**

**Goal:** understand what a Telegram bot actually is (token + updates) before writing any code —
register a bot, and be able to explain the polling-vs-webhook tradeoff unprompted.

| # | Task | Status |
|---|------|--------|
| 1 | Register a bot with **@BotFather**, get a name/username | ⬜ To do |
| 2 | Save the bot **token** somewhere safe (not in code/commits) | ⬜ To do |
| 3 | Read the `Update`/`Message` object docs (`text`, `chat.id`, `from.id`) | ⬜ To do |
| 4 | Read the `getUpdates` (polling) vs `setWebhook` (webhooks) docs | ⬜ To do |
| 5 | Decide + justify: this project uses **polling** | ⬜ To do |
| 6 | Send a test message, confirm it via a raw `getUpdates` `curl` call | ⬜ To do |

**Done when:** working bot token in hand, polling vs. webhooks explained unprompted, and a raw
update seen from your own test message.

---

_Legend: ✅ Done · 🔧 Needs fix · ⬜ To do_
