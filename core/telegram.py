#!/usr/bin/python

import ConfigParser
import commands
import telebot
from telebot import types
import time
import unicodedata

from apscheduler.scheduler import Scheduler

knownUsers = []
userStep = {}

commandsbot = {
              'ayuda': 'Informacion de comandos disponibles',
              'anuncio': 'Enviar anuncio para reproducir en el repetidor',
              'noanuncio': 'Cancelar la reproduccion del anuncio en el repetidor',
              'modulo': 'Ejecutar modulo especifico',
              'dtmf': 'Enviar codigo DTMF especifico',
              'sonido': 'Ultimo mensaje que se envio a traves del repetidor',
              'sstv': 'Ultima fotografia que se decodifico por SSTV',
              'estado': 'Estado del sistema'
}

user_dict = {}

class User:
    def __init__(self, callsign):
        self.callsign = callsign
        self.announcement = None
        self.recurrence = None

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

sched = Scheduler()

callsign = None
announcement = None
schedinstance = None

def job_function():
    global callsign
    global announcement
    repeater = 'python nuupxe.py -p \"' + callsign + '\"'
    status, output = commands.getstatusoutput(repeater)
    repeater = 'python nuupxe.py -v \"' + announcement + '\"'
    status, output = commands.getstatusoutput(repeater)

@bot.message_handler(commands=['ayuda'])
def command_help(m):
    cid = m.chat.id
    help_text = "Los siguientes comandos estan disponibles: \n"
    for key in commandsbot:
        help_text += "/" + key + ": "
        help_text += commandsbot[key] + "\n"
    bot.send_message(cid, help_text)

@bot.message_handler(commands=['noanuncio'])
def command_noannouncement(m):
    cid = m.chat.id
    global schedinstance
    try:
        sched.unschedule_job(schedinstance)
    except:
        pass
    bot.send_message(cid, "Hemos cancelado cualquier anuncio")

@bot.message_handler(commands=["anuncio"])
def command_announcement(m):
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
        msg = bot.reply_to(m, 'Cada cuantos minutos quieres ejecutarlo?')
        bot.register_next_step_handler(msg, process_message_recurrence)
    except Exception as e:
        bot.reply_to(m, 'Algo no esta funcionando!')

def process_message_recurrence(m):
    try:
        chat_id = m.chat.id
        recurrence = m.text
        user = user_dict[chat_id]
        user.recurrence = recurrence
        recurrence = int(user.recurrence)
        global callsign
        global announcement
        global sched
        global schedinstance
        try:
            sched.unschedule_job(schedinstance)
        except:
            pass
        callsign = user.callsign
        announcement = user.announcement
        bot.send_chat_action(chat_id, 'typing')
        time.sleep(2)
        bot.send_message(chat_id, 'Gracias *' + user.callsign + \
                                  '*!\nRecurrence: ' + user.recurrence + \
                                  '\nAnuncio: _' + user.announcement + '_', \
                                  parse_mode="Markdown")
        repeater = 'python nuupxe.py -v \"Anuncio recibido desde Telegram\"'
        status, output = commands.getstatusoutput(repeater)
        repeater = 'python nuupxe.py -p \"' + user.callsign + '\"'
        status, output = commands.getstatusoutput(repeater)
        repeater = 'python nuupxe.py -v \"' + user.announcement + '\"'
        status, output = commands.getstatusoutput(repeater)
        schedinstance = sched.add_interval_job(job_function, minutes=recurrence)
        sched.start()
    except Exception as e:
        bot.reply_to(m, 'Algo no esta funcionando!')

@bot.message_handler(commands=["modulo"])
def command_module(m):
    msg = bot.reply_to(m, "Que modulo quieres ejecutar?")
    bot.register_next_step_handler(msg, process_module)

def process_module(m):
    try:
        chat_id = m.chat.id
        module = m.text.lower()
        bot.send_chat_action(chat_id, 'typing')
        time.sleep(2)
        bot.send_message(chat_id, 'Listo! Ejecutaremos *' + module + \
                                  '*', parse_mode="Markdown")
        repeater = 'python nuupxe.py -m \"' + module + '\"'
        status, output = commands.getstatusoutput(repeater)
    except Exception as e:
        bot.reply_to(m, 'Algo no esta funcionando!')

@bot.message_handler(commands=["dtmf"])
def command_dtmf(m):
    msg = bot.reply_to(m, "Que codigo DTMF quieres enviar?")
    bot.register_next_step_handler(msg, process_dtmf)

def process_dtmf(m):
    try:
        chat_id = m.chat.id
        dtmf = m.text.upper()
        bot.send_chat_action(chat_id, 'typing')
        time.sleep(2)
        bot.send_message(chat_id, 'Listo! Enviaremos *' + dtmf + \
                                  '*', parse_mode="Markdown")
        repeater = 'python nuupxe.py -d \"' + dtmf + '\"'
        print repeater
        status, output = commands.getstatusoutput(repeater)
        print status, output
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
#    bot.send_message(m.chat.id, "Hola! No creo conocer tu comando \"" + m.text + "\"\nQue tal si pides ayuda con /ayuda")

bot.polling()
