#!/usr/bin/python

import ConfigParser

from morse import Morse
from phonetic import Phonetic
from voicesynthetizer import VoiceSynthetizer

class Identification:

	def __init__(self, voicesynthetizer):

		self.phonetic = Phonetic()
		self.morse = Morse()
		self.voicesynthetizer = voicesynthetizer
		
		self.conf = ConfigParser.ConfigParser()
                self.path = "../configuration/general.configuration"
		self.conf.read(self.path)

	def identify(self):
		message = self.conf.get("general", "radioclub") + ", " + self.conf.get("general", "systemname")
		message = message + " operado por " + ' '.join(self.phonetic.decode(self.conf.get("general", "callsign")))
		self.voicesynthetizer.speechit(message)
		self.morse.generate('xe1gyq')

if __name__ == '__main__':

	mytest = Identification()
	mytest.identify()
