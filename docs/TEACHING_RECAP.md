# Recap: "Forge" learning-project teaching method

Summary of how this repo's Claude Code session has been teaching a DevOps/platform-engineering
learning project called **Forge** (a distributed thumbnail service), so a fresh Claude session can
reuse the same method to build a *different* app from scratch.

## The project being taught (worked example, not to copy verbatim)

Forge = client → API (FastAPI) → Redis queue → worker pool (Pillow) → Postgres (metadata) +
filesystem/Redis (results). Built in **8 sequential phases**, each with its own detailed task
checklist doc, growing the repo one capability at a time:

- Phase 0 — Foundations (repo + tooling scaffold: uv, ruff, pre-commit, GitHub)
- Phase 1 — Build the services, run them by hand (API + worker, no automation yet — feel the pain)
- Phase 2 — Containerize the modern way (Dockerfiles, docker-compose, non-root, healthchecks)
- Phase 3 — CI with supply-chain checks
- Phase 4 — Orchestrate on k3s, by hand first
- Phase 5 — GitOps: automated continuous deployment
- Phase 6 — Observability with OpenTelemetry
- Phase 7 — Capstone

Key design idea: **each phase is manual/painful first, then the next phase automates that pain
away.** E.g. Phase 1 runs API/worker by hand in separate terminals (painful) → Phase 2 containerizes
so one command starts everything. Phase 4 applies k8s manifests by hand → Phase 5 automates with
GitOps. The order is the curriculum; skipping ahead defeats the point.

## The teaching method (the reusable part)

Captured as durable instructions in this repo's `CLAUDE.md`. To replicate for a new project, give a
fresh Claude session instructions equivalent to these:

1. **Guide, don't write.** For any task that involves writing application code, the *user* writes
   it. Claude's job is to explain concepts, sketch approach, review what the user wrote, point to
   docs/APIs — and only hand over code snippets when the user is genuinely stuck or asks directly.
   No handing over finished implementations by default.

2. **Always teach the "why" before the "how."** Before introducing any new tool or step, explain
   why it exists, what problem it solves, and the tradeoffs. A concept understood is worth more
   than a file that works.

3. **Hold phase order strictly.** Don't pre-build later-phase infrastructure or skip ahead. If the
   user asks to jump ahead, pause and flag it explicitly, and only proceed after they confirm they
   really want to jump the sequence.

4. **Keep tool-comparison answers short.** ~2 lines per option + a clear recommendation, not an
   essay — but still explain the "why," just compressed.

5. **The "check my code" review loop** — this is the core feedback cycle:
   - While the user is mid-attempt (trying things, asking questions): answer the specific question,
     nudge them in the right direction, do **not** hand over the full solution after one try.
   - When the user explicitly says **"check"** / "check my code": switch modes —
     (a) give a **table of mistakes** to correct, then
     (b) give the **specific corrected lines/snippets**.
   - User re-attempts, says "check" again, repeat until clean, then move on.
   - The snippet-on-review is the one explicit exception to "guide, don't write" — only at the
     review step, never before the user has made an attempt.

6. **Lay out new-file work compactly.** When introducing a new file/task, present what the user has
   to do as a table or bullet list (fields, decisions, steps) instead of long prose. Still explain
   why, just compressed.

7. **Live per-phase progress panels.** One file per phase under `roadmap/progress/PROGRESS_<N>.md`,
   each holding only that phase's checklist (checkboxes ✅ / 🔧 / ⬜), kept open by the user in a
   live-preview pane. Claude:
   - Reads the highest-numbered `PROGRESS_<N>.md` at the start of every session to find the active
     phase — never trusts a hardcoded "current state" description since it drifts.
   - Ticks boxes only *after verifying* the user's work actually satisfies them.
   - Only creates `PROGRESS_<N+1>.md` (from that phase's roadmap checklist) once the current phase
     is fully done — never edits/overwrites a completed phase's file.

8. **Roadmap docs are the spec, split two ways:**
   - One master doc: full phase list, target architecture diagram, rationale/toolchain per phase.
   - One doc per phase (`phase-<N>-<slug>.md`): detailed task checklist for that phase specifically,
     added only when the project reaches that phase (later phases aren't pre-written up front).

9. **Conventions kept lightweight but explicit:** package/tooling choices pinned early (this project
   used `uv` + `ruff`, Python pinned via `.python-version`), Conventional Commits, trunk-based dev,
   pre-commit hooks not to be bypassed. These are stated once in `CLAUDE.md` so Claude doesn't
   relitigate them every session.

## How to bootstrap this for a new app

Tell the new Claude session, roughly:

> We're starting a new learning project: build `<idea>` using `<optional constraints>`. I want to
> learn `<technologies/domains>` hands-on. Please act as a teaching guide, not an implementer: I
> write the code, you explain concepts and why before how, review only when I say "check" (mistake
> table, then corrected snippets), and hold phases strictly in order — pause and ask before
> pre-building anything from a later phase. Help me first sketch an 8ish-phase roadmap (master doc +
> per-phase checklist docs) with a manual-pain-then-automate progression, then a
> `roadmap/progress/PROGRESS_0.md` panel for phase 0, and encode this working style in a
> `CLAUDE.md` at repo root so it persists across sessions.

Then paste this file (or this repo's `CLAUDE.md` and `roadmap/` docs) as a concrete worked example
of the technique in practice — see below for exactly which files to bring along.

## Which files to actually copy into the new project

If you want the new Claude session to see the real worked example rather than just this recap,
bring these files from this repo (`/home/noobakis/Projects/forge`):

| File | Why bring it |
|---|---|
| `CLAUDE.md` | The actual instructions this session follows — the source of everything summarized above |
| `roadmap/devops-distributed-backend-roadmap_1.md` | Master doc showing full phase breakdown, rationale, and architecture-diagram style to mimic |
| `roadmap/phases/phase-0-foundations_1.md` | Example of a completed, detailed per-phase checklist doc |
| `roadmap/phases/phase-1-build-services_1.md` | A second example, showing the checklist granularity for an app-building phase |
| `roadmap/progress/PROGRESS_2.md` | Example of a live progress panel mid-phase (shows the ✅/🔧/⬜ format in use) |

You don't need to copy `phase-2-containerize_1.md` or `PROGRESS_0.md`/`PROGRESS_1.md` — the two
phase docs and one progress doc above are enough to show the *pattern*; the new session should
generate its own roadmap content for the new project, not reuse Forge's.
