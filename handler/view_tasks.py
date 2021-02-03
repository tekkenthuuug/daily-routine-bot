from telegram import Update
from telegram.ext import CallbackContext, MessageHandler, Filters
from util import keyboard_markup, button_message, format
from database import Session
from model.userTask import UserTask


def view_tasks(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    result = ""

    session = Session()

    user_tasks = session.query(UserTask).filter(UserTask.user_id == user_id).order_by(UserTask.completed).all()

    session.commit()

    if len(user_tasks) > 0:
        for i in range(len(user_tasks)):
            result += format.task({'description': user_tasks[i].description, 'completed': user_tasks[i].completed})
    else:
        result = "You don't have any tasks yet!"

    context.bot.send_message(chat_id=update.effective_chat.id, text=result,
                             reply_markup=keyboard_markup.main)


view_tasks_handler = MessageHandler(Filters.regex(button_message.VIEW_TASKS_MESSAGE), view_tasks)
