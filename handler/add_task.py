from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
from telegram import Update, ParseMode
from util import button_message, keyboard_markup, emoji, format
from model.userTask import UserTask
from database import Session

SET_TASK_NAME, SET_TASK_COMPLETED, CONFIRMATION = range(3)


def request_task_description(update: Update, context: CallbackContext) -> int:
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Describe your task...",
                             reply_markup=keyboard_markup.cancellation)

    return SET_TASK_NAME


def set_task_name(update: Update, context: CallbackContext) -> int:
    context.user_data["description"] = update.message.text

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Have you already completed this task today?",
                             reply_markup=keyboard_markup.confirmation)

    return SET_TASK_COMPLETED


def set_task_completed(update: Update, context: CallbackContext) -> int:
    message_text = update.message.text

    if message_text != button_message.NO_MESSAGE and message_text != button_message.YES_MESSAGE:
        return SET_TASK_COMPLETED

    context.user_data['completed'] = message_text == button_message.YES_MESSAGE
    user_data = context.user_data

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Here is a summary on your task: \n{format.task(user_data)}\n"
                                  f"*Would you like to add it?*",
                             parse_mode=ParseMode.MARKDOWN,
                             reply_markup=keyboard_markup.confirmation)

    return CONFIRMATION


def add_task(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    session = Session()

    user_task = UserTask(description=context.user_data.get('description'),
                         completed=context.user_data.get('completed'),
                         tg_user_id=user_id)

    session.add(user_task)
    session.commit()

    context.bot.send_message(chat_id=update.effective_chat.id, text=f"{emoji.check_mark} Task has been added!",
                             reply_markup=keyboard_markup.main)

    return ConversationHandler.END


def cancel_add_task(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text="Anyway, you can add it anytime!",
                             reply_markup=keyboard_markup.main)

    return ConversationHandler.END


add_task_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex(button_message.ADD_TASK_MESSAGE), request_task_description)],
        states={
            SET_TASK_NAME: [MessageHandler(Filters.text & ~Filters.command &
                                           ~Filters.regex(button_message.CANCEL_MESSAGE), set_task_name)],
            SET_TASK_COMPLETED: [MessageHandler(Filters.text, set_task_completed)],
            CONFIRMATION: [MessageHandler(Filters.regex(button_message.YES_MESSAGE), add_task),
                           MessageHandler(Filters.regex(button_message.NO_MESSAGE), cancel_add_task)],
        },
        fallbacks=[CommandHandler('cancel', cancel_add_task),
                   MessageHandler(Filters.regex(button_message.CANCEL_MESSAGE), cancel_add_task)]
    )