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

class Cancun():

	def __init__(self):
		self.voicesynthetizer = VoiceSynthetizer("festival", "spanish")
		self.scheduler = Scheduler(misfire_grace_time=120, coalesce=True, threadpool=ThreadPool(max_threads=1))
		self.scheduler.start()

	def __del__(self):
		self.scheduler.shutdown()

	def modules(self):
		self.clock = Clock(self.voicesynthetizer)
		self.id = Identification(self.voicesynthetizer)
		self.messages = Messages()
		self.morseteacher = MorseTeacher()
		self.weather = Weather()

	def schedule(self):
		#self.scheduler.add_cron_job(self.id.identify,month='*',day='*',hour='*',minute ='0',second='0')
		#self.scheduler.add_cron_job(self.clock.hour,month='*',day='*',hour='*',minute ='0',second='0')
		#self.scheduler.add_cron_job(self.clock.date,month='*',day='*',hour='*',minute ='0',second='0')
		#self.scheduler.add_cron_job(self.morseteacher.go,month='*',day='*',hour='*',minute ='0-30',second='0')
		
		self.scheduler.add_interval_job(self.id.identify, minutes=5)
		self.scheduler.add_interval_job(self.clock.hour, minutes=5)
		self.scheduler.add_interval_job(self.clock.date, minutes=10)
		self.scheduler.add_interval_job(self.weather.report, minutes=10)
		self.scheduler.add_interval_job(self.messages.repeaters, minutes=10)
		self.scheduler.add_interval_job(self.morseteacher.golearn, minutes=30)

		self.scheduler.print_jobs()

if __name__ == "__main__":

	mytest = Cancun()
	mytest.modules()
	mytest.schedule()

	while True:
		print 'Cancun Project Alive'
		time.sleep(60)
