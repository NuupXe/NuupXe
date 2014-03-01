#!/usr/bin/python

import ConfigParser
import time
import sys

from apscheduler.scheduler import Scheduler
from datetime import date
from phonetic import Phonetic
from voicesynthetizer import VoiceSynthetizer

class Messages():

	def __init__(self):

		self.speaker = VoiceSynthetizer("festival", "spanish")
		self.phonetic = Phonetic()

	def repeaters(self):
		
		self.conf = ConfigParser.ConfigParser()
		self.path = "../configuration/repeaters"
		self.conf.read(self.path)

		self.speaker.speechit("Lista de Repetidores en la Ciudad de Guadalajara y Area Metropolitana")

		self.sections = self.conf.sections()
		for section in self.sections:

			owner = self.conf.get(section, 'owner')
			callsign = self.conf.get(section, 'callsign')
			frequency = self.conf.get(section, 'frequency')
			subtone = self.conf.get(section, 'subtone')
			sign = self.conf.get(section, 'sign')
			offset = self.conf.get(section, 'offset')

			self.speaker.speechit("Repetidor, " + ' '.join(self.phonetic.decode(callsign)))
			self.speaker.speechit("Propietario, " + owner)
			self.speaker.speechit("Frecuencia, " +  ', '.join(frequency.split('.')))
			self.speaker.speechit("Subtono, " +  ' '.join(self.phonetic.decode(subtone)))
			self.speaker.speechit("Offset, " + ' '.join(self.phonetic.decode(sign)) + " " + offset)

			time.sleep(2)

if __name__ == "__main__":

	mytest = Messages()
	mytest.repeaters()

