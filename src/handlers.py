from pathlib import Path
from random import choice
from telegram import ParseMode

import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

from gizoogle import gizooglelize


class SmallHandler(Updater):
    def __init__(self, updater, dispatcher, own_id, bot_token):
        self.own_id = own_id
        self.token = bot_token
        self.updater = updater
        self.dispatcher = dispatcher

    def start_message(self):
        # welcome message
        start_handler = CommandHandler('start', self.start)
        self.dispatcher.add_handler(start_handler)

    def start(self, update, context):
        print("start")
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Hoi, ich heisse trooublebot. Ich bin en Hausgeist!")

    def mensamenu_pdf(self):
        mensamenu_handler = CommandHandler('mensamenu', self.mensamenu)
        self.dispatcher.add_handler(mensamenu_handler, group=1)

    def mensamenu(self, update, context):
        menu_url = "http://zfv.ch/de/menuplan-download/142"
        SmallHandler.read_pdf_from_url(menu_url, 'downloads/menu.pdf')
        document = open('downloads/menu.pdf', 'rb')
        # reply = 'Für diese Woche wurde leider kein Menueplan gefunden.'
        # context.bot.send_message(chat_id=update.effective_chat.id, text=reply)
        context.bot.send_document(chat_id=update.effective_chat.id, document=document,
                                  filename='hopefully_without_pilze.pdf', caption='Da häsch din Irchel Mensa Wucheplan',
                                  disable_notification=True)

    @staticmethod
    def read_pdf_from_url(url, name):
        filename = Path(name)
        response = requests.get(url)
        filename.write_bytes(response.content)

    def logfile_sender(self):
        # sends the logfile to my_id
        logfile_handler = MessageHandler(filters=Filters.text(["/logfile"]), callback=self.send_logfile)
        self.dispatcher.add_handler(logfile_handler)

    def send_logfile(self, update, context):
        document = open('logfile.txt', 'rb')
        if update.effective_user['id'] == self.own_id:
            # logtxt = "sending logfile to user {}".format(update.effective_user.id)
            # logging.info(logtxt)
            context.bot.send_document(chat_id=update.effective_chat.id, document=document, disable_notification=True)
        document.close()

    def respond_ganster(self):
        # responds gangsta style
        gizoogle_handler = MessageHandler(filters=Filters.text & (~Filters.command), callback=self.echo_gangster)
        self.dispatcher.add_handler(gizoogle_handler)

    def echo_gangster(self, update, context):
        reply = gizooglelize(update.message.text)
        context.bot.send_message(chat_id=update.effective_chat.id, text=reply, disable_notification=True)

    def planck_command(self):
        # Belegungsplan handler
        planck_handler = CommandHandler('planckraum', self.planckraum)
        self.dispatcher.add_handler(planck_handler, group=2)

    def planckraum(self, update, context):
        print("Planckraum Belegungsplan")
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="<a href='https://www.sharedequipment.uzh.ch/EZbooking/cgi-bin/ezb_timeCalendar."
                                      "cgi?publicUserID=1&KeyNameID=EZbooking&isPopup=1&catID=14&objectID=480&calendar"
                                      "Type=1048640&refreshRate=1'>Belegungsplans Planckraum Klick!</a>", parse_mode=ParseMode.HTML)


