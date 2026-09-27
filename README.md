# task-chat

A Telegram bot that turns messages into tasks. A leading `@folder` routes the
task, `#tag` tokens label it, and the rest is the task itself. Commands read the list back, mark
things done, and delete them.

A learning project, built phase by phase to get hands-on with bot API integration and lightweight
database design. Single user, one database file.

## Usage

Message the bot and it files what you send:

```
buy milk                       → inbox, no tags
@work call the plumber         → folder: work
@home fix the sink #urgent     → folder: home, tags: urgent
pick up parcel #errand #today  → inbox, tags: errand, today
```

Then read it back:

```
/list                  all open tasks
/list -v               with id, folder and tags
/list @work            just the work folder
/list #urgent          just the urgent ones
/done 3                mark task 3 complete
/edit 3 @home mow #yard rewrite task 3, folder and tags included
/rm 3                  delete task 3
/folders               folders in use, with a count each
/help                  the command list
```

Only the Telegram user id in `ALLOWED_USER_ID` gets answers. Anyone else who finds the bot gets a
refusal and their id lands in the log.

## Status

| Phase | | |
| --- | --- | --- |
| 1 | Bot registration, API basics | Done |
| 2 | Minimal echo bot | Done |
| 3 | Database schema design | Done |
| 4 | Wire the database to the bot | Done |
| 5 | Parsing logic | Done |
| 6 | Command set | Done |
| 7 | Access control | Done |
| 8 | Local run, real-world testing | In progress |
| 9 | Deployment | In progress |
| 10 | Iterate | |

`/edit` was pulled forward out of Phase 10 early, so editing a task works already.
