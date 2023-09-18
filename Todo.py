# import asyncio
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, filters, MessageHandler, PicklePersistence

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Define the states of the conversation
TASK, DELETE = range(2)


# Define the start function
async def start_bot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text='Hi! I am Lena, your todo list bot. You can add tasks by sending me messages.\n'
                                        'After typing your task, use the /new command to add it to your todo list.\n'
                                        'To see all your tasks, use the /list command.\n'
                                        'To see these options again, use the /help command.\n')

    return TASK


# A function to let users create to do
async def create_task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_id = update.effective_message.message_id
    print(message_id)
    message_text = update.effective_message.text
    print(message_text)
    todo_title = message_text.replace("/new ", "")
    print(todo_title)
    context.user_data[message_id] = {"title": todo_title, "completed": False}
    print(context.user_data)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Todo successfully created")


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
    Available commands:
    /start => start bot:
    /new => Make a new Todo
    /list => To show list of Todos
    """
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)


# A function to view todo
async def show_todo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #   text, reply_markup = parent_todo(context)
    text = "Here are the list of your task:\n"
    keyboard = []
    for key, value in context.user_data.items():
        status_icon = "✔" if value["completed"] else "✖"
        to_do = value["title"] + " " + status_icon
        keyboard.append(
            [InlineKeyboardButton(text=to_do, callback_data=key)]
        )
        text += "- " + to_do
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=f"Your tasks:\n{text}", reply_markup=reply_markup)


# async def parent_todo(context: ContextTypes.DEFAULT_TYPE):
#   text="Here are the list of your task:\n"
#  keyboard = []
# for key, value in context.user_data.items():
#    status_icon = "✔" if value["completed"] else "✖"
#   to_do = value["title"] + " " + status_icon
#  keyboard.append(
#         [InlineKeyboardButton(text=to_do, callback_data=key)]
#    )
# text += "- " + to_do
# reply_markup = InlineKeyboardMarkup(keyboard)
# return await text, reply_markup

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    toDo_id = int(query.data)
    task_status = context.user_data[toDo_id]['completed']
    context.user_data[toDo_id]['completed'] = not task_status
    # text, reply_markup = parent_todo(context)
    text = "Here are the list of your task:\n"
    keyboard = []
    for key, value in context.user_data.items():
        status_icon = "✔" if value["completed"] else "✖"
        to_do = value["title"] + " " + status_icon
        keyboard.append(
            [InlineKeyboardButton(text=to_do, callback_data=key)]
        )
        text += "- " + to_do
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.answer(text='Status successfully updated')
    await query.edit_message_text(text=text, reply_markup=reply_markup)


if __name__ == '__main__':
    my_persistence = PicklePersistence(filepath='todo')
    application = ApplicationBuilder().token('6696230486:AAHn2IyePbZSG4bPT0xjXlQFeo0oFmSICrw').persistence(
        my_persistence).build()

    create_handler = CommandHandler('new', create_task)
    application.add_handler(create_handler)

    start_handler = CommandHandler('start', start_bot)
    application.add_handler(start_handler)

    help_handler = CommandHandler('help', help)
    application.add_handler(help_handler)

    show_handler = CommandHandler('list', show_todo)
    application.add_handler(show_handler)

    application.add_handler(CallbackQueryHandler(button))

    application.run_polling(poll_interval=5)
