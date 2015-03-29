#!/usr/bin/python

import argparse
import commands
import logging
import os
import random
import signal
import sys
import thread
import time

from apscheduler.scheduler import Scheduler
from apscheduler.threadpool import ThreadPool

from core.irlp import Irlp
from core.voicesynthetizer import VoiceSynthetizer

# Production

from modules.alive import Alive
from modules.aprstracker import AprsTracker
from modules.aprstt import Aprstt
from modules.clock import Clock
from modules.identification import Identification
from modules.selfie import Selfie
from modules.voicecommand import VoiceCommand
from modules.weather import Weather
from modules.wolframalpha import WolframAlpha

# Experimental

from modules.assistant import Assistant
from modules.messages import Messages
from modules.meteorology import Meteorology
from learning.morseteacher import MorseTeacher
from modules.news import News
from modules.seismology import Seismology
from modules.voicemail import VoiceMail
from modules.voiceexperimental import VoiceExperimental

class Cancun(object):

    def __init__(self, voicesynthetizer, irlp):

        self.irlp = irlp
        self.voicesynthetizer = voicesynthetizer
        self.pidfile = None
        self.scheduler_status = False
        self.pidfile = "/tmp/cancun.pid"

    def __del__(self):
        pass

    def modules_setup(self):

        # Production Modules
        self.alive = Alive()
        self.aprstracker = AprsTracker(self.voicesynthetizer)
        self.aprstt = Aprstt(self.voicesynthetizer)
        self.clock = Clock(self.voicesynthetizer)
        self.identification = Identification(self.voicesynthetizer)
        self.meteorology = Meteorology(self.voicesynthetizer)
        self.news = News(self.voicesynthetizer)
        self.selfie = Selfie(self.voicesynthetizer)
        self.voicecommand = VoiceCommand(self.voicesynthetizer)
        self.voiceexperimental = VoiceExperimental(self.voicesynthetizer)
        self.weather = Weather(self.voicesynthetizer)
        self.wolframalpha = WolframAlpha(self.voicesynthetizer)

        # Experimental Modules
        self.assistant = Assistant(self.voicesynthetizer)
        self.messages = Messages(self.voicesynthetizer)
        self.morseteacher = MorseTeacher(self.voicesynthetizer)
        self.seismology = Seismology(self.voicesynthetizer)
        self.voicemail = VoiceMail(self.voicesynthetizer)

    def dtmf_setup(self,dtmf):
        dtmf_codes = {
        'PS0': 'alive',
        'PS1': 'aprstracker',
        'PS2': 'news',
        'PS3': 'meteorology',
        'PS4': 'seismology',
        'PS5': 'selfie',
        'PS6': 'voicecommand',
        'PS7': 'voiceexperimental',
        'PS8': 'wolframalpha'
        }
        return dtmf_codes.get(dtmf)

    def enabled(self):
        return os.path.isfile(self.pidfile)

    def enable(self):

        pid = str(os.getpid())
        file(self.pidfile, 'w').write(pid)

    def disable(self):

        if self.enabled():
            os.unlink(self.pidfile)
        if self.scheduler_status:
            self.scheduler.shutdown()

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
                self.voicesynthetizer.speechit("Se ha activado el nodo, Proyecto Cancun se despide, hasta pronto!")
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

    def module_mode(self, module, dtmf):

        logging.info('Mode Module')

        # Custom Decode Activated Modules

        if module == 'identification':
            self.identification.identify()
        elif module == 'date':
            self.clock.date()
        elif module == 'hour':
            self.clock.hour()
        elif module == 'weather':
            self.weather.report()

        # PS Activated Modules

        elif module == 'alive':
            self.alive.report()
        elif module == 'aprstracker':
            self.aprstracker.query()
        elif module == 'news':
            self.news.getitems()
        elif module == 'meteorology':
            self.meteorology.conagua_clima()
        elif module == 'selfie':
            self.selfie.get()
        elif module == 'voicecommand':
            self.voicecommand.listen()
        elif module == 'wolframalpha':
            self.wolframalpha.ask()
        elif module == 'voiceexperimental':
            self.voiceexperimental.listen()

        # SS Activated Modules

        # Experimental Modules

        elif module == 'aprstt':
            self.aprstt.query(dtmf)
        elif module == 'seismology':
            self.seismology.SismologicoMX()
        elif module == 'morselearn':
            self.morseteacher.learn()
        elif module == 'morsecontest'	:
            self.morseteacher.contest()
	elif module == 'regulations':
            self.messages.readfile('learning/reglamentos.1')
	elif module == 'radioclub':
            self.messages.readfile('learning/arej.radioclubs')
        elif module == 'stations':
            self.messages.stations()
        elif module == 'voicemail':
            self.voicemail.run(dtmf)
        elif module == 'assistant':
            self.assistant.demo1()
        elif module == 'voicebackground':
            self.voicecommand.background()
        else:
            print 'Module not found! Please check its name...\n'

        self.disable()

    def schedule_print(self):
        self.scheduler.print_jobs()

    def schedule(self):

        # Production Modules
        self.scheduler.add_interval_job(self.alive.report, minutes=60)
        self.scheduler.add_cron_job(self.clock.date,month='*',day_of_week='*',hour='6,12,22',minute ='00',second='0')
        self.scheduler.add_interval_job(self.clock.hour, minutes=15)
        self.scheduler.add_interval_job(self.identification.identify, minutes=30)
        self.scheduler.add_cron_job(self.selfie.get,month='*',day_of_week='*',hour='6,12,22',minute ='00',second='0')
        self.scheduler.add_interval_job(self.weather.report, minutes=120)

        # Experimental Modules
        self.scheduler.add_interval_job(self.seismology.SismologicoMX, minutes=120)
        self.scheduler.add_interval_job(self.news.getitems, minutes=120)
        self.scheduler.add_interval_job(self.meteorology.conagua_clima, minutes=120)
        self.scheduler.add_interval_job(self.messages.stations, minutes=240)

	# Learning Modules, AREJ
        self.scheduler.add_cron_job(self.messages.readfile,args=['learning/arej.radioclubs'],month='*',day_of_week='*',hour='7,12,17',minute ='00',second='0')

        # Learning Modules, Morse
        self.scheduler.add_cron_job(self.morseteacher.learn,month='*',day='*',hour='7,12,17',minute ='30',second='0')
        self.scheduler.add_cron_job(self.morseteacher.contest,month='*',day='*',hour='7,12,17',minute ='45',second='0')

        # Learning Modules, Reglamentos
        self.scheduler.add_cron_job(self.messages.readfile,args=['learning/reglamentos.1'],month='*',day_of_week='mon',hour='8,13,18',minute ='00',second='0')
        self.scheduler.add_cron_job(self.messages.readfile,args=['learning/reglamentos.2'],month='*',day_of_week='tue',hour='8,13,18',minute ='00',second='0')
        self.scheduler.add_cron_job(self.messages.readfile,args=['learning/reglamentos.3'],month='*',day_of_week='wed',hour='8,13,18',minute ='00',second='0')
        self.scheduler.add_cron_job(self.messages.readfile,args=['learning/reglamentos.4'],month='*',day_of_week='thu',hour='8,13,18',minute ='00',second='0')
        self.scheduler.add_cron_job(self.messages.readfile,args=['learning/reglamentos.5'],month='*',day_of_week='fri',hour='8,13,18',minute ='00',second='0')

