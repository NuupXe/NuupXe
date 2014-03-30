#!/usr/bin/python

import ConfigParser
import time
import sys

from apscheduler.scheduler import Scheduler
from datetime import date
from morse import Morse
from phonetic import Phonetic
from voicesynthetizer import VoiceSynthetizer

class Messages():

	def __init__(self, voicesynthetizer):

		self.morse = Morse()
		self.speaker = voicesynthetizer
		self.phonetic = Phonetic()

	def stations(self):

		self.conf = ConfigParser.ConfigParser()
		self.path = "../configuration/stations"
		self.conf.read(self.path)

		city = self.conf.get('general', 'city')
		self.speaker.speechit("Lista de Repetidores y Estaciones en la ciudad de " + city)

		self.sections = self.conf.sections()
		for section in self.sections:

			try:
				type = self.conf.get(section, 'type')			
				owner = self.conf.get(section, 'owner')
				callsign = self.conf.get(section, 'callsign')
				frequency = self.conf.get(section, 'frequency')
				subtone = self.conf.get(section, 'subtone')

				self.speaker.speechit(type + ", " + ' '.join(self.phonetic.decode(callsign)))
				self.morse.generate(callsign)
				self.speaker.speechit("Propietario, " + owner)
				self.speaker.speechit("Frecuencia, " +  ', '.join(frequency.split('.')))
				self.speaker.speechit("Subtono, " +  ' '.join(self.phonetic.decode(subtone)))

				sign = self.conf.get(section, 'sign')
				offset = self.conf.get(section, 'offset')
				
				if sign == 'simplex':
					self.speaker.speechit("Offset, " + sign)
				else:
					self.speaker.speechit("Offset, " + ' '.join(self.phonetic.decode(sign)) + " " + offset)	

				time.sleep(2)

			except:

				None

if __name__ == "__main__":

	mytest = Messages()
	mytest.repeaters()
