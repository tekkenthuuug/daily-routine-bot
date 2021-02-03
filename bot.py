import os
import logging
from telegram.ext import Updater
from database import create_tables
from handler.add_task import add_task_handler
from handler.view_tasks import view_tasks_handler
from handler.start import start_handler
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    create_tables()

    updater = Updater(os.getenv('TOKEN'))

    dispatcher = updater.dispatcher

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(add_task_handler)
    dispatcher.add_handler(view_tasks_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
