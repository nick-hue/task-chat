from enum import StrEnum
import html
import os
from typing import final
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import sqlite3

import db
from parser import Result, parse

load_dotenv()
db.init_db()

token = os.environ.get("BOT_TOKEN")


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


def _format_listing_verbose(rows: list[sqlite3.Row]) -> str:
    """Render rows as a fixed-width table. Send inside <pre> with parse_mode="HTML"."""
    table = [("Id", "Folder", "Tags", "Content")]
    for row in rows:
        table.append(
            (str(row["id"]), row["folder"], row["tags"] or "-", row["content"])
        )

    # Widen each column to its longest cell so the separators line up.
    widths = [max(len(cell) for cell in column) for column in zip(*table)]

    lines = [
        " | ".join(cell.ljust(width) for cell, width in zip(cells, widths)).rstrip()
        for cells in table
    ]
    lines.insert(1, "-+-".join("-" * width for width in widths))

    return "\n".join(lines)


def _format_listing_plain(rows: list[sqlite3.Row]) -> str:
    final_string = "Current Tasks\n"
    for row in rows:
        final_string += f"- {row['content']}\n"
    return final_string


async def list_handler(update, context):
    rows = db.list_tasks(update.effective_chat.id)
    if not rows:
        await update.message.reply_text("No items to list.")
        return
    if "-v" in context.args:
        table = html.escape(_format_listing_verbose(rows))
    else:
        table = html.escape(_format_listing_plain(rows))

    await update.message.reply_text(f"<pre>{table}</pre>", parse_mode="HTML")


app = Application.builder().token(token).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler))
app.add_handler(CommandHandler("list", list_handler))

if __name__ == "__main__":
    app.run_polling()
