#!/usr/bin/python

import json
import logging

from core.alive import alive
from core.emailx import Emailx
from core.twitterc import TwitterC
from core.voicerecognition import VoiceRecognition

class VoiceExperimental(object):

    def __init__(self, voicesynthetizer):

        self.modulename = 'VoiceExperimental'
        self.voicesynthetizer = voicesynthetizer
        self.emailx = Emailx()
        self.twitterc = TwitterC('twython')
        self.voicerecognition = VoiceRecognition(self.voicesynthetizer)

        self.setup()

    def __del__(self):

        self.cleanup()

    def setup(self):

        logging.info('Voice Experimental Setup')
        self.voicerecognition.languageset('spanish')
        self.voicesynthetizer._set_language_argument("spanish")

    def cleanup(self):

        logging.info('Voice Experimental Cleanup')
        self.voicerecognition.languageset('spanish')
        self.voicesynthetizer._set_language_argument("spanish")

    def listen(self):

        logging.info('Voice Experimental Listen')
        self.voicesynthetizer.speechit('Hola! Dime tu frase!')
        self.voicerecognition.record()
        question = self.voicerecognition.recognize('False')
        logging.info('Phrase? ' + question)
        self.voicesynthetizer.speechit(question)
        question = '#VoiceRecognition ' + question.capitalize()
        self.twitterc.timeline_set('#' + self.modulename + ' ' + question, media=None)
        self.emailx.create('nuupxe@gmail.com', 'Voice Experimental Listen', question)
        self.emailx.send()
        alive(modulename=self.modulename, modulemessage=question)

# End of File
