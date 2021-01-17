import logging
from telegram.ext import Updater
from handlers import SmallHandler, JokeHandler
from configparser import ConfigParser


def get_token():
    config = ConfigParser()
    config.read('config.cfg')
    return config.get('auth', 'token')

def get_own_id():
    config = ConfigParser()
    config.read('config.cfg')
    id = config.get('auth', 'own_id')
    return int(id)

if __name__ == '__main__':
    token = get_token()
    own_id =get_own_id()
    keywords = ['/logfile', '/test']
    keywords_other = ['/wallis']

    logging.basicConfig(filename='logfile.txt', filemode='w',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher

    joke_handler = JokeHandler(updater, dispatcher, own_id, token)
    small_handlers = SmallHandler(updater, dispatcher, own_id, token)

    joke_handler.start_joke()
    small_handlers.start_message()
    small_handlers.mensamenu_pdf()
    small_handlers.logfile_sender()
    small_handlers.respond_ganster()

    # jokes with menu function
    # dispatcher.add_handler(joke_start_handler)
    # dispatcher.add_handler(main_menu_handler)
    # dispatcher.add_handler(exit_handler)
    # updater.dispatcher.add_handler(first_menu_handler)
    # updater.dispatcher.add_handler(second_menu_handler)
    # updater.dispatcher.add_handler(send_flach_joke_handler)
    # updater.dispatcher.add_handler(send_shortie_joke_handler)


    # sends the logfile to my_id
    # dispatcher.add_handler(logfile_handler)

    # responds gangsta style
    # dispatcher.add_handler(gizoogle_handler)

    # disput handler
    # dispatcher.add_handler(disput_handler, group=2)

    # print("start_polling...")

    small_handlers.updater.start_polling(timeout=100)


