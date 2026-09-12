import os
from dotenv import load_dotenv
from telegram.ext import Application, MessageHandler, filters

import db

load_dotenv()
db.init_db()

token = os.environ.get("BOT_TOKEN")


async def handler(update, context):
    msg = update.message
    # user = msg.from_user
    chat_id = update.effective_chat.id

    task_id = db.insert_task(chat_id, msg.text)
    await msg.reply_text(f"Saved #{task_id}")


app = Application.builder().token(token).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler))


if __name__ == "__main__":
    app.run_polling()
