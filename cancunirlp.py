#!/usr/bin/python

import time
import sys

from apscheduler.scheduler import Scheduler
from apscheduler.threadpool import ThreadPool

from core.voicesynthetizer import VoiceSynthetizer

from modules.command import Command
from modules.clock import Clock
from modules.identification import Identification
from modules.messages import Messages
from modules.twitterc import TwitterC
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

        self.command = Command(self.voicesynthetizer)
        self.clock = Clock(self.voicesynthetizer)
        self.identification = Identification(self.voicesynthetizer)
        self.reglamentos = Reglamentos(self.voicesynthetizer)
        self.messages = Messages(self.voicesynthetizer)
        self.morseteacher = MorseTeacher(self.voicesynthetizer)
        self.twitterc = TwitterC(self.voicesynthetizer)
        self.weather = Weather(self.voicesynthetizer)

    def run(self):
	
	if self.sysargv[1] == 'identificacion':
                self.identification.identify()
	elif self.sysargv[1] == 'clima':
		self.weather.report()
	elif self.sysargv[1] == 'fecha':
		self.clock.date()
	elif self.sysargv[1] == 'hora':
		self.clock.hour()
	elif self.sysargv[1] == 'comandos':
		self.command.execute()
	elif self.sysargv[1] == 'sismologico':
                self.twitterc.sismologicomx()
	elif self.sysargv[1] == 'estaciones':
		self.messages.stations()
	elif self.sysargv[1] == 'morse':
		self.morseteacher.goask()
	else:
		print 'No Cancun module found by that name'

	#while True:
		#self.identification.identify()
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
