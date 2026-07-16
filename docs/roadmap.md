# Leaning Roadmap Task chat

## 1. Bot registration & API basics

Get familiar with what a Telegram bot actually is (a token + webhook/polling endpoint). Register one, understand the difference between polling and webhooks, and read just enough of the Bot API docs to know what an "update" object looks like.

## 2. Minimal echo bot

Before touching a database, get a bot running that just receives a message and replies with something. This proves your auth (bot token) and your message loop work before any complexity is added.

## 3. Database schema design

Design the tasks table on paper first — what fields do you need (id, content, folder, tags, done, timestamp), and decide how tags are stored (separate table vs. simple column) before writing code. This is the actual "database management" learning part — think about it before implementing it.

## 4. Wire the database to the bot

Connect the echo bot to your database: every message gets inserted as a row instead of just echoed back. Confirm you can add and read rows from the chat.

## 5. Parsing logic

Add the @folder and #tag extraction on top of a working save. Keep it isolated from the database code so you can test parsing on its own before it touches storage.

## 6. Command set

Add the read/update commands (list, mark done, delete, list folders) one at a time, testing each before moving to the next.

## 7. Access control

Restrict the bot to only respond to your account before you forget and leave it open.

## 8. Local run, real-world testing

Run it from your machine for a few days of actual use, using it like you would day to day, before deploying anywhere.

## 9. Deployment

Move it to your home server and make it persistent (survives reboots, restarts on crash) — this is the "deployment" learning piece, distinct from just running a script.

## 10. Iterate

Once the core loop is solid and deployed, layer on anything extra (due dates, digests) — not before.
Ping me if you want a sanity check at the end of any phase, or if you get stuck on something specific.
