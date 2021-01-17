from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler
from pathlib import Path
from telegram import ReplyKeyboardMarkup
import requests
from configparser import ConfigParser
from gizoogle import gizooglelize

def get_token():
    config = ConfigParser()
    config.read('config.cfg')
    return config.get('auth', 'token')


def get_own_id():
    config = ConfigParser()
    config.read('config.cfg')
    id = config.get('auth', 'own_id')
    return int(id)

def start(update, context):
    print("start")
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Hoi, ich heisse trooublebot. Ich bin en Hausgeist!")



def send_loggfile(update, context):
    document = open('logfile.txt', 'rb')
    if update.effective_user['id'] == my_own_id:
        # logtxt = "sending logfile to user {}".format(update.effective_user.id)
        # logging.info(logtxt)
        context.bot.send_document(chat_id=update.effective_chat.id, document=document, disable_notification=True)
    document.close()


def echo_gangster(update, context):
    reply = gizooglelize(update.message.text)
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply, disable_notification=True)


my_own_id = get_own_id()
# welcome message
start_handler = CommandHandler('start', start)

# sends the logfile to my_id
logfile_handler = MessageHandler(filters=Filters.text(["/logfile"]), callback=send_loggfile)

# responds gangsta style
gizoogle_handler = MessageHandler(filters=Filters.text, callback=echo_gangster)

