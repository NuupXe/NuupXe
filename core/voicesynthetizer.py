#!/usr/bin/python

import logging
import sys
import threading
import unicodedata
import time

from pushtotalk import PushToTalk

class VoiceSynthetizer(logging.Handler):

    def __init__(self, synthetizer, language):
        self.synthetizer = synthetizer
        self.language = language
        self.arguments = ""

        self.setsynthetizer(self.synthetizer)

    def setsynthetizer(self, synthetizer):
        self.synthetizer = synthetizer
        self.setlanguage(self.language)
        self.setarguments()

    def getsynthetizer(self):
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
        elif self.synthetizer == "google":
            if self.language == "english":
                self.languageargument = "en"
            elif self.language == "spanish":
                self.languageargument = "es"

    def getlanguage(self):
        return self.language

    def setarguments(self):
        if self.synthetizer == "festival":
            self.text2speechargument = "--tts"
            self.arguments = self.synthetizer + " " + self.text2speechargument + " " + self.languageargument
        elif self.synthetizer == "espeak":
            self.text2speechargument = "--stdout"
            self.arguments = self.synthetizer + " " + self.languageargument + " " + self.text2speechargument
        elif self.synthetizer == "google":
            self.arguments = self.languageargument

    def speechit(self, text):
        self.setarguments()
        self.pushtotalk = PushToTalk()
        logging.info(text)

        if self.synthetizer == "festival":
            command = "echo \"" + text + "\" | " + self.arguments
        elif self.synthetizer == "espeak":
            command = self.arguments + " \"" + text + "\" | aplay"
        elif self.synthetizer == "google":
            command = "core/google.sh " + " " + self.arguments + " " + text
        self.pushtotalk.message(command)

# End of File
