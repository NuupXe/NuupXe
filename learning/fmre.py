# -*- coding: utf-8 -*-
#!/usr/bin/python

import codecs
import random
import string
import sys
import time
import unicodedata

sys.path.append('../modules')

from morse import Morse
from phonetic import Phonetic
from random import randint
from voicesynthetizer import VoiceSynthetizer

class FmreTeacher:

	def __init__(self, voicesynthetizer):
		
		self.morse = Morse()
		self.speaker = voicesynthetizer
		self.phonetic = Phonetic()

	def __del__(self):
		pass

	def message(self, message):
		message = "\"" + message + "\"" 
		self.speaker.speechit(message)

	def welcome(self):
		self.message("Modulo de Aprendizaje de Reglamentos, sugerencias escribir a ")
		self.message("".join(self.phonetic.decode('xe1gyq@gmail.com')))

	def read(self, fmrefile):
		print '[Cancun] Reglamentos'
		file = codecs.open(fmrefile, encoding='utf-8')
		for line in file.readlines():
			line = unicodedata.normalize('NFKD', line)
			line = line.encode("ascii", "ignore")
			if "pausa" in line:
				self.message("Modulo de Aprendizaje de Reglamentos, Hagamos una Pausa de 1 minuto")
				time.sleep(60)
				self.message("Modulo de Aprendizaje de Reglamentos, Continuamos")
			else:
				self.message(line)
		return

if __name__ == '__main__':

	myfmre = FmreTeacher()
	myfmre.read('fmre.reglamento.1')

