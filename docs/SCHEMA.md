# SCHEMA

## Tables

### Tasks

id, INTEGER PRIMARY KEY
chat_id, INTEGER NOT NULL
content, text NOT NULL
done, INTEGER NOT NULL DEFAULT 0 CHECK (done IN (0, 1))  
created_at, TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
folder, text NOT NULL DEFAULT 'inbox'

### Tags

I chose the join table because it gives exact match filtering, even though its 3 tables instead of 1 with comma seperated values. Although I matches the functionality i want with #urgent instead of using non existant tags like /#urgently

tag_id, INTEGER PRIMARY KEY
tag_name, text not null UNIQUE

### Task Tags

task_id, INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE
tag_id, INTEGER NOT NULL REFERENCES tags(tag_id)
PRIMARY KEY (task_id, tag_id)

## DDL

Run these in order. `tasks` and `tags` must exist before `task_tags` can reference them.

```sql
PRAGMA foreign_keys = ON;

CREATE TABLE tasks (
    id         INTEGER PRIMARY KEY,
    chat_id    INTEGER NOT NULL,
    content    TEXT    NOT NULL,
    done       INTEGER NOT NULL DEFAULT 0 CHECK (done IN (0, 1)),
    created_at TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    folder     TEXT    NOT NULL DEFAULT 'inbox'
);

CREATE TABLE tags (
    tag_id   INTEGER PRIMARY KEY,
    tag_name TEXT NOT NULL UNIQUE
);

CREATE TABLE task_tags (
    task_id INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    tag_id  INTEGER NOT NULL REFERENCES tags(tag_id),
    PRIMARY KEY (task_id, tag_id)
);
```

`PRAGMA foreign_keys = ON` is per connection, not per database. It has to run every
time `db.py` connects, not once at creation time.
