from telegram.ext import MessageHandler, Filters, CallbackContext, CallbackQueryHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from util import button_message, format
from database import Session
from model.userTask import UserTask

TASKS_ON_PAGE = 4


def create_edit_tasks_markup(user_tasks, page_no, has_next=False, has_prev=False):
    inline_keyboard_markup = InlineKeyboardMarkup([])

    user_tasks_length = len(user_tasks)

    if user_tasks_length > 0:
        buttons = []

        for i in range(user_tasks_length):
            user_task = user_tasks[i]

            buttons.append(
                [
                    InlineKeyboardButton(text=format.task(user_task), callback_data=f"UserTask_toggle:{user_task.id}")
                ]
            )

        if has_prev or has_next:
            page_buttons = []

            if has_prev:
                page_buttons.append(
                    InlineKeyboardButton(text="< Prev", callback_data=f"UserTask_page:{page_no - 1}")
                )

            if has_next:
                page_buttons.append(
                    InlineKeyboardButton(text="Next >", callback_data=f"UserTask_page:{page_no + 1}")
                )

            buttons.append(page_buttons)

        inline_keyboard_markup = InlineKeyboardMarkup(buttons)

    return inline_keyboard_markup


def list_edit_tasks_page(update: Update, context: CallbackContext) -> None:
    user_id = update.callback_query.from_user.id

    callback_query = update.callback_query
    event, page_str = callback_query.data.split(":")
    page_no = int(page_str)

    session = Session()

    has_next = False

    user_tasks = session.query(UserTask) \
        .filter(UserTask.user_id == user_id) \
        .order_by(UserTask.created_at) \
        .offset(page_no * TASKS_ON_PAGE) \
        .limit(TASKS_ON_PAGE + 1) \
        .all()

    if len(user_tasks) > TASKS_ON_PAGE:
        user_tasks.pop()
        has_next = True

    session.commit()

    inline_keyboard_markup = create_edit_tasks_markup(user_tasks, page_no, has_next, page_no > 0)

    context.bot.edit_message_reply_markup(chat_id=update.effective_chat.id,
                                          message_id=update.callback_query.message.message_id,
                                          reply_markup=inline_keyboard_markup)

    update.callback_query.answer()


def list_edit_tasks(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    session = Session()

    user_tasks = session.query(UserTask) \
        .filter(UserTask.user_id == user_id) \
        .order_by(UserTask.created_at) \
        .limit(TASKS_ON_PAGE + 1) \
        .all()

    session.commit()

    has_next = False

    if len(user_tasks) > TASKS_ON_PAGE:
        user_tasks.pop()
        has_next = True

    inline_keyboard_markup = create_edit_tasks_markup(user_tasks, 0, has_next, False)

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Here is the list of your tasks:\n\n*You can toggle task by clicking on it*",
                             reply_markup=inline_keyboard_markup,
                             parse_mode=ParseMode.MARKDOWN)


def edit_task(update: Update, context: CallbackContext) -> None:
    user_id = update.callback_query.from_user.id
    callback_query = update.callback_query
    message_keyboard_markup = callback_query.message.reply_markup.inline_keyboard
    event, task_id = callback_query.data.split(":")

    for i in range(len(message_keyboard_markup)):
        if message_keyboard_markup[i][0].callback_data == callback_query.data:
            session = Session()

            user_task = session.query(UserTask)\
                .filter(UserTask.id == task_id)\
                .filter(UserTask.user_id == user_id)\
                .first()

            user_task.completed = not user_task.completed

            session.commit()

            message_keyboard_markup[i][0] = InlineKeyboardButton(format.task(user_task),
                                                                 callback_data=f"UserTask_toggle:{user_task.id}")

            break

    context.bot.edit_message_reply_markup(chat_id=update.effective_chat.id,
                                          message_id=update.callback_query.message.message_id,
                                          reply_markup=InlineKeyboardMarkup(message_keyboard_markup))

    update.callback_query.answer()


edit_tasks_handler = MessageHandler(Filters.regex(button_message.MANAGE_TASKS_MESSAGE), list_edit_tasks)
callback_edit_task_handler = CallbackQueryHandler(edit_task, pattern=r'^UserTask_toggle:')
callback_tasks_page_handler = CallbackQueryHandler(list_edit_tasks_page, pattern=r'^UserTask_page:')
