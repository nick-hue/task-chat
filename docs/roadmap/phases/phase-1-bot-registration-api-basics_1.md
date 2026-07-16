# Phase 1 — Bot Registration & API Basics

**Goal:** understand what a Telegram bot actually is (a token + an endpoint that receives
"updates") before writing any code. No project files yet beyond a token you're holding onto.

**Estimated time:** ~1–2 hours

---

## Tasks

Complete every box before moving to Phase 2.

- [ ] Open a chat with **@BotFather** on Telegram and run `/newbot` to register a bot; give it a
      name and username.
- [ ] Save the **bot token** BotFather gives you somewhere safe (you'll put it in `.env` in
      Phase 2 — don't paste it into code, a commit, or a chat you'd mind leaking).
- [ ] Read the Telegram Bot API docs section on **`Update`** objects: know what a `Message` looks
      like, and specifically what `message.text`, `message.chat.id`, and `message.from.id` are.
- [ ] Read the docs' description of **`getUpdates`** (long polling) and **`setWebhook`**
      (webhooks). Be able to explain, in your own words, the difference and why you'd pick one
      over the other.
- [ ] Decide — and be able to justify — that this project uses **polling**. (Hint: think about
      what a webhook requires that a home server behind a home router doesn't have by default.)
- [ ] Send your bot a message via the Telegram app and confirm (via the raw `getUpdates` HTTP
      call, e.g. with `curl`) that you can see the update come through — this is the proof the
      token and your account are correctly wired, before any Python is involved.

**Done when:** you have a working bot token, can explain polling vs. webhooks unprompted, and have
seen a raw update from your own test message.

---

## What each task did

Registering the bot with **@BotFather** and getting a token is the entire "auth" story for a
Telegram bot — there's no OAuth flow or key-pair to manage, just a bearer token that identifies
your bot to Telegram's servers. Reading the **`Update`**/**`Message`** shape matters because every
handler you write from Phase 2 onward is just a function of that object — knowing `chat.id` is
"where to reply," `from.id` is "who sent this" (which becomes Phase 7's access control), and
`text` is "the raw string Phase 5 will parse" means the rest of the project is just filling in
blanks you already understand, rather than discovering the API's shape by trial and error while
also debugging your own code.

The **polling vs. webhook** comparison is the one real architectural decision this phase makes.
Webhooks want Telegram's servers to `POST` updates to a public HTTPS URL you control — great for
low-latency, high-volume bots, but it means running a reachable server with a valid TLS cert.
Polling instead has *your* process repeatedly ask Telegram "anything new?" over `getUpdates` — no
public endpoint needed, at the cost of a small poll delay and a process that has to stay running.
For a single-user bot on a home server with no public domain in front of it, polling is the
pragmatic choice — but the goal of this phase is that you arrive at that conclusion from the
tradeoff, not because this doc told you to.

The final raw-`curl`-against-`getUpdates` check exists to isolate failure domains: if you can see
your test message in the raw JSON response, you know the token and your Telegram account are
correctly connected *before* any Python code, a virtualenv, or a library enters the picture — so
if Phase 2's echo bot doesn't work, you already know the problem is in your code, not your setup.
