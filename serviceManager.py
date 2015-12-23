#!/usr/bin/python

import logging
import os
import random
import signal
import sys
import thread
import time

from apscheduler.scheduler import Scheduler
from apscheduler.threadpool import ThreadPool

from core.alive import alive
from core.irlp import Irlp
from core.observer import Subscriber, Publisher
from core.voicesynthetizer import VoiceSynthetizer

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
from modules.voicecommand import VoiceCommand
from modules.voicemail import VoiceMail
from modules.weather import Weather
from modules.wolframalpha import WolframAlpha

# Experimental

from modules.assistant import Assistant
from modules.messages import Messages
from learning.morseteacher import MorseTeacher
from modules.voiceexperimental import VoiceExperimental
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
        self.voicesynthetizer = VoiceSynthetizer("google", "spanish")

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
        self.voicecommand = VoiceCommand(self.voicesynthetizer)
        self.voicemail = VoiceMail(self.voicesynthetizer)
        self.weather = Weather(self.voicesynthetizer)
        self.wolframalpha = WolframAlpha(self.voicesynthetizer)

        # Experimental Modules
        self.assistant = Assistant(self.voicesynthetizer)
        self.messages = Messages(self.voicesynthetizer)
        self.morseteacher = MorseTeacher(self.voicesynthetizer)
        self.seismology = Seismology(self.voicesynthetizer)
        self.sstv = SSTV(self.voicesynthetizer)
        self.voiceexperimental = VoiceExperimental(self.voicesynthetizer)
        self.voicemailer = VoiceMailer(self.voicesynthetizer)

    def dtmf_setup(self,dtmf):
        dtmf_codes = {
        'PS0'  : 'alive',
        'PS1'  : 'aprstracker',
        'PS2'  : 'news',
        'PS3'  : 'meteorology',
        'PS4'  : 'seismology',
        'PS5'  : 'selfie',
        'PS6'  : 'voicecommand',
        'PS7'  : 'voiceexperimental',
        'PS8'  : 'wolframalpha',
        'PS9'  : 'voicemail',
        'PS10' : 'sstv',
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
        self.voicesynthetizer.speechit("Modo Planificador")
        self.scheduler = Scheduler(misfire_grace_time=900, coalesce=True, threadpool=ThreadPool(max_threads=1))
        self.schedule()
        self.scheduler.start()
        self.schedule_print()
        self.scheduler_status = True

        while True:
            time.sleep(5)
            if self.irlp.active():
                time.sleep(5)
                self.irlp.busy()
                self.voicesynthetizer.speechit("Se ha activado el nodo, Proyecto NuupXe dice hasta pronto!")
                break

        self.disable()

    def writing_mode(self):

        logging.info('Mode')
        self.voicesynthetizer.speechit("Modo Escritura")

        while True:
            print " Type any text to make use of Text to Speech infraestructure"
            x = raw_input(" Type 'e' for exit: ")
            if x.lower() == 'e':
                self.disable()
                break;
            else:
                self.voicesynthetizer.speechit(x)
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
            self.weather.temperature()
        elif module == 'weather':
            self.weather = Weather(self.voicesynthetizer)
            self.weather.report()

        # PS Activated Modules

        elif module == 'alive':
            alive()
        elif module == 'aprstracker':
            self.aprstracker = AprsTracker(self.voicesynthetizer)
            self.aprstracker.localize()
        elif module == 'news':
            self.news = News(self.voicesynthetizer)
            self.news.getitems()
        elif module == 'meteorology':
            self.meteorology = Meteorology(self.voicesynthetizer)
            self.meteorology.conagua_clima()
        elif module == 'selfie':
            self.selfie = Selfie(self.voicesynthetizer)
            self.selfie.get()
        elif module == 'voicecommand':
            self.voicecommand = VoiceCommand(self.voicesynthetizer)
            self.voicecommand.listen()
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
        elif module == 'voicebackground':
            self.voicecommand = VoiceCommand(self.voicesynthetizer)
            self.voicecommand.background()
        elif module == 'voiceexperimental':
            self.voiceexperimental = VoiceExperimental(self.voicesynthetizer)
            self.voiceexperimental.listen()
        elif module == 'voicemailer':
            self.voicemailer = VoiceMailer(self.voicesynthetizer)
            self.voicemailer.attend(dtmf)
        else:
            print 'Module not found! Please check its name...\n'

        self.disable()

    def schedule_print(self):
        self.scheduler.print_jobs()

    def schedule(self):

        # Production Modules
        self.scheduler.add_cron_job(self.clock.date, month='*', day_of_week='*', hour='06,12,22', minute ='00', second='00')
        self.scheduler.add_cron_job(self.clock.hour, month='*', day_of_week='*', hour='*', minute ='*/15', second='00')
        self.scheduler.add_cron_job(self.identification.identify, month='*', day_of_week='*', hour='*', minute ='*/30', second='00')
        self.scheduler.add_cron_job(self.selfie.get, month='*', day_of_week='*', hour='00,04,08,14,19', minute ='00', second='00')
        self.scheduler.add_cron_job(self.weather.report, month='*', day_of_week='*', hour='*/2', minute ='00', second='00')

        # Experimental Modules
        self.scheduler.add_cron_job(self.seismology.SismologicoMX, month='*', day='*', hour='*/4', minute ='00', second='00')
        self.scheduler.add_cron_job(self.news.getitems, month='*', day='*', hour='*/4', minute ='00', second='00')
        self.scheduler.add_cron_job(self.meteorology.conagua_clima, month='*', day='*', hour='*', minute ='15', second='00')
        self.scheduler.add_cron_job(self.messages.stations, month='*', day='*', hour='*/4', minute ='00', second='00')
        self.scheduler.add_cron_job(self.sstv.decode, month='*', day='*', hour='00,04,08,14,19', minute ='00', second='00')

	# Learning Modules, AREJ
        self.scheduler.add_cron_job(self.messages.readfile,args=['learning/arej.radioclubs'],month='*',day_of_week='*',hour='7,12,17',minute ='00',second='00')

        # Learning Modules, Morse
        self.scheduler.add_cron_job(self.morseteacher.learn, month='*', day='*', hour='07,12,17', minute ='30', second='00')
        self.scheduler.add_cron_job(self.morseteacher.contest, month='*', day='*', hour='07,12,17', minute ='45', second='00')

        # Learning Modules, Reglamentos
        self.scheduler.add_cron_job(self.messages.readfile,args=['learning/reglamentos.1'], month='*', day_of_week='mon', hour='08,13,18', minute ='00', second='00')
        self.scheduler.add_cron_job(self.messages.readfile,args=['learning/reglamentos.2'], month='*', day_of_week='tue', hour='08,13,18', minute ='00', second='00')
        self.scheduler.add_cron_job(self.messages.readfile,args=['learning/reglamentos.3'], month='*', day_of_week='wed', hour='08,13,18', minute ='00', second='00')
        self.scheduler.add_cron_job(self.messages.readfile,args=['learning/reglamentos.4'], month='*', day_of_week='thu', hour='08,13,18', minute ='00', second='00')
        self.scheduler.add_cron_job(self.messages.readfile,args=['learning/reglamentos.5'], month='*', day_of_week='fri', hour='08,13,18', minute ='00', second='00')

# End of File
