#!/usr/bin/python

import random
import string
import sys
import time

sys.path.append('../modules')

from morse import Morse
from phonetic import Phonetic
from random import randint
from voicesynthetizer import VoiceSynthetizer

class MorseTeacher:

	def __init__(self):
		
		self.morse = Morse()
		self.speaker = VoiceSynthetizer("festival", "spanish")
		self.phonetic = Phonetic()

		self.message("Modulo de Aprendizaje de Codigo Morse")
		self.message("Sugerencias escribir a")
		self.message("".join(self.phonetic.decode('xe1gyq@gmail.com')))

	def __del__(self):
		pass

	def message(self, message):
		self.speaker.speechit(message)

	def randomnumber(self, n):
		range_start = 10**(n-1)
		range_end = (10**n)-1
		return randint(range_start, range_end)

	def randomletter(self, n):
		letters = []
		for x in range(0, n):
			letters.append(random.choice(string.ascii_letters))
		return "".join(letters)

	def randomnumberplay(self, help, iterations):
		random = self.randomnumber(iterations)
		for x in str(random):
			if help:
				self.speaker.speechit("Numero " + x + ", " + "".join(self.phonetic.decode(x)))
				self.speaker.speechit("Su codificacion es ")
			self.morse.generate(x)

	def randomletterplay(self, help, iterations):
		random = self.randomletter(iterations)
		for x in str(random):
			if help:
				self.speaker.speechit("Letra " + x + ", " + "".join(self.phonetic.decode(x)))
				self.speaker.speechit("Su codificacion es ")
			self.morse.generate(x)

if __name__ == '__main__':

	mymorse = MorseTeacher()
	mymorse.randomnumberplay(True, 5)
	mymorse.randomletterplay(True, 5)
