#!/usr/bin/python

import json
import logging

from core.alive import alive
from core.voicerecognition import VoiceRecognition
from core.wolfram import Wolfram
from core.xspeechrecognition import xSpeechRecognition

class WolframAlpha(object):

    def __init__(self, voicesynthetizer):

        self.modulename = 'WolframAlpha'
        self.voicesynthetizer = voicesynthetizer
        self.voicerecognition = VoiceRecognition(self.voicesynthetizer)
        self.wolfram = Wolfram()
        self.idSpeechRecognition = xSpeechRecognition()

    def __del__(self):

        self.cleanup()

    def setup(self):

        logging.info('Wolfram Alpha Setup')
        self.voicerecognition.languageset('english')
        self.voicesynthetizer.setlanguage("english")

    def cleanup(self):

        logging.info('Wolfram Alpha Cleanup')
        self.voicerecognition.languageset('spanish')
        self.voicesynthetizer.setlanguage("spanish")

    def ask(self):

        logging.info('Wolfram Alpha Ask')
        self.setup()
        self.voicesynthetizer.speechit('Yes! What is your question for Wolfram Alpha?', 'english')
        self.voicerecognition.record()
        question = self.voicerecognition.recognize('False')
        questionmessage = 'Question? ' + question
        logging.info(questionmessage)
        self.voicesynthetizer.speechit(question, 'english')
        answer = self.wolfram.question(question)
        if answer != None:
            self.voicesynthetizer.speechit(answer, 'english')
            answermessage = 'Answer? ' + answer
            logging.info(answermessage)
        else:
            answermessage = 'Answer? Sorry! Something went wrong!'
            self.voicesynthetizer.speechit(answermessage, 'english')
        self.cleanup()

        alive(modulename=self.modulename, modulemessage=questionmessage + ' ' + answermessage )

# End of File
