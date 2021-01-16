import logging
import requests
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from gizoogle import gizooglelize
from configparser import ConfigParser
from pathlib import Path
from random import choice
from src.handlers import *


def get_token():
    config = ConfigParser()
    config.read('config.cfg')
    return config.get('auth', 'token')


if __name__ == '__main__':
    token = get_token()
    keywords = ['/logfile', '/test']
    keywords_other = ['/wallis']

    logging.basicConfig(filename='logfile.txt', filemode='w',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher

    # All the handlers and the callback functions are imported from handlers.py
    # welcome message
    dispatcher.add_handler(start_handler)

    # jokes mit menu
    dispatcher.add_handler(joke_start_handler)
    dispatcher.add_handler(main_menu_handler)
    dispatcher.add_handler(exit_handler)
    updater.dispatcher.add_handler(first_menu_handler)
    updater.dispatcher.add_handler(second_menu_handler)
    updater.dispatcher.add_handler(send_flach_joke_handler)
    updater.dispatcher.add_handler(send_shortie_joke_handler)

    # sends the UZH Irchel Mensa Menu as a pdf
    dispatcher.add_handler(mensamenu_handler, group=1)

    # sends the logfile to my_id
    dispatcher.add_handler(logfile_handler)

    # responds gangsta style
    gizoogle_handler = MessageHandler(filters=Filters.text, callback=echo_gangster)
    dispatcher.add_handler(gizoogle_handler)

    # print("start_polling...")
    updater.start_polling(timeout=100)
