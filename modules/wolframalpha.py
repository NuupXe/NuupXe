#!/usr/bin/python

import json
import logging

from core.voicerecognition import VoiceRecognition
from core.wolfram import Wolfram

class WolframAlpha(object):

    def __init__(self, voicesynthetizer):

        self.voicesynthetizer = voicesynthetizer
        self.voicerecognition = VoiceRecognition(self.voicesynthetizer)
        self.wolfram = Wolfram()

        self.setup()

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
        self.voicesynthetizer.speechit('Yes! What is your question for Wolfram Alpha?')
        self.voicerecognition.record()
        question = self.voicerecognition.recognize('False')
        logging.info('Question? ' + question)
        self.voicesynthetizer.speechit(question)
        answer = self.wolfram.question(question)
        if answer != None:
            self.voicesynthetizer.speechit(answer)
            logging.info('Answer! ' + answer)
        else:
            self.voicesynthetizer.speechit('Sorry! We do not have an answer')

# End of File
