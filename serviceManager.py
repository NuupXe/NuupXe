#!/usr/bin/python

import logging
import os
import random
import signal
import sys
import _thread
import time
import unicodedata

"""
from APScheduler.scheduler import Scheduler
from APScheduler.threadpool import ThreadPool
"""

from core.alive import alive
from core.irlp import Irlp
from core.observer import Subscriber, Publisher
from core.phonetic import Phonetic
from core.voicesynthesizer import VoiceSynthesizer
from apscheduler.schedulers.background import BackgroundScheduler
from concurrent.futures import ThreadPoolExecutor as ThreadPool
from apscheduler.triggers.cron import CronTrigger

# Production

from modules.aprstracker import AprsTracker
from modules.aprstt import Aprstt
from modules.clock import Clock
from modules.identification import Identification
from modules.meteorology import Meteorology
from modules.news import News
from modules.seismology import Seismology
from modules.selfie import Selfie
from modules.sstv import SSTV
from modules.voiceapp import VoiceApp
from modules.audiocommandmanager import AudioCommandManager
from modules.voicemail import VoiceMail
from modules.weather import Weather
from modules.wolframalpha import WolframAlpha

# Experimental

from modules.assistant import Assistant
from modules.messages import Messages
from learning.morseteacher import MorseTeacher
from modules.querymaster import QueryMaster
from modules.voicemailer import VoiceMailer

