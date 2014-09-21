#!/usr/bin/python

import time
import signal
import sys
import thread

from apscheduler.scheduler import Scheduler
from apscheduler.threadpool import ThreadPool

from core.voicesynthetizer import VoiceSynthetizer

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
        self.voicesynthetizer = voicesynthetizer
        self.scheduler = Scheduler(misfire_grace_time=600, coalesce=True, threadpool=ThreadPool(max_threads=1))
        self.scheduler.start()

    def __del__(self):
        self.scheduler.shutdown()

    def timeout(self):
        print 'Cancun timeout function'

    def modules(self):
        self.command = Command(self.voicesynthetizer)
        self.clock = Clock(self.voicesynthetizer)
        self.identification = Identification(self.voicesynthetizer)
        self.reglamentos = Reglamentos(self.voicesynthetizer)
        self.messages = Messages(self.voicesynthetizer)
        self.morseteacher = MorseTeacher(self.voicesynthetizer)
        self.seismology = Seismology(self.voicesynthetizer)
        self.weather = Weather(self.voicesynthetizer)

    def show(self):
        self.scheduler.print_jobs()

    def schedule(self):

        # General Modules
        # self.scheduler.add_interval_job(self.command.execute, minutes=15)
        # self.scheduler.add_interval_job(self.morseteacher.goask, minutes=20)
        self.scheduler.add_interval_job(self.identification.identify, minutes=30)
        self.scheduler.add_interval_job(self.clock.date, minutes=5)
        self.scheduler.add_interval_job(self.clock.hour, minutes=5)
        self.scheduler.add_interval_job(self.seismology.SismologicoMX, minutes=60)
        self.scheduler.add_interval_job(self.weather.report, minutes=60)
        self.scheduler.add_interval_job(self.messages.stations, minutes=120)

        # Learning Modules, Morse
        self.scheduler.add_cron_job(self.morseteacher.golearn,month='*',day='*',hour='7,12,18',minute ='00',second='0')
        self.scheduler.add_cron_job(self.morseteacher.gocompete,month='*',day='*',hour='7,12,18',minute ='15',second='0')

        # Learning Modules, Reglamentos
        self.scheduler.add_cron_job(self.reglamentos.read,args=['learning/reglamentos.1'],month='*',day_of_week='mon,sat,sun',hour='8,13,19',minute ='00',second='0')
        self.scheduler.add_cron_job(self.reglamentos.read,args=['learning/reglamentos.2'],month='*',day_of_week='tue,sat,sun',hour='8,13,19',minute ='00',second='0')
        self.scheduler.add_cron_job(self.reglamentos.read,args=['learning/reglamentos.3'],month='*',day_of_week='wed,sat,sun',hour='8,13,19',minute ='00',second='0')
        self.scheduler.add_cron_job(self.reglamentos.read,args=['learning/reglamentos.4'],month='*',day_of_week='thu,sat,sun',hour='8,13,19',minute ='00',second='0')
        self.scheduler.add_cron_job(self.reglamentos.read,args=['learning/reglamentos.5'],month='*',day_of_week='fri,sat,sun',hour='8,13,19',minute ='00',second='0')

if __name__ == "__main__":

    voicesynthetizer = VoiceSynthetizer("google", "spanish")

    experimental = Cancun(voicesynthetizer)
    experimental.modules()
    experimental.schedule()
    experimental.show()

    while True:
        print "\n [" + time.ctime() + "] Cancun Project, Repeater Voice Services"
        print " Type 'jobs' to see the list of running modules"
        print " Type any text to make use of Text to Speech infraestructure"
        x = raw_input(" Type 'e' for exit: ")
        if x.lower() == 'jobs':
            experimental.show()
        elif x.lower() == 'e':
            break;
        else:
            voicesynthetizer.speechit(x)
	pass