def set_exit_handler(func):
    signal.signal(signal.SIGTERM, func)

def on_exit(sig, func=None):
    print "exit handler triggered"
    sys.exit(1)

def main(argv):

    logging.basicConfig(filename='output/cancun.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

    irlp = Irlp()
    voicesynthetizer = VoiceSynthetizer("google", "spanish")

    parser = argparse.ArgumentParser(description='Cancun Project, Voice Services Experimental Project')
    parser.add_argument('-m', '--module', help='Module Mode')
    parser.add_argument('-s', '--server', help='Server mode')
    parser.add_argument('-d', '--dtmf', help='DMTF Code')
    args = parser.parse_args()

    if irlp.active():
        logging.info("Nodo activo, no podemos iniciar Proyecto Cancun")
        sys.exit(0)

    experimental = Cancun(voicesynthetizer, irlp)

    if (args.module or args.server) and experimental.enabled():
        voicesynthetizer.speechit("Proyecto Cancun ya habilitado, no podemos iniciar otra instancia")
        sys.exit(1)

    if args.server == 'stop' and not experimental.enabled():
        voicesynthetizer.speechit("Proyecto Cancun deshabilitado")
        status, output = commands.getstatusoutput('./cancun.sh stop')
        sys.exit(1)

    if args.server == 'stop' and experimental.enabled():
        voicesynthetizer.speechit("Deshabilitando Proyecto Cancun, hasta pronto!")
        status, output = commands.getstatusoutput('./cancun.sh stop')
        sys.exit(1)

    experimental.enable()
    experimental.modules_setup()

    if args.module:
        experimental.module_mode(args.module, args.dtmf)

    elif args.server == 'scheduler':
        experimental.scheduler_mode()

    elif args.server == 'writing':
        experimental.writing_mode()

    elif args.dtmf:
        logging.info(args.dtmf)
        if len(args.dtmf) == 3:
            module = experimental.dtmf_setup(args.dtmf)
            experimental.module_mode(module, args.dtmf)
        elif len(args.dtmf) > 10:
            experimental.module_mode('aprstt', args.dtmf)

    experimental.disable()

if __name__ == "__main__":

    main(sys.argv[1:])
