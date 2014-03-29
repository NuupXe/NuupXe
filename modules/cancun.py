#!/usr/bin/python

import time
import sys

from apscheduler.scheduler import Scheduler
from apscheduler.threadpool import ThreadPool
from clock import Clock
from id import Identification
from messages import Messages
from voicesynthetizer import VoiceSynthetizer
from weather import Weather

sys.path.append('../learning')
from morseteacher import MorseTeacher
from fmre import FmreTeacher

class Cancun():

	def __init__(self):
		self.voicesynthetizer = VoiceSynthetizer("google", "spanish")
		self.scheduler = Scheduler(misfire_grace_time=120, coalesce=True, threadpool=ThreadPool(max_threads=1))
		self.scheduler.start()

	def __del__(self):
		self.scheduler.shutdown()

	def modules(self):
		self.clock = Clock(self.voicesynthetizer)
		self.id = Identification(self.voicesynthetizer)
		self.fmreteacher = FmreTeacher(self.voicesynthetizer)
		self.messages = Messages(self.voicesynthetizer)
		self.morseteacher = MorseTeacher(self.voicesynthetizer)
		self.weather = Weather(self.voicesynthetizer)

	def show(self):
		self.scheduler.print_jobs()

	def schedule(self):
		# General Modules
		self.scheduler.add_interval_job(self.id.identify, minutes=15)
		self.scheduler.add_interval_job(self.clock.date, minutes=60)
		self.scheduler.add_interval_job(self.clock.hour, minutes=60)
		self.scheduler.add_interval_job(self.weather.report, minutes=120)
		self.scheduler.add_interval_job(self.messages.repeaters, minutes=120)

		# Learning Modules, Morse
		self.scheduler.add_cron_job(self.morseteacher.golearn,month='*',day='*',hour='7,12,18',minute ='00',second='0')
		self.scheduler.add_cron_job(self.morseteacher.gocompete,month='*',day='*',hour='7,12,18',minute ='43',second='0')

		# Learning Modules, FMRE
		self.scheduler.add_cron_job(self.fmreteacher.read,args=['../learning/fmre.reglamento.1'],month='*',day_of_week='mon',hour='8,13,19',minute ='00',second='0')
		self.scheduler.add_cron_job(self.fmreteacher.read,args=['../learning/fmre.reglamento.2'],month='*',day_of_week='tue',hour='8,13,19',minute ='00',second='0')
		self.scheduler.add_cron_job(self.fmreteacher.read,args=['../learning/fmre.reglamento.3'],month='*',day_of_week='wed',hour='8,13,19',minute ='00',second='0')
		self.scheduler.add_cron_job(self.fmreteacher.read,args=['../learning/fmre.reglamento.4'],month='*',day_of_week='thu',hour='8,13,19',minute ='00',second='0')
		self.scheduler.add_cron_job(self.fmreteacher.read,args=['../learning/fmre.reglamento.5'],month='*',day_of_week='fri',hour='8,13,19',minute ='00',second='0')

if __name__ == "__main__":

	mytest = Cancun()
	mytest.modules()
	mytest.schedule()

	while True:
		print ' [' + time.ctime() + '] ' + 'Cancun Project Alive'
		mytest.show()
		time.sleep(60)
