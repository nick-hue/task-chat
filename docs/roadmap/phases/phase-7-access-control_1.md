# Phase 7 — Access control

**Goal:** the bot answers you and nobody else. Right now its username is public and anyone who
finds it can file tasks into your database. Phase 8 leaves it running unattended for days, so the
door closes first.

**Estimated time:** ~1 hour

---

## Tasks

- [ ] Find your own numeric Telegram user id.
- [ ] Put it in `.env` as `ALLOWED_USER_ID`, and confirm `.env` is still gitignored.
- [ ] Load it in `bot.py` and fail at startup if it is missing or not a number.
- [ ] Decide how to enforce it: a check inside every handler, or one filter at registration.
- [ ] Decide what an unauthorized user gets: silence, or a short "not authorized" reply.
- [ ] Test it. Confirm an unauthorized id gets your chosen behaviour and writes no rows.

**Done when:** a message from any id other than yours produces no task row, and the bot still works
normally for you.

---

## What each task did

**Finding your id costs one message.** Every `update` carries `update.effective_user.id`. Print it
from the existing `handler`, send the bot anything, read it off your terminal, delete the print.
There are bots that will tell you the number, but you already have the plumbing.

**`ALLOWED_USER_ID` is config, not code.** Same reason `BOT_TOKEN` is in `.env`: the value is
specific to your machine and your account, and hardcoding it means the repo carries a fact about
you. It is also the second thing that has to be present for the bot to work at all, which is why
validating it at startup beats discovering it is `None` inside a handler an hour later.

**`int()` on the way in, not at every comparison.** `os.environ.get` hands you a string.
`update.effective_user.id` is an int. `"12345" == 12345` is `False` in Python, silently, and a
guard that is always false locks you out of your own bot. Convert once, near `load_dotenv()`.

**Two ways to enforce it, and they teach different things.**

An `if` at the top of each handler is explicit and obvious, and you write it seven times. Miss one
handler and that command stays open, which is exactly the failure mode you get when the guard is
copy-pasted.

`python-telegram-bot` ships `filters.User(user_id=...)`, which composes with the filters you
already use: `filters.TEXT & ~filters.COMMAND & filters.User(...)`. The dispatcher then never calls
the handler at all. One expression per registration, and a `CommandHandler` takes the same
`filters=` argument. The tradeoff is that a filtered-out update falls through to whatever handler
matches next, so the order of `add_handler` calls starts to matter. Recommendation: use the filter,
and keep one unfiltered catch-all last for the unauthorized case.

**Silence versus a reply is a real decision.** Silence gives a stranger no confirmation the bot is
live. A reply is friendlier and tells you, in the logs, that someone found it. Either is defensible
for a single-user bot; pick one and know why.

**`chat_id` is not `user_id`.** Your `db.py` keys every row on `chat_id`, which in a private chat
happens to equal your user id. They diverge the moment the bot is added to a group. The guard
belongs on the user id, since that is the identity being authorized, and leaving `chat_id` as the
storage key is fine. Worth knowing the two are different things that currently look the same.
