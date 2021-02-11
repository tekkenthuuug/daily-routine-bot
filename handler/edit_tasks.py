from telegram.ext import MessageHandler, Filters, CallbackContext, CallbackQueryHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from util import button_message, format, message
from database import Session
from model.userTask import UserTask
from util.create_tasks_keyboard_markup import create_tasks_keyboard_markup


def change_manage_tasks_page(update: Update, context: CallbackContext) -> None:
    user_id = update.callback_query.from_user.id

    event, page_str = update.callback_query.data.split(":")
    page_no = int(page_str)

    inline_keyboard_markup = create_tasks_keyboard_markup(user_id, page_no, "toggle")

    context.bot.edit_message_reply_markup(chat_id=update.effective_chat.id,
                                          message_id=update.callback_query.message.message_id,
                                          reply_markup=inline_keyboard_markup)

    update.callback_query.answer()


def list_manage_tasks(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    inline_keyboard_markup = create_tasks_keyboard_markup(user_id, 0, "toggle")

    text = f"{message.TASKS_LIST}\n\n*You can toggle task by clicking on it*"
    if len(inline_keyboard_markup.inline_keyboard) <= 0:
        text = message.NO_TASKS

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text,
                             reply_markup=inline_keyboard_markup,
                             parse_mode=ParseMode.MARKDOWN)


def toggle_task(update: Update, context: CallbackContext) -> None:
    user_id = update.callback_query.from_user.id
    callback_query = update.callback_query
    message_keyboard_markup = callback_query.message.reply_markup.inline_keyboard
    event, task_id = callback_query.data.split(":")

    for i in range(len(message_keyboard_markup)):
        if message_keyboard_markup[i][0].callback_data == callback_query.data:
            session = Session()

            user_task = session.query(UserTask)\
                .filter(UserTask.id == task_id)\
                .filter(UserTask.tg_user_id == user_id)\
                .first()

            if user_task is not None:
                user_task.completed = not user_task.completed
                message_keyboard_markup[i][0] = \
                    InlineKeyboardButton(format.task(user_task), callback_data=f"UserTask_toggle_click:{user_task.id}")

                session.commit()
            else:
                del message_keyboard_markup[i]
                session.close()

            break

    context.bot.edit_message_reply_markup(chat_id=update.effective_chat.id,
                                          message_id=update.callback_query.message.message_id,
                                          reply_markup=InlineKeyboardMarkup(message_keyboard_markup))

    update.callback_query.answer()


edit_tasks_handler = MessageHandler(Filters.regex(button_message.MANAGE_TASKS_MESSAGE), list_manage_tasks)
callback_edit_task_handler = CallbackQueryHandler(toggle_task, pattern=r'^UserTask_toggle_click:')
callback_tasks_page_handler = CallbackQueryHandler(change_manage_tasks_page, pattern=r'^UserTask_toggle_page:')
