#!/usr/bin/python

import ConfigParser
import commands
import telebot
from telebot import types
import time
import unicodedata

knownUsers = []
userStep = {}

commandsbot = {
              'ayuda': 'Informacion de comandos disponibles',
              'mensaje': 'Enviar mensaje para reproducir en el repetidor',
              'sonido': 'Ultimo mensaje que se envio a traves del repetidor',
              'sstv': 'Ultima fotografia que se decodifico por SSTV',
              'estado': 'Estado del sistema'
}

user_dict = {}

class User:
    def __init__(self, callsign):
        self.callsign = callsign
        self.announcement = None

hideBoard = types.ReplyKeyboardHide()

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

def listener(messages):
    for m in messages:
        if m.content_type == 'text':
            print str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text

configuration = ConfigParser.ConfigParser()
configuration.read('configuration/services.config')
token = configuration.get('telegram','token')
bot = telebot.TeleBot(token)
bot.set_update_listener(listener)

@bot.message_handler(commands=['ayuda'])
def command_help(m):
    cid = m.chat.id
    help_text = "Los siguientes comandos estan disponibles: \n"
    for key in commandsbot:
        help_text += "/" + key + ": "
        help_text += commandsbot[key] + "\n"
    bot.send_message(cid, help_text)

@bot.message_handler(commands=["mensaje"])
def command_message(m):
    msg = bot.reply_to(m, "Hola, cual es tu indicativo?")
    bot.register_next_step_handler(msg, process_message)

def process_message(m):
    try:
        chat_id = m.chat.id
        callsign = m.text
        user = User(callsign)
        user_dict[chat_id] = user
        msg = bot.reply_to(m, 'Que anuncio quieres enviar?')
        bot.register_next_step_handler(msg, process_message_repeater)
    except Exception as e:
        bot.reply_to(m, 'Algo no esta funcionando!')

def process_message_repeater(m):
    try:
        chat_id = m.chat.id
        announcement = remove_accents(m.text)
        user = user_dict[chat_id]
        user.announcement = announcement
        bot.send_message(chat_id, 'Gracias *' + user.callsign + \
                                  '*!\nAnuncio: _' + user.announcement + '_', \
                                  parse_mode="Markdown")
        repeater = 'python nuupxe.py -v \"Anuncio recibido desde Telegram\"'
        status, output = commands.getstatusoutput(repeater)
        repeater = 'python nuupxe.py -p \"' + user.callsign + '\"'
        status, output = commands.getstatusoutput(repeater)
        repeater = 'python nuupxe.py -v \"' + user.announcement + '\"'
        status, output = commands.getstatusoutput(repeater)
    except Exception as e:
        bot.reply_to(m, 'Algo no esta funcionando!')

@bot.message_handler(commands=["sonido"])
def command_sound(m):
    cid =  m.chat.id
    audio = open('output/voicerss.mp3', 'rb')
    bot.send_audio(cid, audio)

@bot.message_handler(commands=['sstv'])
def command_sstv(m):
    cid = m.chat.id
    bot.send_photo(cid, open('output/bing.jpg', 'rb'),
                   reply_markup=hideBoard)

@bot.message_handler(commands=["estado"])
def command_status(m):
    bot.reply_to(m, "Estoy vivo!")

#@bot.message_handler(func=lambda message: True, content_types=['text'])
#def command_default(m):
#    bot.send_message(m.chat.id, "Hola! No creo conocer tu comando \"" + m.text + "\"\nQue tal si pides ayuda con /help")

bot.polling()
