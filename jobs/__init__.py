from model.user import User
from model.userTask import UserTask
from database import  Session
from datetime import datetime
from telegram.ext import CallbackContext
import logging
logger = logging.getLogger()


def reset_tasks_completed(context: CallbackContext) -> None:
    utc_now = datetime.utcnow()
    time_delta = 24 - utc_now.hour
    utc_timezone_offset = time_delta if time_delta <= 12 else time_delta - 24

    logger.log(level=logging.INFO, msg="Resetting tasks for " + str(utc_timezone_offset) + " timezone")

    session = Session()

    session.query(UserTask)\
        .filter(User.utc_offset == utc_timezone_offset)\
        .update({UserTask.completed: False}, synchronize_session='fetch')

    session.commit()
