#!/usr/bin/python

import time
import sys

from apscheduler.scheduler import Scheduler
from apscheduler.threadpool import ThreadPool
from clock import Clock
from id import Identification
from messages import Messages
from twitterc import TwitterC
from voicesynthetizer import VoiceSynthetizer
from weather import Weather

sys.path.append('../learning')
from morseteacher import MorseTeacher
from reglamentos import Reglamentos

class Test(object):

    def __init__(self):
        self.voicesynthetizer = VoiceSynthetizer("espeak", "spanish")

    def __del__(self):
        pass

    def modules(self):
        self.clock = Clock(self.voicesynthetizer)
        self.id = Identification(self.voicesynthetizer)
        self.reglamentos = Reglamentos(self.voicesynthetizer)
        self.messages = Messages(self.voicesynthetizer)
        self.morseteacher = MorseTeacher(self.voicesynthetizer)
        #self.twitterc = TwitterC(self.voicesynthetizer)
        self.weather = Weather(self.voicesynthetizer)

	while True:
		self.id.identify()
		time.sleep(30)
		self.clock.date()
		time.sleep(30)
		self.clock.hour()
		time.sleep(30)
		#self.weather.report()
		#time.sleep(15)
		#self.twitterc.sismologicomx()
		#time.sleep(2)
		self.morseteacher.golearn()
		time.sleep(60)
		self.morseteacher.gocompete()
		time.sleep(60)
		self.messages.stations()
		time.sleep(60)
		self.reglamentos.read("../learning/reglamentos.1")
		time.sleep(120)
		self.reglamentos.read("../learning/reglamentos.2")
		time.sleep(120)
		self.reglamentos.read("../learning/reglamentos.3")
		time.sleep(120)
		self.reglamentos.read("../learning/reglamentos.4")
		time.sleep(120)
		self.reglamentos.read("../learning/reglamentos.5")
		time.sleep(120)

if __name__ == "__main__":

    mytest = Test()
    mytest.modules()
