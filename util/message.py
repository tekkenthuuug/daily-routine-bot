from util import emoji

NO_TASKS = f"{emoji.eyes}  You don't have any tasks"
TASKS_LIST = f"{emoji.clipboard}  Here is the list of your tasks:"
START = 'I will remind you about your daily routine. \n\nIn order to reset your tasks daily and send notifications ' \
        'I need to know your timezone. \n\nYou can send to me your location or UTC offset itself.\n\n' \
        'Offset examples: \nUTC+1 - offset 1\nUTC-1 - offset -1\nUTC+0 - offset 0 \n\n' \
        '*In case of sending location only your timezone would be saved.*'
BAD_RATIO = "Pull yourself together!"
GOOD_RATIO = "You are doing great, keep up a good pace!"
