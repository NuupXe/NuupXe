#!/usr/bin/python

import time
import signal
import sys

from apscheduler.scheduler import Scheduler
from apscheduler.threadpool import ThreadPool

from core.voicesynthetizer import VoiceSynthetizer

from modules.clock import Clock
from modules.identification import Identification
from modules.messages import Messages
from modules.twitterc import TwitterC
from modules.weather import Weather

from learning.morseteacher import MorseTeacher
from learning.reglamentos import Reglamentos

class Cancun(object):

    def __init__(self):
        self.voicesynthetizer = VoiceSynthetizer("google", "spanish")
        self.scheduler = Scheduler(misfire_grace_time=240, coalesce=True, threadpool=ThreadPool(max_threads=1))
        self.scheduler.start()

    def __del__(self):
        self.scheduler.shutdown()

    def timeout(self):
        print 'Cancun timeout function'

    def modules(self):
        self.clock = Clock(self.voicesynthetizer)
        self.identification = Identification(self.voicesynthetizer)
        self.reglamentos = Reglamentos(self.voicesynthetizer)
        self.messages = Messages(self.voicesynthetizer)
        self.morseteacher = MorseTeacher(self.voicesynthetizer)
        self.twitterc = TwitterC(self.voicesynthetizer)
        self.weather = Weather(self.voicesynthetizer)

    def show(self):
        self.scheduler.print_jobs()

    def schedule(self):

        # Core
        # tbi

        # General Modules
        self.scheduler.add_interval_job(self.identification.identify, minutes=10)
        self.scheduler.add_interval_job(self.clock.date, minutes=30)
        self.scheduler.add_interval_job(self.clock.hour, minutes=30)
        self.scheduler.add_interval_job(self.twitterc.sismologicomx, minutes=60)
        self.scheduler.add_interval_job(self.weather.report, minutes=60)
        self.scheduler.add_interval_job(self.messages.stations, minutes=150)

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

    mytest = Cancun()
    mytest.modules()
    mytest.schedule()

    while True:
        print ' [' + time.ctime() + '] ' + 'Cancun Project Alive'
        mytest.show()
        time.sleep(1)
        signal.pause()
