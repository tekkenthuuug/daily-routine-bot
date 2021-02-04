from telegram import Update
from telegram.ext import CallbackContext, MessageHandler, Filters
from util import button_message, format
from database import Session
from model.userTask import UserTask


def view_tasks(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    text = ""

    session = Session()

    user_tasks = session.query(UserTask).filter(UserTask.tg_user_id == user_id).order_by(UserTask.completed).all()

    session.commit()

    user_tasks_length = len(user_tasks)

    if user_tasks_length > 0:
        for i in range(user_tasks_length):
            text += format.task(user_tasks[i])
    else:
        text = "You don't have any tasks yet!"

    context.bot.send_message(chat_id=update.effective_chat.id, text=text)


view_tasks_handler = MessageHandler(Filters.regex(button_message.LIST_TASKS_MESSAGE), view_tasks)
