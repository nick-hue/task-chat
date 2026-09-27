# Phase 9 — Deployment

**Goal:** the bot runs on the home server without you watching it, and comes back on its own after a
crash or a reboot. Running `uv run src/bot.py` in an SSH session is not deployment, it is a process
that dies when the session does.

**Estimated time:** ~half a day

**Note:** Phase 8 is still open. Real daily use continues after this, and deploying is largely what
makes that use realistic.

---

## Tasks

- [ ] Push `main` to `origin`, then clone the repo on the server.
- [ ] Install `uv` on the server and run `uv sync`.
- [ ] Create `.env` on the server by hand, with `BOT_TOKEN` and `ALLOWED_USER_ID`.
- [ ] Decide whether `tasks.db` gets copied across or started fresh.
- [ ] Stop the bot on your laptop, then run it manually on the server once to prove it works.
- [ ] Write the systemd unit file.
- [ ] `systemctl enable --now`, then read the log with `journalctl`.
- [ ] Prove it recovers: kill the process, then reboot the server.

**Done when:** you reboot the server, do nothing, and the bot answers you.

---

## Tools introduced this phase

- **systemd** — Linux's service manager. Used here for `Restart=` and starting at boot, nothing more.
- **journalctl** — reads what your `logger` calls and PTB's own logging wrote. This is where the
  Phase 8 habit of reading the morning scrollback moves to.
- **loginctl** — only if you choose a user service. See below.

---

## What each task did

**Two commits will not reach the server on their own.** `git status` says `ahead 2`, so push first.
Cloning is better than `scp` because the next change is a `git pull` instead of a second copy of the
whole tree, and because it makes the server's copy inspectable: `git log` tells you what is actually
running there.

**`.env` is created by hand, never copied by git.** It is gitignored, which is the point. That makes
a missing `.env` on the server the most likely first failure, and the reason Phase 7's startup
validation was worth writing: you get `BOT_TOKEN is missing from .env` instead of a 401 from inside
`run_polling()`.

**Only one process may poll a bot token at a time.** Telegram answers a second `getUpdates` with
HTTP 409 Conflict, and the two instances then fight over every message. Stop the laptop bot before
starting the server one. This will happen to you at least once.

**Copying `tasks.db` is a decision with a wrong answer either way.** Copy it and your Phase 8 tasks
come along, but you now have two files that both look authoritative and you have to remember which.
Start fresh and the history is clean but your real tasks are on the wrong machine. Whichever you
pick, `tasks.db` is now a file on a machine you are not backing up, which belongs on the friction
list.

**User service or system service.** A user service (`~/.config/systemd/user/`, managed with
`systemctl --user`) needs no root and keeps the bot under your own account, which fits a
single-user bot. The catch: it stops when you log out, and does not start at boot, unless you run
`loginctl enable-linger $USER`. A system service (`/etc/systemd/system/`, needs sudo) starts at boot
with no extra step but runs as whatever `User=` you give it, so file ownership on `tasks.db` and
`.env` becomes something to get right. Either is fine. The user service plus lingering is the
smaller blast radius.

**The three lines in the unit that actually matter.**

`WorkingDirectory=` pointing at the repo root is what makes `load_dotenv()` find `.env`, since it
searches upward from the current directory. `DB_PATH` in `db.py` is derived from `__file__`, so the
database resolves correctly either way, but `.env` does not.

`ExecStart=` needs an absolute path to `uv`. systemd runs with a minimal environment and does not
search your shell's `PATH`, so `uv run src/bot.py` alone fails with a status 203 exec error. `which
uv` gives you the path to paste.

`Restart=on-failure` restarts on a non-zero exit, which covers a crash but not a clean shutdown.
Pair it with `RestartSec=` so a broken `.env` does not thrash: the Phase 7 `RuntimeError` exits
non-zero, so systemd would otherwise restart it in a tight loop forever. `systemctl status` showing
`activating (auto-restart)` over and over is what that looks like.

**Killing the process is the real test.** `systemctl status` after a `kill` should show a new PID and
the log should show the bot starting again. Rebooting tests a different thing, whether the unit is
enabled, and on a user service whether lingering is on. Both are worth doing, since each one passes
while the other fails.