class JokeHandler(Updater):
    def __init__(self, updater, dispatcher, own_id, bot_token):
        self.own_id = own_id
        self.token = bot_token
        self.updater = updater
        self.dispatcher = dispatcher

    def start_joke(self):
        # jokes mit menu
        joke_start_handler = CommandHandler('joke', self.joke)
        main_menu_handler = CallbackQueryHandler(self.main_menu, pattern='main')
        exit_handler = CallbackQueryHandler(self.exit_menu, pattern='exit')
        first_menu_handler = CallbackQueryHandler(self.first_menu, pattern='m1')
        second_menu_handler = CallbackQueryHandler(self.second_menu, pattern='m2')
        send_flach_joke_handler = CallbackQueryHandler(self.send_flach_joke, pattern='flacher')
        send_shortie_joke_handler = CallbackQueryHandler(self.send_shorite_joke, pattern='shortie')
        self.dispatcher.add_handler(joke_start_handler)
        self.dispatcher.add_handler(main_menu_handler)
        self.dispatcher.add_handler(exit_handler)
        self.updater.dispatcher.add_handler(first_menu_handler)
        self.updater.dispatcher.add_handler(second_menu_handler)
        self.updater.dispatcher.add_handler(send_flach_joke_handler)
        self.updater.dispatcher.add_handler(send_shortie_joke_handler)

    def choose_joke(self, category):
        data_folder = Path("jokes/")
        file_to_open = data_folder / (category + ".csv")
        f = open(file_to_open, encoding='utf-8')
        joke_list = f.readlines()
        return choice(joke_list)

    def send_flach_joke(self, update, context):
        joke = self.choose_joke('flach')
        user_name = update.effective_user.first_name
        joke = joke.replace(r'/NAME1', user_name)
        self.exit_menu(update, context)
        context.bot.send_message(chat_id=update.effective_chat.id, text=joke)

    def send_shorite_joke(self, update, context):
        joke = self.choose_joke('shorties')
        user_name = update.effective_user.first_name
        joke = joke.replace(r'/NAME1', user_name)
        self.exit_menu(update, context)
        context.bot.send_message(chat_id=update.effective_chat.id, text=joke)

    def joke(self, update, context):
        update.message.reply_text(self.main_menu_message(), reply_markup=self.main_menu_keyboard(),
                                  disable_notification=True)

    def main_menu(self, update, context):
        update.effective_message.edit_text(self.main_menu_message(), reply_markup=self.main_menu_keyboard())

    def exit_menu(self, update, context):
        token = self.token
        cid = update.effective_chat.id  # chat id
        mid = update.effective_message.message_id  # message id
        url = 'https://api.telegram.org/bot{}/deleteMessage?chat_id={}&message_id={}'.format(token, cid, mid)
        requests.get(url)

    def first_menu(self, update, context):
        update.callback_query.message.edit_text(self.first_menu_message(), reply_markup=self.shortie_menu_keyboard())

    def second_menu(self, update, context):
        update.callback_query.message.edit_text(self.second_menu_message(), reply_markup=self.second_menu_keyboard())

    def main_menu_keyboard(self):
        keyboard = [[InlineKeyboardButton('Ein Shortie', callback_data='m1')],
                    [InlineKeyboardButton('Ein Flacher', callback_data='m2')],
                    [InlineKeyboardButton('Exit', callback_data='exit')]]
        return InlineKeyboardMarkup(keyboard)

    def shortie_menu_keyboard(self):
        keyboard = [[InlineKeyboardButton('Generiere zufälligen Witz', callback_data='shortie')],
                    [InlineKeyboardButton('Zurück', callback_data='main')]]
        return InlineKeyboardMarkup(keyboard)

    def second_menu_keyboard(self):
        keyboard = [[InlineKeyboardButton('Generiere zufälligen Witz', callback_data='flacher')],
                    [InlineKeyboardButton('Zurück', callback_data='main')]]
        return InlineKeyboardMarkup(keyboard)

    def first_menu_message(self):
        return 'Vorsicht! Es kann sein, dass du selber verarscht wirst!'

    def second_menu_message(self):
        return 'Vorsicht! Der kommt ziemlich flach. Mit dir in der Hauptrolle!'

    def exit_message(self):
        return 'bye'

    def main_menu_message(self):
        return 'Wähle eine Witzkategorie aus:'


class ScrapingHandler(Updater):
    def __init__(self, updater, dispatcher, own_id, bot_token):
        self.own_id = own_id
        self.token = bot_token
        self.updater = updater
        self.dispatcher = dispatcher
