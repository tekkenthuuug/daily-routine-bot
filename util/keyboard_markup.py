from telegram import KeyboardButton, ReplyKeyboardMarkup
from util import button_message

cancellation = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(button_message.CANCEL_MESSAGE),
        ]
    ],
    resize_keyboard=True
)

skip = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(button_message.SKIP_MESSAGE),
        ]
    ],
    resize_keyboard=True
)

main = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(button_message.LIST_TASKS_MESSAGE),
        ],
        [
            KeyboardButton(button_message.ADD_TASK_MESSAGE),
            KeyboardButton(button_message.MANAGE_TASKS_MESSAGE),
            KeyboardButton(button_message.REMOVE_TASK_MESSAGE)
        ]
    ],
    resize_keyboard=True
)

confirmation = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(button_message.YES_MESSAGE),
            KeyboardButton(button_message.NO_MESSAGE),
        ]
    ],
    resize_keyboard=True,
)
