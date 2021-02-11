from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from util import button_message, format
from database import Session
from model.userTask import UserTask

TASKS_ON_PAGE = 4


def create_tasks_keyboard_markup(user_id, page_no, scope):
    session = Session()

    user_tasks = session.query(UserTask) \
        .filter(UserTask.tg_user_id == user_id) \
        .order_by(UserTask.created_at) \
        .offset(page_no * TASKS_ON_PAGE) \
        .limit(TASKS_ON_PAGE + 1) \
        .all()

    session.close()

    has_next = False
    has_prev = page_no > 0

    if len(user_tasks) > TASKS_ON_PAGE:
        user_tasks.pop()
        has_next = True

    inline_keyboard_markup = InlineKeyboardMarkup([])

    user_tasks_length = len(user_tasks)

    if user_tasks_length > 0:
        buttons = []

        for i in range(user_tasks_length):
            user_task = user_tasks[i]

            buttons.append(
                [
                    InlineKeyboardButton(text=format.task(user_task),
                                         callback_data=f"UserTask_{scope}_click:{user_task.id}")
                ]
            )

        if has_prev or has_next:
            page_buttons = []

            if has_prev:
                page_buttons.append(
                    InlineKeyboardButton(text=button_message.PREV_MESSAGE,
                                         callback_data=f"UserTask_{scope}_page:{page_no - 1}")
                )

            if has_next:
                page_buttons.append(
                    InlineKeyboardButton(text=button_message.NEXT_MESSAGE,
                                         callback_data=f"UserTask_{scope}_page:{page_no + 1}")
                )

            buttons.append(page_buttons)

        inline_keyboard_markup = InlineKeyboardMarkup(buttons)

    return inline_keyboard_markup
