import os
import logging
from telegram.ext import Updater, CallbackContext
from database import create_tables
from handler.add_task import add_task_handler
from handler.view_tasks import view_tasks_handler
from handler.start import start_handler
from handler.edit_tasks import edit_tasks_handler, callback_edit_task_handler, callback_tasks_page_handler
from dotenv import load_dotenv
from datetime import datetime
from model.user import User
from model.userTask import UserTask
from database import  Session

load_dotenv()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def reset_tasks_completed(context: CallbackContext) -> None:
    utc_now = datetime.utcnow()
    time_delta = 24 - utc_now.hour
    utc_timezone_offset = time_delta if time_delta <= 12 else time_delta - 24

    session = Session()

    userTasks = session.query(UserTask).filter(User.utc_offset == 1).all()

    print(userTasks[0])

    session.commit()


def main():
    create_tables()

    updater = Updater(os.getenv('TOKEN'))

    jq = updater.job_queue

    utc_now_full = datetime.utcnow()
    first_reset_task_time = datetime(utc_now_full.year, utc_now_full.month, utc_now_full.day, utc_now_full.hour + 1)

    job = jq.run_repeating(reset_tasks_completed, interval=3600, first=1)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(add_task_handler)
    dispatcher.add_handler(view_tasks_handler)
    dispatcher.add_handler(edit_tasks_handler)
    dispatcher.add_handler(callback_edit_task_handler)
    dispatcher.add_handler(callback_tasks_page_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
