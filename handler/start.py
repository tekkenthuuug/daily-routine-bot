from telegram import Update, ParseMode
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler, MessageHandler, Filters
from util import keyboard_markup, button_message, time
from database import Session
from model.user import User


LOCATION, CONFIRMATION = range(2)


def greeting(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id

    update.message.reply_text(f'Hello, {update.effective_user.first_name}. I will remind you about your daily routine.'
                              f'\n\nIn order to reset your tasks daily and send notifications,'
                              f' we need to know your location.\n\n*You location won\'t be saved,'
                              f' only timezone, however this step is completely optional*',
                              reply_markup=keyboard_markup.skip,
                              parse_mode=ParseMode.MARKDOWN)

    session = Session()

    existing_user: User = session.query(User).filter(User.tg_user_id == user_id).first()

    if existing_user is None:
        user = User(tg_user_id=user_id)
        session.add(user)

    session.commit()

    return LOCATION


def handle_location(update: Update, context: CallbackContext) -> int:
    user_coordinates = update.message.location

    user_timezone_name = time.timezone_name_from_coordinates(user_coordinates.longitude, user_coordinates.latitude)

    user_utcoffset = time.utcoffset_from_timezone_name(user_timezone_name)

    context.user_data['utcoffset'] = user_utcoffset

    update.message.reply_text(f'Your location is: {user_timezone_name} (UTC {user_utcoffset})',
                              reply_markup=keyboard_markup.confirmation)

    return CONFIRMATION


def save_utc_offset(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id

    session = Session()

    user_utc_offset = context.user_data['utcoffset']

    session.query(User).filter(User.tg_user_id == user_id).update({User.utc_offset: user_utc_offset})

    session.commit()

    update.message.reply_text(f'Saved timezone', reply_markup=keyboard_markup.main)

    return ConversationHandler.END


def skip(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'*You can change your location later in settings*',
                              reply_markup=keyboard_markup.main,
                              parse_mode=ParseMode.MARKDOWN)

    return ConversationHandler.END


start_handler = ConversationHandler(
    entry_points=[CommandHandler('start', greeting)],
    states={
        LOCATION: [MessageHandler(Filters.location, handle_location)],
        CONFIRMATION: [MessageHandler(Filters.regex(button_message.YES_MESSAGE), save_utc_offset),
                       MessageHandler(Filters.regex(button_message.NO_MESSAGE), skip)]
    },
    fallbacks=[CommandHandler('cancel', skip),
               MessageHandler(Filters.regex(button_message.SKIP_MESSAGE), skip)]
)
