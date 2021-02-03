from telegram import Update
from telegram.ext import CallbackContext, CommandHandler
from util import keyboard_markup


def handle_start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'Hello, {update.effective_user.first_name}. I will remind you about your daily routine',
                              reply_markup=keyboard_markup.main)


start_handler = CommandHandler('start', handle_start)
