from telegram.ext import MessageHandler, Filters, CallbackContext, CallbackQueryHandler
from telegram import Update, ParseMode
from util import button_message, message
from database import Session
from model.userTask import UserTask
from util.create_tasks_keyboard_markup import create_tasks_keyboard_markup


def reply(update, context, new_inline_keyboard_markup):
    if len(new_inline_keyboard_markup.inline_keyboard) <= 0:
        context.bot.edit_message_text(chat_id=update.effective_chat.id,
                                      message_id=update.callback_query.message.message_id,
                                      text=message.NO_TASKS,
                                      reply_markup=new_inline_keyboard_markup)

    else:
        context.bot.edit_message_reply_markup(chat_id=update.effective_chat.id,
                                              message_id=update.callback_query.message.message_id,
                                              reply_markup=new_inline_keyboard_markup)

    update.callback_query.answer()


def change_remove_tasks_page(update: Update, context: CallbackContext) -> None:
    user_id = update.callback_query.from_user.id

    event, page_str = update.callback_query.data.split(":")
    page_no = int(page_str)

    reply(update, context, create_tasks_keyboard_markup(user_id, page_no, "remove"))


def list_remove_tasks(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    inline_keyboard_markup = create_tasks_keyboard_markup(user_id, 0, "remove")

    text = f"{message.TASKS_LIST}\n\n*You can remove task by clicking on it*"
    if len(inline_keyboard_markup.inline_keyboard) <= 0:
        text = message.NO_TASKS

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=text,
                             reply_markup=inline_keyboard_markup,
                             parse_mode=ParseMode.MARKDOWN)


def remove_task(update: Update, context: CallbackContext) -> None:
    user_id = update.callback_query.from_user.id
    callback_query = update.callback_query
    message_keyboard_markup = callback_query.message.reply_markup.inline_keyboard
    event, task_id = callback_query.data.split(":")

    for i in range(len(message_keyboard_markup)):
        if message_keyboard_markup[i][0].callback_data == callback_query.data:
            session = Session()

            session.query(UserTask).filter(UserTask.id == task_id).delete()

            session.commit()

            break

    reply(update, context, create_tasks_keyboard_markup(user_id, 0, "remove"))


remove_tasks_handler = MessageHandler(Filters.regex(button_message.REMOVE_TASK_MESSAGE), list_remove_tasks)
callback_remove_task_handler = CallbackQueryHandler(remove_task, pattern=r'^UserTask_remove_click:')
callback_remove_tasks_page_handler = CallbackQueryHandler(change_remove_tasks_page, pattern=r'^UserTask_remove_page:')
