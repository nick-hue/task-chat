import html
import os
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import sqlite3
from dataclasses import dataclass

import db
from parser import Result, parse

load_dotenv()
db.init_db()

token = os.environ.get("BOT_TOKEN")


@dataclass
class Command:
    name: str
    description: str
    # callback
    # # handler?


def _build_reply(result: Result, task_id: int | None = None) -> str:
    final_str = f"Added new task [{task_id}]"

    if result.folder == "inbox":
        final_str += " at default folder [inbox]"
    else:
        final_str += f" at folder [{result.folder}]"

    if len(result.tags) > 0:
        final_str += f" with tags: {', '.join(result.tags)}"

    return final_str


async def handler(update, context):
    msg = update.message
    chat_id = update.effective_chat.id

    try:
        result = parse(msg.text)
    except ValueError as e:
        await msg.reply_text(f"Could not save that: {e}")
        return

    task_id = db.insert_task(
        chat_id=chat_id, content=result.content, folder=result.folder, tags=result.tags
    )

    await msg.reply_text(_build_reply(result=result, task_id=task_id))


async def unknown_handler(update, context):

    await update.message.reply_text(
        f"Command <{update.message.text}> does not exist.\n"
        "Try running the /help command to see available commands."
    )


def _build_help_command() -> str:
    return f"\n{'-' * 96}\n".join(
        ["Available commands:"]
        + [f"{cmd.name}:\t{cmd.description}" for cmd in commands]
    )


async def help_handler(update, context):

    await update.message.reply_text(_build_help_command())


def _render_table(header: tuple[str, ...], body: list[tuple[str, ...]]) -> str:
    """Render a fixed-width table. Send inside <pre> with parse_mode="HTML"."""
    table = [header, *body]

    # Widen each column to its longest cell so the separators line up.
    widths = [max(len(cell) for cell in column) for column in zip(*table)]

    lines = [
        " | ".join(cell.ljust(width) for cell, width in zip(cells, widths)).rstrip()
        for cells in table
    ]
    lines.insert(1, "-+-".join("-" * width for width in widths))

    return "\n".join(lines)


def _format_task_listing_verbose(rows: list[sqlite3.Row]) -> str:
    return _render_table(
        ("Id", "Folder", "Tags", "Content"),
        [
            (str(row["id"]), row["folder"], row["tags"] or "-", row["content"])
            for row in rows
        ],
    )


def _format_task_listing(rows: list[sqlite3.Row]) -> str:
    return "\n".join(
        ["Current tasks"] + [f"[{row['id']}]: {row['content']}" for row in rows]
    )


def _format_folder_listing_verbose(rows: list[sqlite3.Row]) -> str:
    return _render_table(
        ("Folder", "Tasks"),
        [(row["folder"], str(row["task_count"])) for row in rows],
    )


def _format_folder_listing(rows: list[sqlite3.Row]) -> str:
    # Pad the folder name, the variable-width part, so the counts share a column.
    name_width = max(len(row["folder"]) for row in rows)
    count_width = max(len(str(row["task_count"])) for row in rows)

    lines = [
        f"{row['folder'].ljust(name_width)}  "
        f"{str(row['task_count']).rjust(count_width)} "
        f"{'task' if row['task_count'] == 1 else 'tasks'}"
        for row in rows
    ]

    return "\n".join(
        ["Current folders", "-" * max(len(line) for line in lines), *lines]
    )


async def list_handler(update, context):
    folder = None
    tags = []
    for arg in context.args:
        if arg.startswith("@"):
            folder = arg[1:]

        if arg.startswith("#"):
            tags.append(arg[1:].lower())

    if tags:
        tags = list(dict.fromkeys(tags))

    rows = db.list_tasks(update.effective_chat.id, folder=folder, tags=tags)
    if not rows:
        await update.message.reply_text("No items to list.")
        return

    if "-v" in context.args:
        table = html.escape(_format_task_listing_verbose(rows))
    else:
        table = html.escape(_format_task_listing(rows))

    await update.message.reply_text(f"<pre>{table}</pre>", parse_mode="HTML")


async def done_handler(update, context):
    if len(context.args) < 1:
        await update.message.reply_text("No id was given. Usage: /done <id> <ids?>")
        return

    ids = []
    for arg in context.args:
        try:
            ids.append(int(arg))
        except ValueError:
            await update.message.reply_text(f"Invalid id <{arg}> was given.")
            return

    updated = db.mark_done(task_ids=ids, chat_id=update.effective_chat.id)
    missing = [i for i in ids if i not in updated]

    lines = []

    if updated:
        lines.append("Marked as done: " + ", ".join([f"[{id}]" for id in updated]))

    if missing:
        lines.append("Could not mark: " + ", ".join([f"[{id}]" for id in missing]))

    await update.message.reply_text("\n".join(lines))


async def delete_handler(update, context):
    if len(context.args) < 1:
        await update.message.reply_text("No id was given. Usage: /rm <id> <ids?>")
        return

    ids = []
    for arg in context.args:
        try:
            ids.append(int(arg))
        except ValueError:
            await update.message.reply_text(f"Invalid id <{arg}> was given.")
            return

    updated = db.delete_task(task_ids=ids, chat_id=update.effective_chat.id)
    missing = [i for i in ids if i not in updated]

    lines = []

    if updated:
        lines.append("Deleted: " + ", ".join([f"[{id}]" for id in updated]))

    if missing:
        lines.append("Could not delete: " + ", ".join([f"[{id}]" for id in missing]))

    await update.message.reply_text("\n".join(lines))


async def folders_handler(update, context):
    rows = db.list_folders(update.effective_chat.id)
    if not rows:
        await update.message.reply_text("No folders found.")
        return

    if "-v" in context.args:
        table = html.escape(_format_folder_listing_verbose(rows))
    else:
        table = html.escape(_format_folder_listing(rows))

    await update.message.reply_text(f"<pre>{table}</pre>", parse_mode="HTML")

    return


app = Application.builder().token(token).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler))
app.add_handler(CommandHandler("help", help_handler))
app.add_handler(CommandHandler("list", list_handler))
app.add_handler(CommandHandler("done", done_handler))
app.add_handler(CommandHandler("rm", delete_handler))
app.add_handler(CommandHandler("folders", folders_handler))
app.add_handler(MessageHandler(filters.COMMAND, unknown_handler))

commands: list[Command] = [
    Command(name="<Plain text>", description="Just type the task you want to add"),
    Command(
        name="/list",
        description="Lists not accomplished tasks. (-v for verbose), (@<folder> for folder filtering), (#<tag> for tag filtering)",
    ),
    Command(name="/done", description="Mark a task as done"),
    Command(name="/rm", description="Delete a task"),
    Command(name="/folders", description="List available folders"),
    Command(name="/help", description="Displays this message"),
]

if __name__ == "__main__":
    app.run_polling()
