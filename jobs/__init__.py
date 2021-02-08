from model.user import User
from model.userTask import UserTask
from database import Session
from telegram.ext import CallbackContext
from telegram import ParseMode
from util.get_timezone_where_time import get_timezone_where_time
from util.call_bulk_with_throttling import call_bulk_with_throttling
from util import format, message
import logging
from sqlalchemy.sql import func

logger = logging.getLogger()


def reset_tasks_completed(context: CallbackContext) -> None:
    utc_timezone_offset = get_timezone_where_time(24)

    logger.log(level=logging.INFO, msg=f"Resetting tasks for {format.to_utc_string(utc_timezone_offset)} timezone")

    session = Session()

    session.query(UserTask) \
        .filter(User.utc_offset == utc_timezone_offset) \
        .update({UserTask.completed: False}, synchronize_session='fetch')

    session.commit()


def remind_about_tasks(context: CallbackContext) -> None:
    utc_timezone_offset = get_timezone_where_time(16)

    session = Session()

    base_stmt = session.query(
        UserTask.tg_user_id, func.count("*").label("tasks_count")
    ).group_by(UserTask.tg_user_id)

    tasks_q = base_stmt.subquery()

    tasks_completed_q = base_stmt.filter(UserTask.completed).subquery()

    users = session.query(User, tasks_q.c.tasks_count, tasks_completed_q.c.tasks_count) \
        .outerjoin(tasks_completed_q, User.tg_user_id == tasks_completed_q.c.tg_user_id) \
        .filter(User.utc_offset == utc_timezone_offset,
                func.coalesce(tasks_completed_q.c.tasks_count, 0) < tasks_q.c.tasks_count) \
        .all()

    session.commit()

    bot_messages = []

    def send_remind_about_task(params):
        user_id, text = params
        context.bot.send_message(
            chat_id=user_id,
            text=text,
            parse_mode=ParseMode.MARKDOWN
        )

    for user, tasks_total, tasks_completed in users:
        message_tuple = ()
        if tasks_completed is None:
            message_tuple = (user.tg_user_id, f"It seems like you forgot about *{tasks_total} "
                                              f"tasks* for today\n\n*{message.BAD_RATIO}*")
        else:
            tasks_ratio = tasks_completed / tasks_total

            ratio_text = message.GOOD_RATIO if tasks_ratio > 0.5 else message.BAD_RATIO

            message_tuple = (user.tg_user_id, f"*You've completed {tasks_completed} "
                                              f"({format.to_percentage(tasks_ratio)}) tasks today*\n\n{ratio_text}")

        bot_messages.append(message_tuple)

        call_bulk_with_throttling(func=send_remind_about_task, max_calls=25, sleep_time=2, args_arr=bot_messages)
