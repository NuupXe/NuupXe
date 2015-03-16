#!/usr/bin/python

import json
import logging

from core.voicecommand import VoiceCommand
from core.wolfram import Wolfram

class WolframAlpha(object):

    def __init__(self, voicesynthetizer):

        self.voicesynthetizer = voicesynthetizer
        self.voicecommand = VoiceCommand(self.voicesynthetizer)
        self.wolfram = Wolfram()

    def setup(self):

        logging.info('Wolfram Alpha Setup')
        self.voicecommand.languageset('english')
        self.voicesynthetizer.setlanguage("english")

    def cleanup(self):

        logging.info('Wolfram Alpha Cleanup')
        self.voicecommand.languageset('spanish')
        self.voicecommand.languageset('spanish')
        self.voicesynthetizer.setlanguage("spanish")

    def report(self):

        logging.info('Wolfram Alpha Report')
        self.setup()
        self.voicecommand.record()
        question = self.voicecommand.decode('False')
        logging.info(question)
        self.voicesynthetizer.speechit(question)
        answer = self.wolfram.question(question)
        self.voicesynthetizer.speechit(answer)
        logging.info(answer)

# End of File
