import os
import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, ConversationHandler
from utils import emoji, keyboard_markup, button_message
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

SET_TASK_NAME, SET_TASK_COMPLETED, CONFIRMATION = range(3)

tasks = {}


def format_task(task_data) -> str:
    icon = emoji.green_circle if task_data.get('completed') else emoji.red_circle
    return f"\n{icon} {task_data.get('description')}\n"


def handle_start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Hello, {update.effective_user.first_name}. I will remind you about your daily routine',
                              reply_markup=keyboard_markup.main)


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
                             text=f"Here is a summary on your task: \n{format_task(user_data)}\n"
                                  f"Would you like to add it?",
                             reply_markup=keyboard_markup.confirmation)

    return CONFIRMATION


def add_task(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    if user_id in tasks:
        tasks[user_id].append(context.user_data)
    else:
        tasks[user_id] = [context.user_data]

    context.bot.send_message(chat_id=update.effective_chat.id, text=f"{emoji.check_mark} Task has been added!",
                             reply_markup=keyboard_markup.main)

    return ConversationHandler.END


def cancel_add_task(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text="Anyway, you can add it anytime!",
                             reply_markup=keyboard_markup.main)

    return ConversationHandler.END


def view_tasks(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    result = ""

    if user_id in tasks:
        for i in range(len(tasks[user_id])):
            result += format_task(tasks[user_id][i])
    else:
        result = "You don't have any tasks yet!"

    context.bot.send_message(chat_id=update.effective_chat.id, text=result,
                             reply_markup=keyboard_markup.main)


def main():
    updater = Updater(os.getenv('TOKEN'))

    start_handler = CommandHandler('start', handle_start)

    add_task_conversation_handler = ConversationHandler(
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

    view_tasks_handler = MessageHandler(Filters.regex(button_message.VIEW_TASKS_MESSAGE), view_tasks)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(add_task_conversation_handler)
    dispatcher.add_handler(view_tasks_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
