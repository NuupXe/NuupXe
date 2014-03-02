#!/usr/bin/python

import logging
import sys
import threading
import unicodedata
import time

from pushtotalk import PushToTalk

class VoiceSynthetizer(threading.Thread):

	def __init__(self, synthetizer, language):
		self.synthetizer = synthetizer
		self.language = language
		self.arguments = ""

		threading.Thread.__init__(self)
		self.lock = threading.Lock()

		self.setsynthetizer(self.synthetizer)



	def setsynthetizer(self, synthetizer):
		self.synthetizer = synthetizer
		self.setlanguage(self.language)
		self.setarguments()

        def getsynthetizer(self, synthetizer):
                return self.synthetizer

	def setlanguage(self, language):
                self.language = language
		if self.synthetizer == "festival":
			self.languageargument = "--language " + self.language
		elif self.synthetizer == "espeak":
			if self.language == "english":
				self.languageargument = "-v en"
			elif self.language == "spanish":
				self.languageargument = "-v es-la"

	def getlanguage(self, language):
		return self.language

	def setarguments(self):
		if self.synthetizer == "festival":
			self.text2speechargument = "--tts"
			self.arguments = self.synthetizer + " " + self.text2speechargument + " " + self.languageargument
		elif self.synthetizer == "espeak":
			self.text2speechargument = "--stdout"
			self.arguments = self.synthetizer + " " + self.languageargument + " " + self.text2speechargument

	def speechit(self, text):
		#text = unicodedata.normalize('NFKD', text)
		ptt = PushToTalk()
		text = text.encode('ASCII', 'ignore')

		if self.synthetizer == "festival":
			command = "echo \"" + text + "\" | " + self.arguments
		elif self.synthetizer == "espeak":
			command = self.arguments + " \"" + text + "\" | aplay"

		ptt.message(command)

if __name__ == "__main__":

	mytest = VoiceSynthetizer("festival", "spanish")
	mytest.speechit("proyecto cancun")
	mytest = VoiceSynthetizer("espeak", "spanish")
	mytest.speechit("proyecto cancun")

