#!/usr/bin/python

import commands
import getopt
import signal
import sys
import thread
import time

from apscheduler.scheduler import Scheduler
from apscheduler.threadpool import ThreadPool

from core.voicesynthetizer import VoiceSynthetizer
from core.wolfram import Wolfram

from modules.assistant import Assistant
from modules.command import Command
from modules.clock import Clock
from modules.identification import Identification
from modules.messages import Messages
from modules.seismology import Seismology
from modules.weather import Weather

from learning.morseteacher import MorseTeacher
from learning.reglamentos import Reglamentos

class Cancun(object):

    def __init__(self, voicesynthetizer):

        commands.getstatusoutput("/home/irlp/scripts/off")

        self.voicesynthetizer = voicesynthetizer
        self.scheduler = Scheduler(misfire_grace_time=600, coalesce=True, threadpool=ThreadPool(max_threads=1))
        self.scheduler.start()

    def __del__(self):
        self.scheduler.shutdown()

    def timeout(self):
        print 'Cancun Timeout Function'

    def setup(self):
        self.assistant = Assistant(self.voicesynthetizer)
        self.command = Command(self.voicesynthetizer)
        self.clock = Clock(self.voicesynthetizer)
        self.identification = Identification(self.voicesynthetizer)
        self.reglamentos = Reglamentos(self.voicesynthetizer)
        self.messages = Messages(self.voicesynthetizer)
        self.morseteacher = MorseTeacher(self.voicesynthetizer)
        self.seismology = Seismology(self.voicesynthetizer)
        self.weather = Weather(self.voicesynthetizer)

        self.wolfram = Wolfram(self.voicesynthetizer)

    def module(self, module):

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
        elif module == 'command':
            self.command.execute()
        elif module == 'morselearn':
            self.morseteacher.learn()
        elif module == 'morsecontest':
            self.morseteacher.contest()
	elif module == 'regulations':
            self.reglamentos.read('learning/reglamentos.1')
        elif module == 'assistant':
            self.assistant.demo1()
        elif module == 'wolfram':
            self.wolfram.question('how many grams in kilograms')
        else:
            print 'Module not found! Please check its name...'
            sys.exit(1)

    def schedulejobs(self):
        self.scheduler.print_jobs()

    def schedule(self):

        # General Modules
        self.scheduler.add_interval_job(self.identification.identify, minutes=30)
        self.scheduler.add_interval_job(self.clock.date, minutes=30)
        self.scheduler.add_interval_job(self.clock.hour, minutes=30)
        self.scheduler.add_interval_job(self.seismology.SismologicoMX, minutes=60)
        self.scheduler.add_interval_job(self.weather.report, minutes=120)
        self.scheduler.add_interval_job(self.messages.stations, minutes=240)
        # self.scheduler.add_interval_job(self.command.execute, minutes=15)

	# Learning Modules, AREJ
        self.scheduler.add_cron_job(self.reglamentos.read,args=['learning/arej.radioclubs'],month='*',day_of_week='*',hour='7,11,17',minute ='00',second='0')

        # Learning Modules, Morse
        self.scheduler.add_cron_job(self.morseteacher.learn,month='*',day='*',hour='7,12,18',minute ='30',second='0')
        self.scheduler.add_cron_job(self.morseteacher.contest,month='*',day='*',hour='7,12,18',minute ='45',second='0')
        # self.scheduler.add_interval_job(self.morseteacher.goask, minutes=20)

        # Learning Modules, Reglamentos
        self.scheduler.add_cron_job(self.reglamentos.read,args=['learning/reglamentos.1'],month='*',day_of_week='mon,sat,sun',hour='8,13,19',minute ='00',second='0')
        self.scheduler.add_cron_job(self.reglamentos.read,args=['learning/reglamentos.2'],month='*',day_of_week='tue,sat,sun',hour='8,13,19',minute ='00',second='0')
        self.scheduler.add_cron_job(self.reglamentos.read,args=['learning/reglamentos.3'],month='*',day_of_week='wed,sat,sun',hour='8,13,19',minute ='00',second='0')
        self.scheduler.add_cron_job(self.reglamentos.read,args=['learning/reglamentos.4'],month='*',day_of_week='thu,sat,sun',hour='8,13,19',minute ='00',second='0')
        self.scheduler.add_cron_job(self.reglamentos.read,args=['learning/reglamentos.5'],month='*',day_of_week='fri,sat,sun',hour='8,13,19',minute ='00',second='0')

def main(argv):

    voicesynthetizer = VoiceSynthetizer("google", "spanish")

    try:
        opts, args = getopt.getopt(argv, "h:m:s", ["help", "module=", "scheduler"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    experimental = Cancun(voicesynthetizer)
    experimental.setup()

    for opt, arg in opts:

        if opt in ("-h", "--help"):
            sys.exit()

        elif opt in ("-m", "--module"):

            print "\n [" + time.ctime() + "] Cancun Project, Repeater Voice Services, Module Mode\n"
            experimental.module(arg)

        elif opt in ("-s", "--scheduler"):

            experimental.schedule()
            experimental.schedulejobs()

            # ToDo Someone speaking? Stop scheduler

            while True:
                print "\n [" + time.ctime() + "] Cancun Project, Repeater Voice Services, Scheduler Mode"
                print " Type 'jobs' to see the list of running modules"
                print " Type any text to make use of Text to Speech infraestructure"
                x = raw_input(" Type 'e' for exit: ")
                if x.lower() == 'jobs':
                    experimental.schedulejobs()
                elif x.lower() == 'e':
                    break;
                else:
                    voicesynthetizer.speechit(x)
                pass
        else:
            assert False, "unhandled option"

if __name__ == "__main__":

    main(sys.argv[1:])
