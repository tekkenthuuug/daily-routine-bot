from telegram import KeyboardButton, ReplyKeyboardMarkup
import button_messages

cancellation = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(button_messages.CANCEL_MESSAGE),
        ]
    ],
    resize_keyboard=True
)

main = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(button_messages.ADD_TASK_MESSAGE)
        ],
        [
            KeyboardButton(button_messages.REMOVE_TASK_MESSAGE),
            KeyboardButton(button_messages.VIEW_TASKS_MESSAGE),
        ]
    ],
    resize_keyboard=True
)

confirmation = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(button_messages.CONFIRM_MESSAGE),
            KeyboardButton(button_messages.CANCEL_MESSAGE),
        ]
    ],
    resize_keyboard=True,
)
