from util import emoji
from dataclasses import asdict


def task(task_data) -> str:
    task_dict = task_data if type(task_data) is dict else asdict(task_data)

    icon = emoji.green_circle if task_dict['completed'] else emoji.red_circle
    return f"\n{icon} {task_dict['description']}\n"


def to_utc_string(number):
    sign = emoji.plus_minus

    if number > 0:
        sign = "+"
    elif number < 0:
        # number already has '-' sign
        sign = ""

    return f"UTC{sign}{number}"
