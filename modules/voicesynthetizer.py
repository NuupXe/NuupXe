#!/usr/bin/python

import commands
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

		self.ptt = PushToTalk()

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
		self.lock.acquire()
		self.ptt.openport()
		
		text = text.encode('ASCII', 'ignore')
		time.sleep(1)

		if self.synthetizer == "festival":
			command = "echo " + text + " | " + self.arguments
		elif self.synthetizer == "espeak":
			command = self.arguments + " \"" + text + "\" | aplay"
		status, output = commands.getstatusoutput(command)
		
		self.ptt.closeport()
		self.lock.release()

if __name__ == "__main__":

	mytest = VoiceSynthetizer("festival", "spanish")
	mytest.speechit("proyecto cancun")
	mytest = VoiceSynthetizer("espeak", "spanish")
	mytest.speechit("proyecto cancun")