class ServiceManager(object):

    def __init__(self, irlp):

        self.irlp = irlp
        self.pidfile = None
        self.scheduler_status = False
        self.pidfile = "/tmp/nuupxe.pid"

    def __del__(self):
        pass

    def voicesynthetizer(self):
        self.voicesynthetizer = VoiceSynthesizer("openai", "spanish")

    def voicesynthetizerget(self):
        return self.voicesynthetizer

    def modules_setup(self):

        # Production Modules
        self.aprstracker = AprsTracker(self.voicesynthetizer)
        self.aprstt = Aprstt(self.voicesynthetizer)
        self.clock = Clock(self.voicesynthetizer)
        self.identification = Identification(self.voicesynthetizer)
        self.meteorology = Meteorology(self.voicesynthetizer)
        self.news = News(self.voicesynthetizer)
        self.selfie = Selfie(self.voicesynthetizer)
        self.audiocommandmanager = AudioCommandManager(self.voicesynthetizer)
        self.voicemail = VoiceMail(self.voicesynthetizer)
        self.weather = Weather(self.voicesynthetizer)
        #self.wolframalpha = WolframAlpha(self.voicesynthetizer)

        # Experimental Modules
        self.assistant = Assistant(self.voicesynthetizer)
        self.messages = Messages(self.voicesynthetizer)
        self.morseteacher = MorseTeacher(self.voicesynthetizer)
        self.seismology = Seismology(self.voicesynthetizer)
        self.sstv = SSTV(self.voicesynthetizer)
        self.voiceapp = VoiceApp(self.voicesynthetizer)
        self.querymaster = QueryMaster(self.voicesynthetizer)
        self.voicemailer = VoiceMailer(self.voicesynthetizer)

    def dtmf_setup(self,dtmf):
        dtmf_codes = {
        'PS0'  : 'alive',
        'PS1'  : 'aprstracker',
        'PS2'  : 'news',
        'PS3'  : 'meteorology',
        'PS4'  : 'seismology',
        'PS5'  : 'selfie',
        'PS6'  : 'audiocommandmanager',
        'PS7'  : 'querymaster',
        'PS8'  : 'wolframalpha',
        'PS9'  : 'voicemail',
        'PS10' : 'sstv',
        'PS11' : 'voiceapp',
        }
        return dtmf_codes.get(dtmf)

    def enabled(self):
        return os.path.isfile(self.pidfile)

    def enable(self):

        pid = str(os.getpid())
        logging.info('Process Id' + pid)
        file(self.pidfile, 'w').write(pid)

    def disable(self):

        if self.enabled():
            os.unlink(self.pidfile)
        if self.scheduler_status:
            self.scheduler.shutdown()

    def observer_mode(self):

        logging.info('Mode Observer')
        pub = Publisher(['text', 'voice'])

        # Radio, Twitter, Email, Telegram, Whatsapp

        radio = Subscriber('radio')
        twitter = Subscriber('twitter')
        email = Subscriber('email')
        telegram = Subscriber('telegram')

        pub.register("text", radio)
        pub.register("voice", radio)
        pub.register("text", twitter)
        pub.register("text", email)
        pub.register("text", telegram)
        pub.register("voice", telegram)

        pub.dispatch("text", "this is text")
        pub.dispatch("voice", "this is voice")

    def scheduler_mode(self):

        logging.info('Mode Scheduler')
        self.voicesynthetizer.speech_it("Modo Planificador")

        self.scheduler = BackgroundScheduler(misfire_grace_time=900, coalesce=True, threadpool=ThreadPool(max_workers=1))
        self.schedule()
        self.scheduler.start()
        self.schedule_print()
        self.scheduler_status = True

        while True:
            time.sleep(5)
            if self.irlp.active():
                time.sleep(5)
                self.irlp.busy()
                self.voicesynthetizer.speech_it("Se ha activado el nodo, Proyecto NuupXe dice hasta pronto!")
                break

        self.disable()


    def writing_mode(self):

        logging.info('Mode Writing')
        # self.voicesynthetizer.speech_it("Modo Escritura")

        while True:
            print(" Type any text to make use of Text to Speech infraestructure")
            x = input(" Type 'e' for exit: ")
            if x.lower() == 'e':
                self.disable()
                break;
            else:
                self.voicesynthetizer.speech_it(x)
            time.sleep(1)

    def module_mode(self, module, dtmf=None):

        logging.info('Mode Module ' + module)

        # Custom Decode Activated Modules

        if module == 'identification':
            self.identification = Identification(self.voicesynthetizer)
            self.identification.identify()
        elif module == 'date':
            self.clock = Clock(self.voicesynthetizer)
            self.clock.date()
        elif module == 'hour':
            self.clock = Clock(self.voicesynthetizer)
            self.clock.hour()
        elif module == 'temperature':
            self.weather = Weather(self.voicesynthetizer)
            self.weather.weather_temperature()
        elif module == 'weather':
            self.weather = Weather(self.voicesynthetizer)
            self.weather.weather_report()

        # PS Activated Modules

        elif module == 'alive':
            alive()
        elif module == 'aprstracker':
            self.aprstracker = AprsTracker(self.voicesynthetizer)
            self.aprstracker.localize()
        elif module == 'news':
            self.news = News(self.voicesynthetizer)
            self.news.get_items()
        elif module == 'meteorology':
            self.meteorology = Meteorology(self.voicesynthetizer)
            self.meteorology.conagua_clima()
        elif module == 'selfie':
            self.selfie = Selfie(self.voicesynthetizer)
            self.selfie.get()
        elif module == 'audiocommandmanager':
            self.audiocommandmanager = AudioCommandManager(self.voicesynthetizer)
            self.audiocommandmanager.listen()
        elif module == 'voiceapp':
            self.voiceapp = VoiceApp(self.voicesynthetizer)
            self.voiceapp.application()
        elif module == 'voicemail':
            self.voicemail = VoiceMail(self.voicesynthetizer)
            self.voicemail.run(dtmf)
        elif module == 'wolframalpha':
            self.wolframalpha = WolframAlpha(self.voicesynthetizer)
            self.wolframalpha.ask()

        # SS Activated Modules

        # Experimental Modules

        elif module == 'aprstt':
            self.aprstt = Aprstt(self.voicesynthetizer)
            self.aprstt.query(dtmf)
        elif module == 'seismology':
            self.seismology = Seismology(self.voicesynthetizer)
            self.seismology.SismologicoMX()
        elif module == 'morselearn':
            self.morseteacher = MorseTeacher(self.voicesynthetizer)
            self.morseteacher.learn()
        elif module == 'morsecontest'	:
            self.morseteacher = MorseTeacher(self.voicesynthetizer)
            self.morseteacher.contest()
        elif module == 'regulations':
            self.messages = Messages(self.voicesynthetizer)
            self.messages.readfile('learning/reglamentos.1')
        elif module == 'radioclub':
            self.messages = Messages(self.voicesynthetizer)
            self.messages.readfile('learning/arej.radioclubs')
        elif module == 'stations':
            self.messages = Messages(self.voicesynthetizer)
            self.messages.stations()
        elif module == 'sstv':
            self.sstv = SSTV(self.voicesynthetizer)
            self.sstv.decode()
        elif module == 'assistant':
            self.assistant = Assistant(self.voicesynthetizer)
            self.assistant.demo1()
        elif module == 'audiocommandmanager':
            self.audiocommandmanager = AudioCommandManager(self.voicesynthetizer)
            self.audiocommandmanager.background()
        elif module == 'querymaster':
            self.querymaster = QueryMaster(self.voicesynthetizer)
            self.querymaster.listen()
        elif module == 'voicemailer':
            self.voicemailer = VoiceMailer(self.voicesynthetizer)
            self.voicemailer.attend(dtmf)
        else:
            self.voicesynthetizer.speech_it("No hemos implementado tu comando! Lo siento!")

        self.disable()

    def voice_mode(self, text):
        logging.info('Voice Mode')
        try:
            self.voicesynthetizer.speech_it(text)
        except (StopIteration, KeyboardInterrupt, SystemExit):
            pass

    def phonetic_mode(self, text):
        logging.info('Phonetic Mode')
        phonetic = Phonetic()
        try:
            text = ' '.join(phonetic.decode(text))
            self.voicesynthetizer.speech_it(text)
        except (StopIteration, KeyboardInterrupt, SystemExit):
            pass

    def schedule_print(self):
        self.scheduler.print_jobs()

    def schedule(self):

        # Production Modules
        self.scheduler.add_job(self.clock.date, trigger=CronTrigger(month='*', day_of_week='*', hour='6,12,22', minute='0', second='0'))
        self.scheduler.add_job(self.clock.hour, trigger=CronTrigger(month='*', day_of_week='*', hour='*', minute='*/15', second='0'))
        self.scheduler.add_job(self.identification.identify, trigger=CronTrigger(month='*', day_of_week='*', hour='*', minute='*/30', second='0'))
        self.scheduler.add_job(self.selfie.get, trigger=CronTrigger(month='*', day_of_week='*', hour='0,4,8,14,19', minute='0', second='0'))
        self.scheduler.add_job(self.weather.weather_report, trigger=CronTrigger(month='*', day_of_week='*', hour='*/2', minute='0', second='0'))
        self.scheduler.add_job(self.sstv.decode, trigger=CronTrigger(month='*', day='*', hour='0,4,8,14,19', minute='0', second='0'))

        # Experimental Modules
        self.scheduler.add_job(self.seismology.SismologicoMX, trigger=CronTrigger(month='*', day='*', hour='*/4', minute='0', second='0'))
        self.scheduler.add_job(self.news.getitems, trigger=CronTrigger(month='*', day='*', hour='*/4', minute='0', second='0'))
        self.scheduler.add_job(self.meteorology.conagua_clima, trigger=CronTrigger(month='*', day='*', hour='*', minute='15', second='0'))
        self.scheduler.add_job(self.messages.stations, trigger=CronTrigger(month='*', day='*', hour='*/4', minute='0', second='0'))
        self.scheduler.add_job(self.sstv.decode, trigger=CronTrigger(month='*', day='*', hour='0,4,8,14,19', minute='0', second='0'))
        self.scheduler.add_job(self.selfie.get, trigger=CronTrigger(month='*', day_of_week='*', hour='0,4,8,14,19', minute='0', second='0'))

        # Learning Modules, AREJ
        self.scheduler.add_job(self.messages.readfile, args=['learning/arej.radioclubs'], trigger=CronTrigger(month='*', day_of_week='*', hour='7,12,17', minute='0', second='0'))

        # Learning Modules, Morse
        self.scheduler.add_job(self.morseteacher.learn, trigger=CronTrigger(month='*', day='*', hour='7,12,17', minute='30', second='0'))
        self.scheduler.add_job(self.morseteacher.contest, trigger=CronTrigger(month='*', day='*', hour='7,12,17', minute='45', second='0'))

        # Learning Modules, Reglamentos
        self.scheduler.add_job(self.messages.readfile, args=['learning/reglamentos.1'], trigger=CronTrigger(month='*', day_of_week='mon', hour='8,13,18', minute='0', second='0'))
        self.scheduler.add_job(self.messages.readfile, args=['learning/reglamentos.2'], trigger=CronTrigger(month='*', day_of_week='tue', hour='8,13,18', minute='0', second='0'))
        self.scheduler.add_job(self.messages.readfile, args=['learning/reglamentos.3'], trigger=CronTrigger(month='*', day_of_week='wed', hour='8,13,18', minute='0', second='0'))
        self.scheduler.add_job(self.messages.readfile, args=['learning/reglamentos.4'], trigger=CronTrigger(month='*', day_of_week='thu', hour='8,13,18', minute='0', second='0'))
        self.scheduler.add_job(self.messages.readfile, args=['learning/reglamentos.5'], trigger=CronTrigger(month='*', day_of_week='fri', hour='8,13,18', minute='0', second='0'))

# End of File
