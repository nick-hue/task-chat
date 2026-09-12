import os
from dotenv import load_dotenv
from telegram.ext import Application, MessageHandler, filters

load_dotenv()

token = os.environ.get("BOT_TOKEN")


async def handler(update, context):

    msg = update.message
    user = msg.from_user

    await msg.reply_text(f"Hello {user.first_name} you sent {msg.text}")
    print(update)
    print(update.message.chat.id)
    print(type(update.message.chat.id))


app = Application.builder().token(token).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler))


if __name__ == "__main__":
    app.run_polling()
