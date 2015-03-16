#!/usr/bin/python

import json
import logging

from core.voicerecognition import VoiceRecognition

class VoiceExperimental(object):

    def __init__(self, voicesynthetizer):

        self.voicesynthetizer = voicesynthetizer
        self.voicerecognition = VoiceRecognition(self.voicesynthetizer)

    def setup(self):

        logging.info('Voice Experimental Setup')
        self.voicerecognition.languageset('spanish')
        self.voicesynthetizer.setlanguage("spanish")

    def cleanup(self):

        logging.info('Voice Experimental Cleanup')
        self.voicerecognition.languageset('spanish')
        self.voicesynthetizer.setlanguage("spanish")

    def listen(self):

        logging.info('Voice Experimental Listen')
        self.setup()
        self.voicesynthetizer.speechit('Hola! Dime tu frase!')
        self.voicerecognition.record()
        question = self.voicerecognition.recognize('False')
        logging.info('Phrase? ' + question)
        print question
        self.voicesynthetizer.speechit(question)
        self.cleanup()

# End of File
