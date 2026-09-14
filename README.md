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
/list            all open tasks
/list @work      just the work folder
/list #urgent    just the urgent ones
/done 3          mark task 3 complete
/delete 3        remove task 3
/folders         folders in use
```

## Status

| Phase | | |
| --- | --- | --- |
| 1 | Bot registration, API basics | Done |
| 2 | Minimal echo bot | Done |
| 3 | Database schema design | Done |
| 4 | Wire the database to the bot | Done |
| 5 | Parsing logic | Done |
| 6 | Command set | In progress |
| 7 | Access control | |
| 8 | Local run, real-world testing | |
| 9 | Deployment | |
| 10 | Iterate | |
