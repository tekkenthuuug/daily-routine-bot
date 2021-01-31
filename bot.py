import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
from dotenv import load_dotenv
load_dotenv()


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

ADD_TASK_MESSAGE = "🗒  Add"
CONFIRM_MESSAGE = "Confirm"
CANCEL_MESSAGE = "Cancel"

SET_TASK_NAME, CONFIRMATION = range(2)

main_keyboard_markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(ADD_TASK_MESSAGE),
            ]
        ],
        resize_keyboard=True
    )

confirmation_keyboard_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(CONFIRM_MESSAGE),
            KeyboardButton(CANCEL_MESSAGE),
        ]
    ],
    resize_keyboard=True,
)


def format_task(task_data) -> str:
    return f"\n\nDescription: {task_data.get('task_description')}\n\n"


def handle_start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Hello, {update.effective_user.first_name}. I will remind you about your daily routine',
                              reply_markup=main_keyboard_markup)


def request_task_description(update: Update, context: CallbackContext) -> int:
    context.bot.send_message(chat_id=update.effective_chat.id, text="Type in task description:")

    return SET_TASK_NAME


def set_task_name(update: Update, context: CallbackContext) -> int:
    context.user_data["task_description"] = update.message.text

    user_data = context.user_data

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=f"Here is your task: {format_task(user_data)} Is everything OK?",
                             reply_markup=confirmation_keyboard_markup)

    return CONFIRMATION


def add_task(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text="Task has been added!",
                             reply_markup=main_keyboard_markup)

    return ConversationHandler.END


def cancel_add_task(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text="Anyway, you can add it anytime!",
                             reply_markup=main_keyboard_markup)

    return ConversationHandler.END


def main():
    updater = Updater(os.getenv('TOKEN'))

    start_handler = CommandHandler('start', handle_start)

    add_task_conversation_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex(ADD_TASK_MESSAGE), request_task_description)],
        states={
            SET_TASK_NAME: [MessageHandler(Filters.text, set_task_name)],
            CONFIRMATION: [MessageHandler(Filters.regex(CONFIRM_MESSAGE), add_task),
                           MessageHandler(Filters.regex(CANCEL_MESSAGE), cancel_add_task)],
        },
        fallbacks=[CommandHandler('cancel', cancel_add_task)]
    )

    dispatcher = updater.dispatcher

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(add_task_conversation_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
