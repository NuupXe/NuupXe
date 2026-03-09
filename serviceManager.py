#!/usr/bin/python

import logging
import os
import sys
import time

from core.alive import alive
from core.irlp import Irlp
from core.observer import Subscriber, Publisher
from core.phonetic import Phonetic
from core.voicesynthesizer import VoiceSynthesizer
from apscheduler.schedulers.background import BackgroundScheduler
from concurrent.futures import ThreadPoolExecutor as ThreadPool
from apscheduler.triggers.cron import CronTrigger


class ServiceManager(object):

    def __init__(self, irlp):

        self.irlp = irlp
        self.pidfile = "/tmp/nuupxe.pid"
        self.scheduler_status = False

    def setup_synthesizer(self):
        self.voicesynthesizer = VoiceSynthesizer("openai", "spanish")

    def voicesynthesizerget(self):
        return self.voicesynthesizer

    def modules_setup(self):
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
        from modules.assistant import Assistant
        from modules.messages import Messages
        from modules.querymaster import QueryMaster
        from modules.voicemailer import VoiceMailer
        from learning.morseteacher import MorseTeacher

        self.aprstracker = AprsTracker(self.voicesynthesizer)
        self.aprstt = Aprstt(self.voicesynthesizer)
        self.clock = Clock(self.voicesynthesizer)
        self.identification = Identification(self.voicesynthesizer)
        self.meteorology = Meteorology(self.voicesynthesizer)
        self.news = News(self.voicesynthesizer)
        self.selfie = Selfie(self.voicesynthesizer)
        self.audiocommandmanager = AudioCommandManager(self.voicesynthesizer)
        self.voicemail = VoiceMail(self.voicesynthesizer)
        self.weather = Weather(self.voicesynthesizer)
        self.assistant = Assistant(self.voicesynthesizer)
        self.messages = Messages(self.voicesynthesizer)
        self.morseteacher = MorseTeacher(self.voicesynthesizer)
        self.seismology = Seismology(self.voicesynthesizer)
        self.sstv = SSTV(self.voicesynthesizer)
        self.voiceapp = VoiceApp(self.voicesynthesizer)
        self.querymaster = QueryMaster(self.voicesynthesizer)
        self.voicemailer = VoiceMailer(self.voicesynthesizer)

    def dtmf_setup(self, dtmf):
        dtmf_codes = {
            'PS0':  'alive',
            'PS1':  'aprstracker',
            'PS2':  'news',
            'PS3':  'meteorology',
            'PS4':  'seismology',
            'PS5':  'selfie',
            'PS6':  'audiocommandmanager',
            'PS7':  'querymaster',
            'PS8':  'wolframalpha',
            'PS9':  'voicemail',
            'PS10': 'sstv',
            'PS11': 'voiceapp',
        }
        return dtmf_codes.get(dtmf)

    def enabled(self):
        return os.path.isfile(self.pidfile)

    def enable(self):
        pid = str(os.getpid())
        logging.info('Process Id' + pid)
        with open(self.pidfile, 'w') as f:
            f.write(pid)

    def disable(self):
        if self.enabled():
            os.unlink(self.pidfile)
        if self.scheduler_status:
            self.scheduler.shutdown()

    def observer_mode(self):
        logging.info('Mode Observer')
        pub = Publisher(['text', 'voice'])

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
        self.voicesynthesizer.speech_it("Modo Planificador")

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
                self.voicesynthesizer.speech_it("Se ha activado el nodo, Proyecto NuupXe dice hasta pronto!")
                break

        self.disable()

    def writing_mode(self):
        logging.info('Mode Writing')

        while True:
            print(" Type any text to make use of Text to Speech infraestructure")
            x = input(" Type 'e' for exit: ")
            if x.lower() == 'e':
                self.disable()
                break
            else:
                self.voicesynthesizer.speech_it(x)
            time.sleep(1)

    def module_mode(self, module, dtmf=None):
        logging.info('Mode Module ' + module)

        if module == 'identification':
            from modules.identification import Identification
            Identification(self.voicesynthesizer).identify()
        elif module == 'date':
            from modules.clock import Clock
            Clock(self.voicesynthesizer).date()
        elif module == 'hour':
            from modules.clock import Clock
            Clock(self.voicesynthesizer).hour()
        elif module == 'clock':
            from modules.clock import Clock
            Clock(self.voicesynthesizer).hour()
        elif module == 'temperature':
            from modules.weather import Weather
            Weather(self.voicesynthesizer).weather_temperature()
        elif module == 'weather':
            from modules.weather import Weather
            Weather(self.voicesynthesizer).weather_report()
        elif module == 'alive':
            alive()
        elif module == 'aprstracker':
            from modules.aprstracker import AprsTracker
            AprsTracker(self.voicesynthesizer).localize()
        elif module == 'news':
            from modules.news import News
            News(self.voicesynthesizer).get_items()
        elif module == 'meteorology':
            from modules.meteorology import Meteorology
            Meteorology(self.voicesynthesizer).conagua_clima()
        elif module == 'selfie':
            from modules.selfie import Selfie
            Selfie(self.voicesynthesizer).get()
        elif module == 'audiocommandmanager':
            from modules.audiocommandmanager import AudioCommandManager
            AudioCommandManager(self.voicesynthesizer).listen()
        elif module == 'voiceapp':
            from modules.voiceapp import VoiceApp
            VoiceApp(self.voicesynthesizer).application()
        elif module == 'voicemail':
            from modules.voicemail import VoiceMail
            VoiceMail(self.voicesynthesizer).run(dtmf)
        elif module == 'wolframalpha':
            from modules.wolframalpha import WolframAlpha
            WolframAlpha(self.voicesynthesizer).ask()
        elif module == 'aprstt':
            from modules.aprstt import Aprstt
            Aprstt(self.voicesynthesizer).query(dtmf)
        elif module == 'seismology':
            from modules.seismology import Seismology
            Seismology(self.voicesynthesizer).SismologicoMX()
        elif module == 'morselearn':
            from learning.morseteacher import MorseTeacher
            MorseTeacher(self.voicesynthesizer).learn()
        elif module == 'morsecontest':
            from learning.morseteacher import MorseTeacher
            MorseTeacher(self.voicesynthesizer).contest()
        elif module == 'regulations':
            from modules.messages import Messages
            Messages(self.voicesynthesizer).readfile('learning/reglamentos.1')
        elif module == 'radioclub':
            from modules.messages import Messages
            Messages(self.voicesynthesizer).readfile('learning/arej.radioclubs')
        elif module == 'stations':
            from modules.messages import Messages
            Messages(self.voicesynthesizer).stations()
        elif module == 'sstv':
            from modules.sstv import SSTV
            SSTV(self.voicesynthesizer).decode()
        elif module == 'assistant':
            from modules.assistant import Assistant
            Assistant(self.voicesynthesizer).demo1()
        elif module == 'querymaster':
            from modules.querymaster import QueryMaster
            QueryMaster(self.voicesynthesizer).listen()
        elif module == 'voicemailer':
            from modules.voicemailer import VoiceMailer
            VoiceMailer(self.voicesynthesizer).attend(dtmf)
        else:
            self.voicesynthesizer.speech_it("No hemos implementado tu comando! Lo siento!")

        self.disable()

    def voice_mode(self, text):
        logging.info('Voice Mode')
        try:
            self.voicesynthesizer.speech_it(text)
        except (StopIteration, KeyboardInterrupt, SystemExit):
            pass

    def phonetic_mode(self, text):
        logging.info('Phonetic Mode')
        phonetic = Phonetic()
        try:
            text = ' '.join(phonetic.decode(text))
            self.voicesynthesizer.speech_it(text)
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
        self.scheduler.add_job(self.news.get_items, trigger=CronTrigger(month='*', day='*', hour='*/4', minute='0', second='0'))
        self.scheduler.add_job(self.meteorology.conagua_clima, trigger=CronTrigger(month='*', day='*', hour='*', minute='15', second='0'))
        self.scheduler.add_job(self.messages.stations, trigger=CronTrigger(month='*', day='*', hour='*/4', minute='0', second='0'))

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
