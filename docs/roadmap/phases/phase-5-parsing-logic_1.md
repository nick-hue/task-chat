# Phase 5 — Parsing logic

**Goal:** turn `"@work buy milk #urgent #shopping"` into a folder, a content string, and a list of
tags. One pure function, tested on its own, then wired in.

**Estimated time:** ~half a day

---

## Tasks

Complete every box before moving to Phase 6.

- [x] Decide the edge-case rules and write them down: no folder, folder not first, repeated tags,
      a message that is only a tag, punctuation attached to a tag.
- [x] Write `src/parser.py` with `parse(text)` returning content, folder and tags.
- [x] Test it against a table of example inputs without starting the bot or touching the database.
- [x] Extend `insert_task()` to take a folder and tags, inserting into `tags` and `task_tags`.
- [x] Wire `parse()` into the handler, and have the reply name the folder and tags it found.
- [x] Send `@work buy milk #urgent` from Telegram and see the folder and both join rows land.

**Done when:** a tagged message from Telegram produces one `tasks` row with the right folder, one
`tags` row per distinct tag, and matching `task_tags` rows. `parser.py` imports neither `telegram`
nor `sqlite3`.

---

## What each task did

**`parse()` is a pure function**, meaning it takes a string and returns a value with no database,
no network, and no global state touched. That is what makes the test step trivial: a list of input
and expected output pairs, run in a fraction of a second, no token and no `tasks.db` in sight. This
is the payoff for keeping the three files apart in Phase 4, and it's why parsing was scheduled
after storage rather than tangled into it.

**Writing the edge cases down first** is the real work of this phase. The happy path takes ten
minutes. What `@work` in the middle of a sentence means, whether `#urgent` and `#Urgent` are one
tag or two, and what happens to a message that is nothing but tags are decisions, not bugs, and
deciding them up front is the difference between a parser and a pile of patches.

**Tags arriving as a list changes `insert_task()`.** One message now writes to three tables: the
task row, a row per new tag, and a join row per tag. `INSERT OR IGNORE` on `tags` handles a tag
that already exists, since you made `tag_name` `UNIQUE` in Phase 3. All of it belongs in one
transaction, so a failure halfway through doesn't leave a task with half its tags.

**The reply naming what it parsed** closes the feedback loop. A bot that silently drops a
misspelled `＃urgent` teaches you nothing. One that answers "saved #3 in @work, tags: urgent"
shows you exactly what it understood.

---

## Parsing rules

Decided before writing the parser. These are the spec, and they double as the test cases.

1. **`@folder` is recognised only as the leading token.** A `@` anywhere else is ordinary text, so
   `email bob@example.com` keeps its address.
2. **With no leading `@folder`, folder is `inbox`.** That matches the column's `DEFAULT`, so
   `parse()` and the schema agree.
3. **A second `@folder` is content.** `@work @home buy milk` gives folder `work` and content
   `@home buy milk`. First wins, no error path.
4. **`#tag` is recognised anywhere in the message.** Consequence accepted: `issue #42` produces a
   tag named `42`.
5. **A tag is `#` followed by letters, digits, underscore or hyphen.** Anything else ends the tag.
   `#urgent.` yields the tag `urgent`, and the `.` stays in the content.
6. **Tags are lowercased.** `#Urgent` and `#urgent` are one tag. Required, since `tag_name` is
   `UNIQUE`.
7. **Tags are deduplicated within one message.** `#urgent #urgent` returns `urgent` once, so the
   composite primary key on `task_tags` never has to reject an insert.
8. **Content is what remains once the tokens are removed**, with runs of whitespace collapsed to
   one space and the ends stripped.
9. **Empty content is rejected.** `@work #urgent` alone parses to nothing, so the bot replies
   saying no task text was found and writes nothing. `content` is `NOT NULL`.

### Worked examples

| Input | folder | content | tags |
|---|---|---|---|
| `buy milk` | inbox | `buy milk` | |
| `@work buy milk` | work | `buy milk` | |
| `@work buy milk #urgent` | work | `buy milk` | urgent |
| `buy #urgent milk` | inbox | `buy milk` | urgent |
| `email bob@example.com` | inbox | `email bob@example.com` | |
| `@work @home buy milk` | work | `@home buy milk` | |
| `milk #Urgent #urgent` | inbox | `milk` | urgent |
| `milk #urgent.` | inbox | `milk .` | urgent |
| `issue #42` | inbox | `issue` | 42 |
| `@work #urgent` | | | rejected |
| `   ` | | | rejected |

Two rows there are deliberate ugliness rather than oversight. `milk .` keeps the orphaned full
stop, because rule 5 says the token is the `#` and the tag characters, nothing more. `issue #42`
tagging `42` is the price of rule 4. Both are cheap to live with and expensive to special-case.
