from util import emoji


def task(task_data) -> str:
    icon = emoji.green_circle if task_data['completed'] else emoji.red_circle
    return f"\n{icon} {task_data['description']}\n"