#!/usr/bin/python

import configparser
import json
import subprocess
import time
import unicodedata

import telebot
from telebot import types
from apscheduler.schedulers.background import BackgroundScheduler
from collections import OrderedDict

knownUsers = []
userStep = {}

commandsbot = {
              'acerca': 'Acerca de NuupXe Bot',
              'ayuda': 'Informacion de comandos disponibles',
              'anuncio': 'Enviar anuncio para reproducir en el repetidor',
              'bing': 'Obtener fotografia del dia gracias a @Bing',
              'noanuncio': 'Cancelar la reproduccion del anuncio en el repetidor',
              'dtmf': 'Enviar codigo DTMF',
              'estado': 'Estado de NuupXe Bot',
              'modulo': 'Ejecutar modulo',
              'sonido': 'Ultimo mensaje que se envio a traves del repetidor',
              'sstv': 'Ultima fotografia que se decodifico por SSTV',
}

user_dict = {}

class User:
    def __init__(self, callsign):
        self.callsign = callsign
        self.announcement = None
        self.recurrence = None

hideBoard = types.ReplyKeyboardRemove()

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

def listener(messages):
    for m in messages:
        if m.content_type == 'text':
            print(str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text)

configuration = configparser.ConfigParser()
configuration.read('configuration/services.config')
token = configuration.get('telegram', 'token')
bot = telebot.TeleBot(token)
bot.set_update_listener(listener)


responses = None
with open('configuration/messages.json') as f:
    responses = json.load(f, object_pairs_hook=OrderedDict)

sched = BackgroundScheduler()

callsign = None
announcement = None
schedinstance = None

def job_function():
    global callsign
    global announcement
    subprocess.run(['python', 'nuupxe.py', '-p', callsign])
    subprocess.run(['python', 'nuupxe.py', '-v', announcement])

# Handles all sent documents and audio files
@bot.message_handler(content_types=['document', 'audio'])
def handle_docs_audio(message):
    print('audio file')
    pass

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
        if schedinstance:
            sched.remove_job(schedinstance)
    except Exception:
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
    except Exception:
        bot.reply_to(m, 'Algo no esta funcionando!')

def process_message_repeater(m):
    try:
        chat_id = m.chat.id
        announcement = remove_accents(m.text)
        user = user_dict[chat_id]
        user.announcement = announcement
        msg = bot.reply_to(m, 'Cada cuantos minutos quieres ejecutarlo?')
        bot.register_next_step_handler(msg, process_message_recurrence)
    except Exception:
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
            if schedinstance:
                sched.remove_job(schedinstance)
        except Exception:
            pass
        callsign = user.callsign
        announcement = user.announcement
        bot.send_chat_action(chat_id, 'typing')
        time.sleep(2)
        bot.send_message(chat_id, 'Gracias *' + user.callsign +
                                  '*!\nRecurrence: ' + user.recurrence +
                                  '\nAnuncio: _' + user.announcement + '_',
                                  parse_mode="Markdown")
        subprocess.run(['python', 'nuupxe.py', '-v', 'Anuncio recibido desde Telegram'])
        subprocess.run(['python', 'nuupxe.py', '-p', user.callsign])
        subprocess.run(['python', 'nuupxe.py', '-v', user.announcement])
        job = sched.add_job(job_function, 'interval', minutes=recurrence)
        schedinstance = job.id
        if not sched.running:
            sched.start()
    except Exception:
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
        bot.send_message(chat_id, 'Listo! Ejecutaremos *' + module +
                                  '*', parse_mode="Markdown")
        subprocess.run(['python', 'nuupxe.py', '-m', module])
    except Exception:
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
        bot.send_message(chat_id, 'Listo! Enviaremos *' + dtmf +
                                  '*', parse_mode="Markdown")
        subprocess.run(['python', 'nuupxe.py', '-d', dtmf])
    except Exception:
        bot.reply_to(m, 'Algo no esta funcionando!')

@bot.message_handler(commands=["sonido"])
def command_sound(m):
    cid = m.chat.id
    audio = open('output/voicerss.mp3', 'rb')
    bot.send_audio(cid, audio)

@bot.message_handler(commands=['sstv'])
def command_sstv(m):
    cid = m.chat.id
    bot.send_photo(cid, open('output/bing.jpg', 'rb'),
                   reply_markup=hideBoard)

@bot.message_handler(func=lambda m: m.content_type ==
                     'text' and m.text in ['BING', 'Bing', 'bing'])
@bot.message_handler(commands=['bing'])
def command_bing(m):
    cid = m.chat.id
    subprocess.run(['python', 'nuupxe.py', '-b', 'bing'])
    bot.send_photo(cid, open('output/bing.jpg', 'rb'),
                   reply_markup=hideBoard)

@bot.message_handler(func=lambda m: m.content_type ==
                     'text' and m.text in ['ESTADO', 'Estado', 'estado'])
@bot.message_handler(commands=["estado"])
def command_status(m):
    global responses
    bot.reply_to(m, responses['info'])

@bot.message_handler(func=lambda m: m.content_type ==
                     'text' and m.text in ['ACERCA', 'Acerca', 'acerca'])
@bot.message_handler(commands=["acerca"])
def command_acerca(m):
    global responses
    bot.reply_to(m, responses['acerca'])

bot.polling()
