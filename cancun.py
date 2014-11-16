#!/usr/bin/python

import argparse
import commands
import os
import signal
import sys
import thread
import time

from apscheduler.scheduler import Scheduler
from apscheduler.threadpool import ThreadPool

from core.irlp import Irlp
from core.voicesynthetizer import VoiceSynthetizer
from core.wolfram import Wolfram

from modules.voicemail import VoiceMail

from modules.assistant import Assistant
from modules.command import Command
from modules.clock import Clock
from modules.identification import Identification
from modules.messages import Messages
from modules.meteorology import Meteorology
from modules.news import News
from modules.seismology import Seismology
from modules.weather import Weather

from learning.morseteacher import MorseTeacher

class Cancun(object):

    def __init__(self, voicesynthetizer):

        self.voicesynthetizer = voicesynthetizer
        self.scheduler = Scheduler(misfire_grace_time=600, coalesce=True, threadpool=ThreadPool(max_threads=1))
        self.scheduler.start()

    def __del__(self):
        self.scheduler.shutdown()

    def timeout(self):
        print 'Cancun Timeout Function'

    def check(self):
        pid = str(os.getpid())
        pidfile = "/tmp/cancun.pid"

        if os.path.isfile(pidfile):
            self.voicesynthetizer.speechit("Proyecto Cancun ya habilitado, no podemos iniciar otra instancia")
            self.voicesynthetizer.speechit("Deshabilita o intenta mas tarde")
            sys.exit()
        else:
            file(pidfile, 'w').write(pid)
        return pidfile

    def setup(self):
        self.assistant = Assistant(self.voicesynthetizer)
        self.command = Command(self.voicesynthetizer)
        self.clock = Clock(self.voicesynthetizer)
        self.identification = Identification(self.voicesynthetizer)
        self.messages = Messages(self.voicesynthetizer)
        self.meteorology = Meteorology(self.voicesynthetizer)
        self.morseteacher = MorseTeacher(self.voicesynthetizer)
        self.news = News(self.voicesynthetizer)
        self.seismology = Seismology(self.voicesynthetizer)
        self.weather = Weather(self.voicesynthetizer)

        self.wolfram = Wolfram(self.voicesynthetizer)

        self.voicemail = VoiceMail(self.voicesynthetizer)

    def module(self, module, dtmf):

        print dtmf

        if module == 'identification':
            self.identification.identify()
        elif module == 'hour':
            self.clock.hour()
        elif module == 'date':
            self.clock.date()
        elif module == 'weather':
            self.weather.report()
        elif module == 'seismology':
            self.seismology.SismologicoMX()
        elif module == 'stations':
            self.messages.stations()
        elif module == 'meteorology':
            self.meteorology.conagua_clima()
        elif module == 'command':
            self.command.execute()
        elif module == 'morselearn':
            self.morseteacher.learn()
        elif module == 'morsecontest':
            self.morseteacher.contest()
	elif module == 'regulations':
            self.messages.readfile('learning/reglamentos.1')
	elif module == 'radioclub':
            self.messages.readfile('learning/arej.radioclubs')
        elif module == 'assistant':
            self.assistant.demo1()
        elif module == 'wolfram':
            self.wolfram.question('how many grams in kilograms')
        elif module == 'news':
            self.news.getitems()
        elif module == 'vm':
            self.voicemail.run(dtmf)
        else:
            print 'Module not found! Please check its name...'

    def schedulejobs(self):
        self.scheduler.print_jobs()

    def schedule(self):

        # General Modules
        self.scheduler.add_interval_job(self.identification.identify, minutes=30)
        self.scheduler.add_interval_job(self.clock.date, minutes=30)
        self.scheduler.add_interval_job(self.clock.hour, minutes=30)
        self.scheduler.add_interval_job(self.seismology.SismologicoMX, minutes=60)
        self.scheduler.add_interval_job(self.news.getitems, minutes=60)
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

def usage():
   print '\nProyecto Cancun Options: help, module <name>, scheduler\n'

def main(argv):

    irlp = Irlp()

    parser = argparse.ArgumentParser(description='Cancun Project, Voice Services Experiemental Project')
    parser.add_argument('-m', '--module', help='Module Mode')
    parser.add_argument('-s', '--scheduler', help='Scheduler mode')
    parser.add_argument('-l', '--live', help='Live Mode')
    parser.add_argument('-d', '--dtmf', help='DMTF Code')
    args = parser.parse_args()

    voicesynthetizer = VoiceSynthetizer("google", "spanish")

    if irlp.active():
        voicesynthetizer.speechit("Nodo activo, no podemos iniciar Proyecto Cancun")
        sys.exit(2)

    experimental = Cancun(voicesynthetizer)
    pidfile = experimental.check()
    experimental.setup()

    print "[" + time.ctime() + "] Cancun Project, Repeater Voice Services"
    voicesynthetizer.speechit("Proyecto Cancun")

    if args.module:

        print "[" + time.ctime() + "] Module Mode"
        experimental.module(args.module, args.dtmf)

    if args.scheduler:

        print "[" + time.ctime() + "] Scheduler Mode\n"
        voicesynthetizer.speechit("Modo Planificador Habilitado")
        experimental.schedule()
        experimental.schedulejobs()

        while True:
             experimental.schedulejobs()
             time.sleep(5)
             if irlp.active():
                  irlp.idle()
                  voicesynthetizer.speechit("Se ha activado el nodo, Proyecto Cancun se despide, hasta pronto!")
                  break
             pass

    if args.live:

        print "[" + time.ctime() + "] Live Mode"
        voicesynthetizer.speechit("Modo Escritura Habilitado")

        while True:
            print " Type any text to make use of Text to Speech infraestructure"
            x = raw_input(" Type 'e' for exit: ")
            if x.lower() == 'e':
                break;
            else:
                voicesynthetizer.speechit(x)
            time.sleep(1)
            pass

    os.unlink(pidfile)

if __name__ == "__main__":

    main(sys.argv[1:])
