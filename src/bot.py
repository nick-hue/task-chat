import os
from dotenv import load_dotenv
from telegram.ext import Application, MessageHandler, filters

import db
from parser import Result, parse

load_dotenv()
db.init_db()

token = os.environ.get("BOT_TOKEN")


def _build_reply(result: Result, task_id: int) -> str:
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


app = Application.builder().token(token).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler))


if __name__ == "__main__":
    app.run_polling()
