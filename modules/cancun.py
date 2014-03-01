#!/usr/bin/python

import time
import sys

from apscheduler.scheduler import Scheduler
from clock import Clock
from id import Identification
from voicesynthetizer import VoiceSynthetizer

class Cancun():

	def __init__(self):

		self.voicesynthetizer = VoiceSynthetizer("festival", "spanish")
		self.scheduler = Scheduler()
		self.scheduler.start()

	def modules(self):
		self.clock = Clock(self.voicesynthetizer)
		self.id = Identification(self.voicesynthetizer)

	def schedule(self):
		self.scheduler.add_cron_job(self.id.identify,month='*',day='*',hour='*',minute ='*',second='15')
		self.scheduler.add_cron_job(self.clock.hour,month='*',day='*',hour='*',minute ='*',second='0')
		self.scheduler.add_cron_job(self.clock.date,month='*',day='*',hour='*',minute ='59',second='0')
		self.scheduler.print_jobs()

if __name__ == "__main__":

	mytest = Cancun()
	mytest.modules()
	mytest.schedule()

	while True:
		print 'Cancun Project Alive'
		time.sleep(60)

