from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, Filters
from settings import BOT_TOKEN, CUSTOM_REPLIES


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


# This function would listen to new messages from the user and send a reply
async def custom_reply(update, context):
    message = update.effective_message.text
    reply_text = CUSTOM_REPLIES.get(message)
    if reply_text:
        update.message.reply_text(text=reply_text)


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("hello", hello))
# A new handler to filter messages received in private chat only
app.add_handler(MessageHandler(custom_reply()))

app.run_polling()
