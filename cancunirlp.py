#!/usr/bin/python

import time
import sys

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

    def run(self):

	if self.sysargv[1] == "assistant":
		self.assistant.demo1()
	elif self.sysargv[1] == 'identification':
		self.identification.identify()
	elif self.sysargv[1] == 'weather':
		self.weather.report()
	elif self.sysargv[1] == 'date':
		self.clock.date()
	elif self.sysargv[1] == 'hour':
		self.clock.hour()
	elif self.sysargv[1] == 'commands':
		self.command.execute()
	elif self.sysargv[1] == 'seismology':
                self.seismology.SismologicoMX()
	elif self.sysargv[1] == 'stations':
		self.messages.stations()
	elif self.sysargv[1] == 'morse':
		self.morseteacher.goask()
	elif self.sysargv[1] == 'bc':
		self.command.background()
	elif self.sysargv[1] == 'wolfram':
		self.wolfram.question('how many grams in kilograms')
	else:
		print 'No Cancun module found by that name'

if __name__ == "__main__":

    cancun = CancunIrlp()
    cancun.modules()
    cancun.run()
