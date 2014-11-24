#!/usr/bin/python

import argparse
import commands
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
from core.wolfram import Wolfram

from learning.morseteacher import MorseTeacher

from modules.assistant import Assistant
from modules.aprstt import Aprstt
from modules.command import Command
from modules.commandtop import CommandTop
from modules.clock import Clock
from modules.identification import Identification
from modules.messages import Messages
from modules.meteorology import Meteorology
from modules.news import News
from modules.seismology import Seismology
from modules.tracker import Tracker
from modules.voicemail import VoiceMail
from modules.weather import Weather

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

        self.aprstt = Aprstt(self.voicesynthetizer)
        self.assistant = Assistant(self.voicesynthetizer)
        self.command = Command(self.voicesynthetizer)
        self.commandtop = CommandTop(self.voicesynthetizer)
        self.clock = Clock(self.voicesynthetizer)
        self.identification = Identification(self.voicesynthetizer)
        self.messages = Messages(self.voicesynthetizer)
        self.meteorology = Meteorology(self.voicesynthetizer)
        self.morseteacher = MorseTeacher(self.voicesynthetizer)
        self.news = News(self.voicesynthetizer)
        self.tracker = Tracker(self.voicesynthetizer)
        self.seismology = Seismology(self.voicesynthetizer)
        self.voicemail = VoiceMail(self.voicesynthetizer)
        self.weather = Weather(self.voicesynthetizer)
        self.wolfram = Wolfram(self.voicesynthetizer)

    def dtmf_setup(self,dtmf):
        dtmf_codes = {
        'P1': 'identification',
        'P2': 'date',
        'P3': 'hour',
        'P4': 'weather',
        'P5': 'seismology',
        'P6': 'stations'
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

    def scheduler_mode(self, action):

        print "[" + time.ctime() + "] Scheduler Mode\n"
        self.voicesynthetizer.speechit("Modo Planificador")

        self.scheduler = Scheduler(misfire_grace_time=600, coalesce=True, threadpool=ThreadPool(max_threads=1))
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

        print "[" + time.ctime() + "] Writing Mode\n"
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

        print "[" + time.ctime() + "] Module Mode\n"

        if module == 'assistant':
            self.assistant.demo1()
        elif module == 'command':
            self.command.execute()
        elif module == 'date':
            self.clock.date()
        elif module == 'hour':
            self.clock.hour()
        elif module == 'identification':
            self.identification.identify()
        elif module == 'meteorology':
            self.meteorology.conagua_clima()
        elif module == 'morselearn':
            self.morseteacher.learn()
        elif module == 'morsecontest':
            self.morseteacher.contest()
        elif module == 'news':
            self.news.getitems()
	elif module == 'regulations':
            self.messages.readfile('learning/reglamentos.1')
	elif module == 'radioclub':
            self.messages.readfile('learning/arej.radioclubs')
        elif module == 'seismology':
            self.seismology.SismologicoMX()
        elif module == 'stations':
            self.messages.stations()
        elif module == 'tracker':
            self.tracker.query()
        elif module == 'vm':
            self.voicemail.run(dtmf)
        elif module == 'weather':
            self.weather.report()
        elif module == 'wolfram':
            self.wolfram.question('how many grams in kilograms')
        elif module == 'aprstt':
            self.aprstt.query(dtmf)
        elif module == 'top':
            self.commandtop.execute()
        else:
            print 'Module not found! Please check its name...\n'

        self.disable()

    def random_mode(self):

        print "[" + time.ctime() + "] Random Mode\n"
        self.voicesynthetizer.speechit("Modo Aleatorio")

        while True:
            modules = ['identification','date','hour', 'weather', 'sismology', 'stations', 'tracker', 'wolfram', 'top']
            random_module = modules[int(random.random() * len(modules))]
            random_time = random.randint(15,30)
            time.sleep(random_time)

            if self.irlp.active():
                time.sleep(5)
                self.irlp.busy()
                self.voicesynthetizer.speechit("Se ha activado el nodo, Proyecto Cancun se despide, hasta pronto!")
                break

            self.module_mode(random_module, 'None')

        self.disable()

    def schedule_print(self):
        self.scheduler.print_jobs()

    def schedule(self):

        # Production Modules
        self.scheduler.add_interval_job(self.commandtop.execute, minutes=15)
        self.scheduler.add_interval_job(self.identification.identify, minutes=30)
        self.scheduler.add_interval_job(self.clock.date, minutes=30)
        self.scheduler.add_interval_job(self.clock.hour, minutes=30)
        self.scheduler.add_interval_job(self.seismology.SismologicoMX, minutes=60)
        #self.scheduler.add_interval_job(self.news.getitems, minutes=60)
        self.scheduler.add_interval_job(self.weather.report, minutes=120)
        self.scheduler.add_interval_job(self.messages.stations, minutes=240)
        # self.scheduler.add_interval_job(self.command.execute, minutes=15)

	# Learning Modules, AREJ
        self.scheduler.add_cron_job(self.messages.readfile,args=['learning/arej.radioclubs'],month='*',day_of_week='*',hour='7,11,17',minute ='00',second='0')

        # Learning Modules, Morse
        self.scheduler.add_cron_job(self.morseteacher.learn,month='*',day='*',hour='7,12,18',minute ='30',second='0')
        self.scheduler.add_cron_job(self.morseteacher.contest,month='*',day='*',hour='7,12,18',minute ='45',second='0')
        # self.scheduler.add_interval_job(self.morseteacher.goask, minutes=20)

        # Learning Modules, Reglamentos
        self.scheduler.add_cron_job(self.messages.readfile,args=['learning/reglamentos.1'],month='*',day_of_week='mon,sat,sun',hour='8,13,19',minute ='00',second='0')
        self.scheduler.add_cron_job(self.messages.readfile,args=['learning/reglamentos.2'],month='*',day_of_week='tue,sat,sun',hour='8,13,19',minute ='00',second='0')
        self.scheduler.add_cron_job(self.messages.readfile,args=['learning/reglamentos.3'],month='*',day_of_week='wed,sat,sun',hour='8,13,19',minute ='00',second='0')
        self.scheduler.add_cron_job(self.messages.readfile,args=['learning/reglamentos.4'],month='*',day_of_week='thu,sat,sun',hour='8,13,19',minute ='00',second='0')
        self.scheduler.add_cron_job(self.messages.readfile,args=['learning/reglamentos.5'],month='*',day_of_week='fri,sat,sun',hour='8,13,19',minute ='00',second='0')

def set_exit_handler(func):
    signal.signal(signal.SIGTERM, func)

def on_exit(sig, func=None):
    print "exit handler triggered"
    sys.exit(1)

def main(argv):

    irlp = Irlp()
    voicesynthetizer = VoiceSynthetizer("google", "spanish")

    parser = argparse.ArgumentParser(description='Cancun Project, Voice Services Experimental Project')
    parser.add_argument('-m', '--module', help='Module Mode')
    parser.add_argument('-s', '--scheduler', help='Scheduler mode')
    parser.add_argument('-w', '--writing', help='Writing Mode')
    parser.add_argument('-r', '--random', help='Random Mode')
    parser.add_argument('-d', '--dtmf', help='DMTF Code')
    args = parser.parse_args()

    if irlp.active():
        voicesynthetizer.speechit("Nodo activo, no podemos iniciar Proyecto Cancun")
        sys.exit(1)

    experimental = Cancun(voicesynthetizer, irlp)

    if (args.module or (args.scheduler == 'start' or args.random == 'start')) and experimental.enabled():
        voicesynthetizer.speechit("Proyecto Cancun ya habilitado, no podemos iniciar otra instancia")
        sys.exit(1)

    if args.scheduler == 'stop' or args.random == 'stop' and not experimental.enabled():
        voicesynthetizer.speechit("Proyecto Cancun deshabilitado")
        status, output = commands.getstatusoutput('./cancun.sh stop')
        sys.exit(1)

    if args.scheduler == 'stop' or args.random == 'stop' and experimental.enabled():
        voicesynthetizer.speechit("Deshabilitando Proyecto Cancun, hasta pronto!")
        status, output = commands.getstatusoutput('./cancun.sh stop')
        sys.exit(1)

    experimental.enable()
    experimental.modules_setup()

    print "[" + time.ctime() + "] Cancun Project, Repeater Voice Services"

    if args.module:
        experimental.module_mode(args.module, args.dtmf)

    if args.scheduler:
        experimental.scheduler_mode()

    if args.writing:
        experimental.writing_mode()

    if args.random:
        experimental.random_mode()

    if args.dtmf:
        #voicesynthetizer.speechit("Modulo Experimental")
        if len(args.dtmf) == 2:
            module = experimental.dtmf_setup(args.dtmf)
            experimental.module_mode(module, args.dtmf)
        else:
            experimental.module_mode('aprstt', args.dtmf)

    experimental.disable()

if __name__ == "__main__":

    main(sys.argv[1:])
