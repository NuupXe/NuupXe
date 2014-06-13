#!/usr/bin/python

import time
import sys

from apscheduler.scheduler import Scheduler
from apscheduler.threadpool import ThreadPool

from core.voicesynthetizer import VoiceSynthetizer

from modules.caudio import Caudio
from modules.clock import Clock
from modules.id import Identification
from modules.messages import Messages
from modules.twitterc import TwitterC
from modules.voicecommands import VoiceCommands
from modules.weather import Weather

from learning.morseteacher import MorseTeacher
from learning.reglamentos import Reglamentos

class CancunIrlp(object):

    def __init__(self):

        self.voicesynthetizer = VoiceSynthetizer("google", "spanish")
	self.sysargv = sys.argv

	print 'Number of arguments:', len(sys.argv), 'arguments.'
	print 'Argument List:', str(sys.argv)
	if len(sys.argv) == 1:
		print 'Please specify 1 Cancun module to run'
		sys.exit(1)

    def __del__(self):
        pass

    def modules(self):

        self.caudio = Caudio(self.voicesynthetizer)
        self.clock = Clock(self.voicesynthetizer)
        self.id = Identification(self.voicesynthetizer)
        self.reglamentos = Reglamentos(self.voicesynthetizer)
        self.messages = Messages(self.voicesynthetizer)
        self.morseteacher = MorseTeacher(self.voicesynthetizer)
        self.twitterc = TwitterC(self.voicesynthetizer)
        self.voicecommands =  VoiceCommands(self.voicesynthetizer)
        self.weather = Weather(self.voicesynthetizer)

    def run(self):
	
        if self.sysargv[1] == 'weather':
		self.weather.report()
	elif self.sysargv[1] == 'date':
		self.clock.date()
	elif self.sysargv[1] == 'hour':
		self.clock.hour()
	elif self.sysargv[1] == 'caudio':
		self.caudio.record()
		self.caudio.play()
	elif self.sysargv[1] == 'vts':
		self.voicecommands.sample()
	else:
		print 'No Cancun module found by that name'

	#while True:
		#self.id.identify()
		#time.sleep(5)
		#self.clock.date()
		#time.sleep(5)
		#self.clock.hour()
		#time.sleep(5)
		#self.weather.report()
		#time.sleep(5)
		#self.twitterc.sismologicomx()
		#time.sleep(2)
		#self.morseteacher.golearn()
		#time.sleep(5)
		#self.morseteacher.gocompete()
		#time.sleep(5)
		#self.messages.stations()
		#time.sleep(5)
		#self.reglamentos.read("learning/reglamentos.1")
		#time.sleep(5)
		#self.reglamentos.read("learning/reglamentos.2")
		#time.sleep(5)
		#self.reglamentos.read("learning/reglamentos.3")
		#time.sleep(5)
		#self.reglamentos.read("learning/reglamentos.4")
		#time.sleep(5)
		#self.reglamentos.read("learning/reglamentos.5")
		#time.sleep(5)

if __name__ == "__main__":

    cancun = CancunIrlp()
    cancun.modules()
    cancun.run()
