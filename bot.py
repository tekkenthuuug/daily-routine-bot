import os
import logging
from telegram.ext import Updater
from database import create_tables
from handler.add_task import add_task_handler
from handler.view_tasks import view_tasks_handler
from handler.start import start_handler
from handler.edit_tasks import edit_tasks_handler, callback_edit_task_handler, callback_tasks_page_handler
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def main():
    create_tables()

    updater = Updater(os.getenv('TOKEN'))

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
