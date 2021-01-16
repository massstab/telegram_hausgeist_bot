import logging
import requests
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from gizoogle import gizooglelize
from configparser import ConfigParser
from pathlib import Path
from random import choice



def get_token():
    config = ConfigParser()
    config.read('config.cfg')
    return config.get('auth', 'token')


def read_pdf_from_url(url, name):
    filename = Path(name)
    response = requests.get(url)
    filename.write_bytes(response.content)


def start(update, context):
    print("start")
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Hoi, ich heisse trooublebot. Ich bin en Hausgeist!")


def mensamenu(update, context):
    menu_url = "http://zfv.ch/de/menuplan-download/142"
    read_pdf_from_url(menu_url, 'downloads/menu.pdf')
    document = open('downloads/menu.pdf', 'rb')
    # reply = 'Für diese Woche wurde leider kein Menueplan gefunden.'
    # context.bot.send_message(chat_id=update.effective_chat.id, text=reply)
    context.bot.send_document(chat_id=update.effective_chat.id, document=document,
                              filename='hopefully_without_pilze.pdf', caption='Da häsch din Irchel Mensa Wucheplan', disable_notification=True)


def echo_gangster(update, context):
    reply = gizooglelize(update.message.text)
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply, disable_notification=True)


def send_loggfile(update, context):
    document = open('logfile.txt', 'rb')
    if update.effective_user['id'] == my_own_id:
        # logtxt = "sending logfile to user {}".format(update.effective_user.id)
        # logging.info(logtxt)
        context.bot.send_document(chat_id=update.effective_chat.id, document=document, disable_notification=True)
    document.close()


def choose_joke(category):
    data_folder = Path("jokes/")
    file_to_open = data_folder / (category + ".csv")
    f = open(file_to_open, encoding='utf-8')
    joke_list = f.readlines()
    return choice(joke_list)


def send_flach_joke(update, context):
    joke = choose_joke('flach')
    user_name = update.effective_user.first_name
    joke = joke.replace(r'/NAME1', user_name)
    exit(update, context)
    context.bot.send_message(chat_id=update.effective_chat.id, text=joke)

def send_shorite_joke(update, context):
    joke = choose_joke('shorties')
    user_name = update.effective_user.first_name
    joke = joke.replace(r'/NAME1', user_name)
    exit(update, context)
    context.bot.send_message(chat_id=update.effective_chat.id, text=joke)


def joke(update, context):
    update.message.reply_text(main_menu_message(), reply_markup=main_menu_keyboard(), disable_notification=True)

def main_menu(update, context):
    update.effective_message.edit_text(main_menu_message(), reply_markup=main_menu_keyboard())


def exit(update, context):
    token = get_token()
    cid = update.effective_chat.id  # chat id
    mid = update.effective_message.message_id  # message id
    url = 'https://api.telegram.org/bot{}/deleteMessage?chat_id={}&message_id={}'.format(token, cid, mid)
    requests.get(url)


def first_menu(update, context):
    update.callback_query.message.edit_text(first_menu_message(), reply_markup=shortie_menu_keyboard())


def second_menu(update, context):
    update.callback_query.message.edit_text(second_menu_message(), reply_markup=second_menu_keyboard())


def main_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Ein Shortie', callback_data='m1')],
                [InlineKeyboardButton('Ein Flacher', callback_data='m2')],
                [InlineKeyboardButton('Exit', callback_data='exit')]]
    return InlineKeyboardMarkup(keyboard)


def shortie_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Generiere zufälligen Witz', callback_data='shortie')],
                [InlineKeyboardButton('Zurück', callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)


def second_menu_keyboard():
    keyboard = [[InlineKeyboardButton('Generiere zufälligen Witz', callback_data='flacher')],
                [InlineKeyboardButton('Zurück', callback_data='main')]]
    return InlineKeyboardMarkup(keyboard)


def first_menu_message():
    return 'Vorsicht! Es kann sein, dass du selber verarscht wirst!'


def second_menu_message():
    return 'Vorsicht! Der kommt ziemlich flach. Mit dir in der Hauptrolle!'


def exit_message():
    return 'bye'


def main_menu_message():
    return 'Wähle eine Witzkategorie aus:'


if __name__ == '__main__':
    token = get_token()
    my_own_id = 900605678
    keywords = ['/logfile', '/test']
    keywords_other = ['/wallis']

    logging.basicConfig(filename='logfile.txt', filemode='w',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher

    # welcome message
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    # jokes mit menu
    joke_start_handler = CommandHandler('joke', joke)
    dispatcher.add_handler(joke_start_handler)

    main_menu_handler = CallbackQueryHandler(main_menu, pattern='main')
    dispatcher.add_handler(main_menu_handler)

    exit_handler = CallbackQueryHandler(exit, pattern='exit')
    dispatcher.add_handler(exit_handler)

    first_menu_handler = CallbackQueryHandler(first_menu, pattern='m1')
    updater.dispatcher.add_handler(first_menu_handler)

    second_menu_handler = CallbackQueryHandler(second_menu, pattern='m2')
    updater.dispatcher.add_handler(second_menu_handler)

    send_flach_joke_handler = CallbackQueryHandler(send_flach_joke, pattern='flacher')
    updater.dispatcher.add_handler(send_flach_joke_handler)

    send_shortie_joke_handler = CallbackQueryHandler(send_shorite_joke, pattern='shortie')
    updater.dispatcher.add_handler(send_shortie_joke_handler)

    # sends the UZH Irchel Mensa Menu as a pdf
    mensamenu_handler = CommandHandler('mensamenu', mensamenu)
    dispatcher.add_handler(mensamenu_handler, group=1)

    # sends the logfile to my_id
    logfile_handler = MessageHandler(filters=Filters.text(["/logfile"]), callback=send_loggfile)
    dispatcher.add_handler(logfile_handler)

    # responds gangsta style
    gizoogle_handler = MessageHandler(filters=Filters.text, callback=echo_gangster)
    dispatcher.add_handler(gizoogle_handler)

    # print("start_polling...")
    updater.start_polling(timeout=100)
