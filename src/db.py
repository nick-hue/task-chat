import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "tasks.db"


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


DDL = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS tasks (
    id         INTEGER PRIMARY KEY,
    chat_id    INTEGER NOT NULL,
    content    TEXT    NOT NULL,
    done       INTEGER NOT NULL DEFAULT 0 CHECK (done IN (0, 1)),
    created_at TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    folder     TEXT    NOT NULL DEFAULT 'inbox'
);

CREATE TABLE IF NOT EXISTS tags (
    tag_id   INTEGER PRIMARY KEY,
    tag_name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS task_tags (
    task_id INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    tag_id  INTEGER NOT NULL REFERENCES tags(tag_id),
    PRIMARY KEY (task_id, tag_id)
);
"""


def init_db() -> None:
    conn = connect()
    conn.executescript(DDL)
    conn.commit()
    conn.close()


def insert_task(
    chat_id: int, content: str, folder: str = "inbox", tags: list[str] | None = None
) -> int | None:
    if tags is None:
        tags = []

    conn = connect()
    sql = "INSERT INTO tasks (chat_id, content, folder) VALUES (?, ?, ?)"
    cur = conn.execute(sql, (chat_id, content, folder))
    task_id = cur.lastrowid

    # for each tag the parser found add them to the row
    for tag in tags:
        # add tag to the tag table if it does not exist
        conn.execute("INSERT OR IGNORE INTO tags (tag_name) VALUES (?)", (tag,))
        # get the current tag row
        tag_row = conn.execute(
            "SELECT tag_id FROM tags WHERE tag_name = ?", (tag,)
        ).fetchone()
        # add it to the join table
        conn.execute(
            "INSERT INTO task_tags (task_id, tag_id) VALUES (?, ?)",
            (task_id, tag_row["tag_id"]),
        )

    conn.commit()
    conn.close()
    return task_id


def list_tasks(
    chat_id: int, folder: str | None = None, tags: list[str] | None = None
) -> list[sqlite3.Row]:
    conn = connect()
    # get the tasks that are not done (for now)
    base_clauses = ["t.chat_id = ?", "t.done = 0"]
    params: list = [chat_id]

    if folder:
        base_clauses.append("t.folder = ?")
        params.append(folder)

    if tags:
        placeholders = ", ".join("?" * len(tags))
        base_clauses.append(
            f"""t.id IN (SELECT tt2.task_id
                FROM task_tags tt2
                JOIN tags g2 ON g2.tag_id = tt2.tag_id
                WHERE g2.tag_name IN ({placeholders})
                GROUP BY tt2.task_id
                HAVING count(*) = ?)"""
        )
        params.extend(tags)
        params.append(len(tags))

    sql = f"""
        SELECT t.id, t.content, t.folder, group_concat(g.tag_name, ', ') AS tags
        FROM tasks t
        LEFT JOIN task_tags tt ON tt.task_id = t.id
        LEFT JOIN tags g on g.tag_id = tt.tag_id
        WHERE {" AND ".join(base_clauses)}
        GROUP BY t.id;
        """

    cur = conn.execute(sql, params)
    rows = cur.fetchall()
    conn.close()
    return rows


def mark_done(task_ids: list[int], chat_id: int) -> list[int]:
    conn = connect()

    placeholders = ", ".join("?" * len(task_ids))
    sql = f"UPDATE tasks SET done = 1 WHERE id IN ({placeholders}) AND chat_id = ? RETURNING id"

    rows = conn.execute(sql, [*task_ids, chat_id]).fetchall()

    conn.commit()
    conn.close()
    return [row["id"] for row in rows]


def delete_task(task_ids: list[int], chat_id: int) -> list[int]:
    conn = connect()

    placeholders = ", ".join("?" * len(task_ids))
    sql = f"DELETE from tasks WHERE id IN ({placeholders}) AND chat_id = ? RETURNING id"

    rows = conn.execute(sql, [*task_ids, chat_id]).fetchall()

    conn.commit()
    conn.close()
    return [row["id"] for row in rows]


def list_folders(chat_id: int) -> list[sqlite3.Row]:
    conn = connect()

    sql = "SELECT folder, count(*) AS task_count FROM tasks WHERE chat_id = ? and done = 0 GROUP BY folder"
    rows = conn.execute(sql, (chat_id,)).fetchall()
    conn.close()

    return rows
