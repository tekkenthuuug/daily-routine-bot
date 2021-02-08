from telegram import Update, ParseMode
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler, MessageHandler, Filters
from util import keyboard_markup, button_message, time, message, format
from database import Session
from model.user import User


TIMEZONE, CONFIRMATION = range(2)


def greeting(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id

    update.message.reply_text(f'Hello, {update.effective_user.first_name}. {message.START}',
                              reply_markup=keyboard_markup.skip,
                              parse_mode=ParseMode.MARKDOWN)

    session = Session()

    existing_user: User = session.query(User).filter(User.tg_user_id == user_id).first()

    if existing_user is None:
        user = User(tg_user_id=user_id)
        session.add(user)

    session.commit()

    return TIMEZONE


def handle_location(update: Update, context: CallbackContext) -> int:
    user_coordinates = update.message.location

    user_timezone_name = time.timezone_name_from_coordinates(user_coordinates.longitude, user_coordinates.latitude)

    user_utcoffset = time.utcoffset_from_timezone_name(user_timezone_name)

    context.user_data['utcoffset'] = user_utcoffset

    update.message.reply_text(f'Your location is: {user_timezone_name} ({format.to_utc_string(user_utcoffset)})',
                              reply_markup=keyboard_markup.confirmation)

    return CONFIRMATION


def handle_utc_offset(update: Update, context: CallbackContext) -> int:
    text = update.message.text

    try:
        print(text)
        user_utc_offset = int(text)

        if user_utc_offset > 12 or user_utc_offset < -11:
            update.message.reply_text(f'{format.to_utc_string(user_utc_offset)} is not a valid timezone')
            return TIMEZONE
        else:
            context.user_data['utcoffset'] = user_utc_offset

            update.message.reply_text(f'Your timezone is: {format.to_utc_string(user_utc_offset)}',
                                      reply_markup=keyboard_markup.confirmation)

            return CONFIRMATION
    except ValueError:
        update.message.reply_text(f'Please, provide me a valid UTC offset to continue')

        return TIMEZONE


def save_utc_offset(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id

    session = Session()

    user_utc_offset = context.user_data['utcoffset']

    session.query(User).filter(User.tg_user_id == user_id).update({User.utc_offset: user_utc_offset})

    session.commit()

    update.message.reply_text(f'Saved timezone', reply_markup=keyboard_markup.main)

    return ConversationHandler.END


def skip(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f'*You can change your timezone later in settings*',
                              reply_markup=keyboard_markup.main,
                              parse_mode=ParseMode.MARKDOWN)

    return ConversationHandler.END


start_handler = ConversationHandler(
    entry_points=[CommandHandler('start', greeting)],
    states={
        TIMEZONE: [MessageHandler(Filters.location, handle_location),
                   MessageHandler(Filters.text & ~Filters.regex(button_message.SKIP_MESSAGE), handle_utc_offset)],
        CONFIRMATION: [MessageHandler(Filters.regex(button_message.YES_MESSAGE), save_utc_offset),
                       MessageHandler(Filters.regex(button_message.NO_MESSAGE), skip)]
    },
    fallbacks=[CommandHandler('cancel', skip),
               MessageHandler(Filters.regex(button_message.SKIP_MESSAGE), skip)]
)
